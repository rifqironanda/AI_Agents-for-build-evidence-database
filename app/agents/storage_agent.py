"""Deterministic storage agent."""
from app.db import upsert_source, save_summary


def store(source, summary: dict) -> None:
    upsert_source(source)
    save_summary(source.source_id, summary)
