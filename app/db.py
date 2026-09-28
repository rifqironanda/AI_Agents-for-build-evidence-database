import os
import sqlite3

DB_PATH = os.path.join("data", "evidence.db")


def get_conn():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS documents(
            document_id TEXT PRIMARY KEY,
            filename TEXT NOT NULL,
            path TEXT NOT NULL,
            page_count INTEGER NOT NULL,
            file_hash TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS page_text(
            document_id TEXT NOT NULL,
            page_number INTEGER NOT NULL,
            text TEXT NOT NULL,
            PRIMARY KEY(document_id, page_number),
            FOREIGN KEY(document_id) REFERENCES documents(document_id)
        );

        CREATE TABLE IF NOT EXISTS summaries(
            document_id TEXT PRIMARY KEY,
            summary TEXT NOT NULL,
            key_points TEXT NOT NULL,
            limitations TEXT NOT NULL,
            model TEXT NOT NULL,
            FOREIGN KEY(document_id) REFERENCES documents(document_id)
        );

        CREATE TABLE IF NOT EXISTS validations(
            document_id TEXT PRIMARY KEY,
            status TEXT NOT NULL DEFAULT 'pending',
            notes TEXT,
            FOREIGN KEY(document_id) REFERENCES documents(document_id)
        );
        """
    )
    conn.commit()
    conn.close()


def save_document(document):
    conn = get_conn()
    conn.execute(
        "INSERT OR REPLACE INTO documents VALUES(?,?,?,?,?)",
        (
            document.document_id,
            document.filename,
            document.path,
            document.page_count,
            document.file_hash,
        ),
    )
    conn.commit()
    conn.close()


def save_pages(pages):
    conn = get_conn()
    conn.executemany(
        "INSERT OR REPLACE INTO page_text VALUES(?,?,?)",
        [(p.document_id, p.page_number, p.text) for p in pages],
    )
    conn.commit()
    conn.close()


def save_summary(summary):
    import json

    conn = get_conn()
    conn.execute(
        "INSERT OR REPLACE INTO summaries VALUES(?,?,?,?,?)",
        (
            summary.document_id,
            summary.summary,
            json.dumps(summary.key_points, ensure_ascii=False),
            summary.limitations,
            summary.model,
        ),
    )
    conn.execute(
        "INSERT OR IGNORE INTO validations(document_id, status) VALUES(?, 'pending')",
        (summary.document_id,),
    )
    conn.commit()
    conn.close()
