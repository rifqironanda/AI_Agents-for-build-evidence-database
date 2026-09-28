# Local Database Schema

Database: data/evidence.db

## documents

One row per PDF: document_id, filename, path, page_count, file_hash.

## page_text

One row per extracted page: document_id, page_number, text.

## summaries

One row per summary: document_id, summary, key_points, limitations, model.

## validations

One row per document: document_id, status, notes. Default status is pending.

## Validation principle

AI output is not evidence by itself. The original PDF and page-level text remain the research source. The validation table records the researcher's decision.