# Local-First Agent Architecture

The researcher manually selects sources. The local system discovers PDFs, extracts page text with PyMuPDF, summarizes selected text with an Ollama model on localhost, and stores results in SQLite.

## Components

Document Agent: finds local PDFs and reads them.

Local Summarizer Agent: sends extracted text only to the local Ollama server and returns structured summary output.

Storage Agent: deterministically writes documents and summaries to SQLite.

## Flow

Researcher -> PDF folder -> Document Agent -> PyMuPDF -> Ollama localhost -> Summary -> SQLite -> Manual validation.

## Constraints

1. No automatic internet search.
2. No cloud LLM dependency.
3. AI output is never automatically validated.
4. PDF page numbers are preserved.
5. SHA-256 identifies each document.
6. Source selection remains under researcher control.

## Future

Evidence extraction can later add claim, exact quote, page/section, topic, threat type, time expression, and confidence, all traceable to the original PDF.