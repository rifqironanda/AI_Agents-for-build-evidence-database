import hashlib
from app.models import Source, ResearchTask
from app.agents.search_agent import search

DEMO = [
    {
        "title": "Quantum computing and the financial system",
        "publisher": "BIS",
        "source_type": "institutional_report",
        "url": "https://www.bis.org/",
        "publication_date": "2024",
        "jurisdiction": "International",
    },
    {
        "title": "Post-Quantum Cryptography Standards",
        "publisher": "NIST",
        "source_type": "standard",
        "url": "https://csrc.nist.gov/projects/post-quantum-cryptography",
        "publication_date": "2024",
        "jurisdiction": "United States",
    },
]


def discover(task: ResearchTask):
    try:
        results = search(task.query, max_results=5)
        if results:
            return [
                Source(
                    source_id="SRC-" + hashlib.sha1(x["url"].encode()).hexdigest()[:10],
                    title=x["title"],
                    publisher=x["domain"],
                    source_type="web_search_result",
                    url=x["url"],
                    jurisdiction=task.jurisdiction,
                )
                for x in results
            ]
    except Exception:
        pass

    return [
        Source(
            source_id="SRC-" + hashlib.sha1(x["url"].encode()).hexdigest()[:10],
            **x,
        )
        for x in DEMO
    ]
