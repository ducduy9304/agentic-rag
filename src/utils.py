"""
Small helper functions used by many parts of the project.

There are three groups of helpers here:
  1. File system helpers (clear a folder).
  2. PDF -> Markdown conversion. The PDFs are converted to markdown first
     because markdown is easier to chunk (we can split at headings).
  3. Token counting. We use this to check if our prompt is too long for
     the LLM context window.
"""

import os
from pathlib import Path
import shutil
import config
import pymupdf4llm
import glob
import tiktoken
import pymupdf.layout

def clear_directory_contents(directory: Path) -> None:
    """Delete everything under directory but not the directory itself (safe for Docker volume / bind mount roots)"""
    # We delete the contents but NOT the folder itself. This is important
    # when the folder is a Docker volume — if we delete the folder, the
    # mount breaks and the container cannot write to it anymore.
    directory = Path(directory)
    if not directory.is_dir():
        return
    for child in directory.iterdir():
        if child.is_dir():
            # Folders need rmtree because they may contain other files.
            shutil.rmtree(child)
        else:
            # Single files can just be unlinked (deleted).
            child.unlink()

def pdf_to_markdown(pdf_path, output_dir):
    # Convert ONE PDF file into a markdown file.
    # We use pymupdf4llm because it keeps the structure (headings, lists)
    # in the output, which makes chunking by heading possible later.
    doc = pymupdf.open(pdf_path)
    # We turn off headers, footers, and images because they add noise
    # without adding useful information for the LLM.
    md = pymupdf4llm.to_markdown(doc, header=False, footer=False, page_separators=True, ignore_images=True, write_images=False, image_path=None)
    # Some PDFs contain weird unicode characters that break encoding.
    # This encode/decode trick removes any bad characters safely.
    md_cleaned = md.encode('utf-8', errors='surrogatepass').decode('utf-8', errors='ignore')
    # Save the result as "<original_pdf_name>.md" in the output folder.
    output_path = Path(output_dir) / Path(doc.name).stem
    Path(output_path).with_suffix(".md").write_bytes(md_cleaned.encode('utf-8'))

def pdfs_to_markdowns(path_pattern, overwrite: bool = False):
    # Convert MANY PDFs in one call. `path_pattern` is a glob pattern,
    # for example "/data/*.pdf".
    output_dir = Path(config.MARKDOWN_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    for pdf_path in map(Path, glob.glob(path_pattern)):
        md_path = (output_dir / pdf_path.stem).with_suffix(".md")
        # If the markdown file already exists, skip the PDF (unless the
        # caller asks to overwrite). This saves a lot of time when we
        # re-run the pipeline.
        if overwrite or not md_path.exists():
            pdf_to_markdown(pdf_path, output_dir)

def estimate_context_tokens(messages: list) -> int:
    # Count roughly how many tokens a list of messages takes.
    # We use this to decide when the conversation is getting too long
    # for the LLM and we need to summarize or trim it.
    try:
        # tiktoken is OpenAI's tokenizer. It is not 100% correct for other
        # models (like Qwen), but the count is close enough for a check.
        encoding = tiktoken.encoding_for_model("gpt-4")
    except:
        # Fallback if the model name is not recognised. cl100k_base is the
        # same tokenizer GPT-4 uses, so this gives the same result.
        encoding = tiktoken.get_encoding("cl100k_base")
    # Add up the token count of every message that actually has content.
    return sum(len(encoding.encode(str(msg.content))) for msg in messages if hasattr(msg, 'content') and msg.content)
