"""Summarization agent.

The LLM is optional. Without an API key the agent returns a deterministic
metadata summary so the rest of the pipeline can still be tested locally.
"""
from app.llm import llm


SYSTEM = """You summarize web-search results for a research workflow.
Use only the information provided. Do not invent facts.
Return JSON with exactly: summary, relevance, limitations."""


def summarize(result: dict, query: str) -> dict:
    prompt = (
        f"Research query: {query}\n"
        f"Title: {result.get('title','')}\n"
        f"URL: {result.get('url','')}\n"
        f"Domain: {result.get('domain','')}\n"
        "Summarize what can be concluded from this search result metadata only."
    )

    if not llm.enabled:
        return {
            "summary": result.get("title", "Untitled") + " — search result found for the requested topic.",
            "relevance": "Potentially relevant; document content has not been retrieved yet.",
            "limitations": "This MVP has not fetched or verified the source document.",
        }

    return llm.json(SYSTEM, prompt)
