import os
import sqlite3

DB_PATH = os.path.join("data", "evidence.db")


def get_conn():
    os.makedirs("data", exist_ok=True)
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c


def init_db():
    c = get_conn()
    c.executescript(
        """
        CREATE TABLE IF NOT EXISTS sources(
            source_id TEXT PRIMARY KEY,
            title TEXT,
            publisher TEXT,
            publication_date TEXT,
            source_type TEXT,
            url TEXT,
            jurisdiction TEXT
        );

        CREATE TABLE IF NOT EXISTS claims(
            claim_id TEXT PRIMARY KEY,
            source_id TEXT,
            claim_text TEXT,
            claim_type TEXT,
            topic TEXT,
            threat_type TEXT,
            evidence_quote TEXT,
            page_or_section TEXT,
            time_expression TEXT,
            extraction_confidence REAL
        );

        CREATE TABLE IF NOT EXISTS validations(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            claim_id TEXT,
            status TEXT,
            claim_supported INTEGER,
            citation_present INTEGER,
            interpretation_risk TEXT,
            rationale TEXT
        );

        CREATE TABLE IF NOT EXISTS summaries(
            source_id TEXT PRIMARY KEY,
            summary TEXT,
            relevance TEXT,
            limitations TEXT,
            FOREIGN KEY(source_id) REFERENCES sources(source_id)
        );
        """
    )
    c.commit()
    c.close()


def upsert_source(s):
    c = get_conn()
    c.execute(
        "INSERT OR REPLACE INTO sources VALUES(?,?,?,?,?,?,?)",
        (
            s.source_id,
            s.title,
            s.publisher,
            s.publication_date,
            s.source_type,
            s.url,
            s.jurisdiction,
        ),
    )
    c.commit()
    c.close()


def save_summary(source_id, summary):
    c = get_conn()
    c.execute(
        "INSERT OR REPLACE INTO summaries(source_id,summary,relevance,limitations) VALUES(?,?,?,?)",
        (
            source_id,
            summary.get("summary", ""),
            summary.get("relevance", ""),
            summary.get("limitations", ""),
        ),
    )
    c.commit()
    c.close()


def insert_claim(x):
    c = get_conn()
    c.execute(
        "INSERT OR REPLACE INTO claims VALUES(?,?,?,?,?,?,?,?,?,?)",
        (
            x.claim_id,
            x.source_id,
            x.claim_text,
            x.claim_type,
            x.topic,
            x.threat_type,
            x.evidence_quote,
            x.page_or_section,
            x.time_expression,
            x.extraction_confidence,
        ),
    )
    c.commit()
    c.close()


def insert_validation(v):
    c = get_conn()
    c.execute(
        "INSERT INTO validations(claim_id,status,claim_supported,citation_present,interpretation_risk,rationale) VALUES(?,?,?,?,?,?)",
        (
            v.claim_id,
            v.status,
            int(v.claim_supported),
            int(v.citation_present),
            v.interpretation_risk,
            v.rationale,
        ),
    )
    c.commit()
    c.close()
