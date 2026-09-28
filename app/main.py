"""CLI for the local PDF evidence pipeline."""
import argparse
from app.agents.pdf_agent import discover_documents, read_document
from app.agents.storage_agent import store
from app.agents.summarizer_agent import summarize
from app.db import init_db, save_pages

def run(pdf_directory: str):
    print("\n=== LOCAL PDF EVIDENCE AGENT ===")
    print(f"PDF directory: {pdf_directory}")
    init_db()
    print("\n1. DOCUMENT AGENT")
    paths = discover_documents(pdf_directory)
    if not paths:
        print("   No PDF files found.")
        return
    total = 0
    for path in paths:
        print("\n2. PDF READER")
        document, pages = read_document(path)
        save_pages(pages)
        text = "\n\n".join(f"[Page {p.page_number}]\n{p.text}" for p in pages if p.text)
        print(f"   Document ID: {document.document_id}")
        print(f"   Pages: {document.page_count}")
        print(f"   Extracted characters: {len(text):,}")
        print("\n3. LOCAL SUMMARIZER AGENT")
        summary = summarize(document.document_id, document.filename, text)
        print(f"   Model: {summary.model}")
        print(f"   Summary: {summary.summary}")
        print("\n4. STORAGE AGENT")
        store(document, summary)
        print("   Saved to data/evidence.db")
        total += 1
    print(f"\n=== DONE: {total} document(s) processed ===")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf-dir", default="documents")
    args = parser.parse_args()
    run(args.pdf_dir)
