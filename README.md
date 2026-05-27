# agentic-rag

An agentic RAG (Retrieval-Augmented Generation) project built with LangChain, LangGraph, and Qdrant.

## Requirements

- Python >= 3.11

## Installation

Clone the repository first:

```bash
git clone https://github.com/ducduy9304/agentic-rag.git
cd agentic-rag
```

Then pick one of the methods below.

### Using uv (recommended)

```bash
uv sync
```

This reads `pyproject.toml` + `uv.lock` and installs the exact pinned versions into `.venv/`.

### Using pip

```bash
python -m venv .venv
source .venv/bin/activate      # On Windows: .venv\Scripts\activate
pip install .
```

### Using conda

```bash
conda create -n agentic-rag python=3.11
conda activate agentic-rag
pip install .
```

## Usage

Run the entry point:

```bash
# With uv
uv run main.py

# With pip/conda (after activating the env)
python main.py
```

## Project Structure

```
agentic-rag/
├── src/
│   └── pdf_to_markdown.py    # PDF parsing utilities
├── main.py                    # Entry point
├── pyproject.toml             # Project metadata & dependencies
└── uv.lock                    # Locked dependency versions (for uv)
```
