"""Agent for discovering and reading local PDF documents."""

from pathlib import Path
from app.pdf_reader import find_pdfs, read_pdf


def discover_documents(directory: str):
    paths = find_pdfs(directory)
    print(f"   Found {len(paths)} PDF file(s)")
    return paths


def read_document(path: Path):
    print(f"   Reading: {path.name}")
    return read_pdf(path)
