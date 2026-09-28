"""Local summarization agent.

Only extracted text is sent to the local Ollama model. Nothing is sent to a
cloud service by this module.
"""

from app.config import OLLAMA_MODEL
from app.llm import llm
from app.models import Summary


def _fallback(document_id: str, text: str) -> Summary:
    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
    points = [s[:400] for s in sentences[:5]]
    return Summary(
        document_id=document_id,
        summary="Local LLM unavailable. Generated a deterministic extractive preview.",
        key_points=points,
        limitations="This is not an AI summary; Ollama was unavailable.",
        model="fallback",
    )


def summarize(document_id: str, filename: str, text: str) -> Summary:
    text = text[:30000]
    if not llm.available():
        return _fallback(document_id, text)

    prompt = f"""
You are a research summarization assistant for a quantum-computing evidence
database.

Document: {filename}

Summarize ONLY the supplied document text. Do not invent facts, dates,
citations, page numbers, or conclusions. Clearly distinguish what the
document states from your interpretation.

Return valid JSON with exactly these keys:
summary: concise paragraph
key_points: array of 3 to 7 factual points
limitations: limitations or missing context

DOCUMENT TEXT:
{text}
"""

    result = llm.json(prompt)
    return Summary(
        document_id=document_id,
        summary=result.get("summary", ""),
        key_points=result.get("key_points", []),
        limitations=result.get("limitations", ""),
        model=OLLAMA_MODEL,
    )
