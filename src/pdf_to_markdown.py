"""
Batch PDF → Markdown converter using a local Vision-Language Model.

Ported from https://github.com/GiovanniPasq/chunky (backend/converters/vlm.py),
trimmed down for offline CLI use:

    * Each PDF page is rasterised to PNG and sent to an OpenAI-compatible
      VLM endpoint (Ollama by default, model ``qwen3-vl``).
    * Pages are transcribed concurrently inside one PDF (semaphore-bounded
      so peak memory is ~N_CONCURRENT x one PNG, not entire_pdf x PNG).
    * Successful pages are checkpointed under ``markdown_docs/.checkpoints/``
      so an interrupted run (Ctrl-C, network blip, Qwen crash) resumes
      without re-transcribing finished pages.
    * Failed pages get an inline ``<!-- page N failed -->`` placeholder and
      the job continues — one bad page never aborts a 200-page document.
    * Two tqdm bars: outer = files, inner = pages of the current file.

Usage:
    python pdf_to_markdown.py <pdf_dir>
    python pdf_to_markdown.py ./pdfs --model qwen3-vl --concurrency 4

Output: one ``.md`` per PDF in ``markdown_docs/`` (config.MARKDOWN_DIR),
ready for document_chunker.py to pick up.
"""

from __future__ import annotations

import argparse
import asyncio
import base64
import logging
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import fitz  # PyMuPDF
from tqdm import tqdm

import config

logger = logging.getLogger("pdf_to_markdown")

# ---------------------------------------------------------------------------
# Defaults — override via CLI flags
# ---------------------------------------------------------------------------

DEFAULT_BASE_URL = "http://localhost:11434/v1"
DEFAULT_MODEL = "qwen3-vl:8b-instruct-q4_K_M"
DEFAULT_API_KEY = "ollama"            # any non-empty string; Ollama ignores it
DEFAULT_TEMPERATURE = 0.1
DEFAULT_RENDER_DPI = 300              # 300 = highest quality, 150 = fastest
DEFAULT_CONCURRENCY = 4               # in-flight pages per PDF
DEFAULT_MAX_RETRIES = 4
DEFAULT_RETRY_BASE_DELAY_S = 2.0

CHECKPOINT_ROOT_NAME = ".checkpoints"

SYSTEM_PROMPT = """You are an expert document parser specializing in converting PDF pages to markdown format.

**Your task:** Extract ALL content from the provided page image and return it as clean, well-structured markdown.

**Text Extraction Rules:**
1. Preserve the EXACT text as written (including typos, formatting, special characters)
2. Maintain the logical reading order (top-to-bottom, left-to-right)
3. Preserve hierarchical structure using appropriate markdown headers (#, ##, ###)
4. Keep paragraph breaks and line spacing as they appear
5. Use markdown lists (-, *, 1.) for bullet points and numbered lists
6. Preserve text emphasis: **bold**, *italic*, `code`
7. For multi-column layouts, extract left column first, then right column

**Tables:**
- Convert all tables to markdown table format
- Preserve column alignment and structure
- Use | for columns and - for headers

**Mathematical Formulas:**
- Convert to LaTeX format: inline `$...$`, display `$$...$$`
- If LaTeX conversion is uncertain, describe the formula clearly

**Images, Diagrams, Charts:**
- Insert markdown image placeholder: `![Description](image)`
- Provide a detailed, informative description including:
  * Type of visual (photo, diagram, chart, graph, illustration)
  * Main subject or purpose
  * Key elements, labels, or data points
  * Colors, patterns, or notable visual features
  * Context or relationship to surrounding text
- For charts/graphs: mention axes, data trends, and key values
- For diagrams: describe components and their relationships

**Special Elements:**
- Footnotes: Use markdown footnote syntax `[^1]`
- Citations: Preserve as written
- Code blocks: Use triple backticks with language specification
- Quotes: Use `>` for blockquotes
- Links: Preserve as `[text](url)` if visible

**Quality Guidelines:**
- DO NOT add explanations, comments, or meta-information
- DO NOT skip or summarize content
- DO NOT invent or hallucinate text not present in the image
- DO NOT include "Here is the markdown..." or similar preambles
- Output ONLY the markdown content, nothing else

**Output Format:**
Return raw markdown with no wrapper, no code blocks, no explanations. Start immediately with the page content."""


# ---------------------------------------------------------------------------
# Checkpoint store — atomic per-page on-disk cache
# ---------------------------------------------------------------------------

class CheckpointStore:
    """Per-PDF directory holding one ``page_NNNN.md`` per completed page."""

    def __init__(self, pdf_stem: str, root: Path) -> None:
        self._dir = root / CHECKPOINT_ROOT_NAME / f"{pdf_stem}_vlm"

    @property
    def dir(self) -> Path:
        return self._dir

    def has_page(self, page_num: int) -> bool:
        return (self._dir / self._fname(page_num)).is_file()

    def load_page(self, page_num: int) -> str:
        return (self._dir / self._fname(page_num)).read_text(encoding="utf-8")

    def save_page(self, page_num: int, markdown: str) -> None:
        self._dir.mkdir(parents=True, exist_ok=True)
        target = self._dir / self._fname(page_num)
        tmp = target.with_suffix(target.suffix + ".tmp")
        tmp.write_text(markdown, encoding="utf-8")
        os.replace(tmp, target)

    def completed_pages(self) -> set[int]:
        if not self._dir.exists():
            return set()
        out: set[int] = set()
        for f in self._dir.glob("page_*.md"):
            try:
                out.add(int(f.stem[len("page_"):]) - 1)
            except ValueError:
                continue
        return out

    @staticmethod
    def _fname(page_num: int) -> str:
        return f"page_{page_num + 1:04d}.md"


# ---------------------------------------------------------------------------
# Per-page result
# ---------------------------------------------------------------------------

@dataclass
class _PageResult:
    page_num: int          # 0-indexed
    markdown: str | None
    error: str | None
    cached: bool = False


# ---------------------------------------------------------------------------
# VLM converter
# ---------------------------------------------------------------------------

class VLMConverter:
    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        base_url: str = DEFAULT_BASE_URL,
        api_key: str = DEFAULT_API_KEY,
        temperature: float = DEFAULT_TEMPERATURE,
        render_dpi: int = DEFAULT_RENDER_DPI,
        concurrency: int = DEFAULT_CONCURRENCY,
        max_retries: int = DEFAULT_MAX_RETRIES,
        retry_base_delay_s: float = DEFAULT_RETRY_BASE_DELAY_S,
    ) -> None:
        self.model = model
        self.base_url = base_url
        self.api_key = api_key
        self.temperature = temperature
        self.render_dpi = render_dpi
        self.concurrency = concurrency
        self.max_retries = max_retries
        self.retry_base_delay_s = retry_base_delay_s

    # ------------------------------------------------------------------
    # Public entry point — sync façade over an internal asyncio loop
    # ------------------------------------------------------------------

    def convert(self, pdf_path: Path, checkpoint: CheckpointStore | None = None) -> tuple[str, list[int]]:
        """Convert one PDF to Markdown.

        Returns ``(markdown, failed_pages_1_indexed)``.
        """
        return asyncio.run(self._async_convert(pdf_path, checkpoint))

    # ------------------------------------------------------------------
    # Async core
    # ------------------------------------------------------------------

    async def _async_convert(
        self, pdf_path: Path, checkpoint: CheckpointStore | None
    ) -> tuple[str, list[int]]:
        loop = asyncio.get_running_loop()

        with fitz.open(str(pdf_path)) as doc:
            total = doc.page_count

        cached = checkpoint.completed_pages() if checkpoint else set()

        sem = asyncio.Semaphore(self.concurrency)
        pbar = tqdm(
            total=total,
            desc=f"  {pdf_path.name}",
            unit="pg",
            leave=False,
            position=1,
        )

        from openai import AsyncOpenAI
        client = AsyncOpenAI(base_url=self.base_url, api_key=self.api_key)

        async def _process(page_num: int) -> _PageResult:
            # Fast path: cached
            if page_num in cached and checkpoint is not None:
                try:
                    md = await loop.run_in_executor(None, checkpoint.load_page, page_num)
                    pbar.update(1)
                    return _PageResult(page_num, md, None, cached=True)
                except OSError as exc:
                    logger.warning("checkpoint load failed page %d: %s — re-transcribing", page_num + 1, exc)
                    # Fall through; pbar still ticks once on the re-transcribe path.

            def _render() -> str:
                with fitz.open(str(pdf_path)) as d:
                    return self._render_page_b64(d[page_num])

            try:
                async with sem:
                    img_b64 = await loop.run_in_executor(None, _render)
                    md = await self._transcribe_with_retry(client, img_b64, page_num)
            except Exception as exc:
                err = f"{type(exc).__name__}: {str(exc)[:200]}"
                logger.warning("page %d failed: %s", page_num + 1, err)
                pbar.update(1)
                return _PageResult(page_num, None, err)

            if checkpoint is not None:
                try:
                    await loop.run_in_executor(None, checkpoint.save_page, page_num, md)
                except OSError as exc:
                    logger.warning("checkpoint save failed page %d: %s", page_num + 1, exc)

            pbar.update(1)
            return _PageResult(page_num, md, None)

        try:
            results = await asyncio.gather(*[_process(i) for i in range(total)])
        finally:
            pbar.close()
            await client.close()

        failed = sorted(r.page_num + 1 for r in results if r.error is not None)

        parts: list[str] = []
        for r in sorted(results, key=lambda x: x.page_num):
            marker = f"<!-- page-marker:{r.page_num + 1} -->"
            body = f"<!-- page {r.page_num + 1} failed: {r.error} -->" if r.error else (r.markdown or "")
            parts.append(f"{marker}\n{body}")
        return "\n\n---\n\n".join(parts), failed

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _render_page_b64(self, page) -> str:
        scale = self.render_dpi / 72
        pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale))
        return base64.b64encode(pix.tobytes("png")).decode("utf-8")

    async def _transcribe_once(self, client, img_b64: str) -> str:
        resp = await client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": f"data:image/png;base64,{img_b64}"},
                    {"type": "text", "text": SYSTEM_PROMPT},
                ],
            }],
        )
        if not resp.choices:
            raise ValueError("VLM returned empty choices")
        text = (resp.choices[0].message.content or "").strip()
        text = re.sub(r"^```(?:markdown)?\n?", "", text)
        text = re.sub(r"\n?```$", "", text)
        return text.strip()

    async def _transcribe_with_retry(self, client, img_b64: str, page_num: int) -> str:
        from openai import APIConnectionError, APIStatusError, APITimeoutError

        last_exc: Exception | None = None
        for attempt in range(self.max_retries):
            try:
                return await self._transcribe_once(client, img_b64)
            except Exception as exc:
                retryable = isinstance(exc, (APITimeoutError, APIConnectionError)) or (
                    isinstance(exc, APIStatusError) and (exc.status_code >= 500 or exc.status_code == 429)
                )
                if not retryable:
                    raise
                last_exc = exc
                if attempt < self.max_retries - 1:
                    delay = self.retry_base_delay_s * (2 ** attempt)
                    logger.warning(
                        "page %d retry %d/%d in %.0fs (%s)",
                        page_num + 1, attempt + 1, self.max_retries, delay, type(exc).__name__,
                    )
                    await asyncio.sleep(delay)
        assert last_exc is not None
        raise last_exc


# ---------------------------------------------------------------------------
# CLI driver
# ---------------------------------------------------------------------------

def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Batch PDF → Markdown via local VLM.")
    p.add_argument(
        "pdf_dir",
        type=Path,
        nargs="?",
        default=Path("/home/ducduy/agentic-rag/pdf_docs"),
        help="Folder containing input .pdf files",
    )
    p.add_argument("-o", "--output-dir", type=Path, default=Path(config.MARKDOWN_DIR),
                   help=f"Output folder (default: {config.MARKDOWN_DIR})")
    p.add_argument("--model", default=DEFAULT_MODEL)
    p.add_argument("--base-url", default=DEFAULT_BASE_URL)
    p.add_argument("--api-key", default=DEFAULT_API_KEY)
    p.add_argument("--dpi", type=int, default=DEFAULT_RENDER_DPI)
    p.add_argument("--concurrency", type=int, default=DEFAULT_CONCURRENCY,
                   help="Concurrent in-flight pages per PDF")
    p.add_argument("--overwrite", action="store_true",
                   help="Re-convert PDFs even if .md already exists")
    p.add_argument("--no-resume", action="store_true",
                   help="Ignore existing checkpoint and re-transcribe every page")
    p.add_argument("-v", "--verbose", action="store_true")
    return p.parse_args()


def main() -> int:
    args = _parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    if not args.pdf_dir.is_dir():
        print(f"Error: {args.pdf_dir} is not a directory", file=sys.stderr)
        return 2

    args.output_dir.mkdir(parents=True, exist_ok=True)

    pdfs = sorted(args.pdf_dir.glob("*.pdf"))
    if not pdfs:
        print(f"No PDFs found in {args.pdf_dir}", file=sys.stderr)
        return 1

    converter = VLMConverter(
        model=args.model,
        base_url=args.base_url,
        api_key=args.api_key,
        render_dpi=args.dpi,
        concurrency=args.concurrency,
    )

    summary: list[tuple[str, int, int]] = []  # (name, total_pages_failed, status)
    outer = tqdm(pdfs, desc="Files", unit="pdf", position=0)
    for pdf in outer:
        out_md = args.output_dir / f"{pdf.stem}.md"
        if out_md.exists() and not args.overwrite:
            outer.write(f"⏭  skip (exists): {pdf.name}")
            continue

        ckpt = None if args.no_resume else CheckpointStore(pdf.stem, args.output_dir)
        try:
            markdown, failed = converter.convert(pdf, checkpoint=ckpt)
        except KeyboardInterrupt:
            outer.write(f"\n⏸  interrupted on {pdf.name} — progress checkpointed, rerun to resume")
            return 130
        except Exception as exc:
            outer.write(f"✗  {pdf.name}: {type(exc).__name__}: {exc}")
            summary.append((pdf.name, -1, -1))
            continue

        out_md.write_text(markdown, encoding="utf-8")
        status = f"✓ {pdf.name} ({len(failed)} failed pages)" if failed else f"✓ {pdf.name}"
        outer.write(status)
        summary.append((pdf.name, len(failed), 0))

    outer.close()

    print("\n=== Summary ===")
    for name, n_failed, status in summary:
        tag = "ERROR" if status < 0 else ("OK" if n_failed == 0 else f"OK ({n_failed} failed pages)")
        print(f"  {tag:30s} {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
