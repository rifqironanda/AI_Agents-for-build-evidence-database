"""Entry point for the first learning version of the evidence agent."""
import sys
from app.agents.discovery import discover
from app.agents.planner import plan
from app.agents.summarizer_agent import summarize
from app.agents.storage_agent import store
from app.db import init_db


def run(query: str):
    print("\n=== AGENT RUN ===")
    print(f"1. USER QUERY\n   {query}")

    init_db()

    print("\n2. PLANNER AGENT")
    tasks = plan(query)
    print(f"   Created {len(tasks)} research task(s)")

    total = 0
    for task in tasks:
        print(f"\n3. SEARCH AGENT\n   Query: {task.query}")
        try:
            sources = discover(task)
        except Exception as exc:
            print(f"   Search failed: {exc}")
            print("   Continuing with no results for this task.")
            sources = []

        print(f"   Found {len(sources)} source(s)")

        for source in sources:
            print(f"\n4. SUMMARIZER AGENT\n   {source.title}")
            summary = summarize(
                {"title": source.title, "url": source.url, "domain": source.publisher},
                task.query,
            )
            print(f"   Summary: {summary['summary']}")

            print("5. STORAGE AGENT")
            store(source, summary)
            print(f"   Saved: {source.source_id}")
            total += 1

    print(f"\n=== DONE: {total} source(s) stored ===\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python -m app.main "your research question"')
        raise SystemExit(1)
    run(" ".join(sys.argv[1:]))
