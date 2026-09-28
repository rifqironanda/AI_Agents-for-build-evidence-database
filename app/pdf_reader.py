"""Local PDF reader. No internet access is used."""

import hashlib
from pathlib import Path
import fitz

from app.models import Document, PageText


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_pdf(path: Path) -> tuple[Document, list[PageText]]:
    with fitz.open(path) as pdf:
        document_id = "DOC-" + file_hash(path)[:12]
        document = Document(
            document_id=document_id,
            filename=path.name,
            path=str(path),
            page_count=len(pdf),
            file_hash=file_hash(path),
        )
        pages = [
            PageText(
                document_id=document_id,
                page_number=index + 1,
                text=page.get_text("text").strip(),
            )
            for index, page in enumerate(pdf)
        ]
    return document, pages


def find_pdfs(directory: str) -> list[Path]:
    root = Path(directory)
    return sorted(root.rglob("*.pdf")) if root.exists() else []
