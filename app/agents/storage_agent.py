"""Deterministic local database storage."""

from app.db import save_document, save_summary


def store(document, summary) -> None:
    save_document(document)
    save_summary(summary)
