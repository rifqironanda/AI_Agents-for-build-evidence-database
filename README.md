# AI Agents for Evidence Database

Local-first evidence database for quantum-computing and banking research.

## Purpose

The researcher manually selects and reviews sources. This repository automates
only repetitive local work: discovering PDFs, extracting page text, generating
a local summary, and storing the result for manual validation.

No automatic internet search is part of the default pipeline. No cloud LLM API
is required.

## Architecture

Manual source collection -> local PDF folder -> Document Agent -> PyMuPDF ->
local Ollama model -> summary -> SQLite -> manual validation.

## Setup

Requirements: Python 3.10+, a local PDF collection, Ollama, and a local Ollama
instruct model.

Run:

    .\.venv\Scripts\Activate.ps1
    python -m pip install -r requirements.txt
    mkdir documents

Check Ollama:

    python -c "from app.llm import llm; print(llm.available())"

Put PDFs in documents/ and run:

    python -m app.main --pdf-dir documents

Database: data/evidence.db

Tables:
- documents: PDF identity and metadata
- page_text: extracted text with page numbers
- summaries: local-LLM summaries
- validations: human validation state

AI output is never automatically marked as validated.

## Cost and privacy

PDF parsing and SQLite run locally. Summarization runs through Ollama on
localhost. No Brave, OpenAI, Google, or other cloud API is used.

## Scope

This MVP summarizes documents. It does not yet claim reliable claim extraction,
citation verification, temporal reasoning, or risk scoring.

See docs/ARCHITECTURE.md, docs/DATABASE_SCHEMA.md, and
docs/LOCAL_WORKFLOW.md.

## Roadmap

1. Local PDF ingestion
2. Local summarization
3. Manual validation
4. Claim/evidence extraction
5. Page-level evidence linking
6. Temporal expression extraction
7. Confidence and validation workflow
8. Local corpus search
9. Optional internet discovery as a separate module
