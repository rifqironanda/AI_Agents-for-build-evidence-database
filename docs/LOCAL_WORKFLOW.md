# Local Workflow

## 1. Collect sources manually

Place selected PDFs into documents/ or another local directory.

## 2. Run

    python -m app.main --pdf-dir documents

## 3. Inspect

Open data/evidence.db with a SQLite viewer. Inspect documents, page_text, summaries, and validations.

## 4. Validate

Compare each generated summary against the original PDF. Keep status as pending until manually reviewed.

## Cost model

PDF parsing: local.

Database: local.

Summarization: local through Ollama.

Internet search: not used.

Cloud API: not required.