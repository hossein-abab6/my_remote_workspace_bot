from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterator

from .paths import database_path


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


@contextmanager
def connection() -> Iterator[sqlite3.Connection]:
    db = sqlite3.connect(database_path())
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    try:
        yield db
        db.commit()
    finally:
        db.close()


def initialize_database() -> None:
    with connection() as db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS user_state (
                user_id INTEGER PRIMARY KEY,
                active_project_path TEXT,
                active_session_id INTEGER,
                selected_mode TEXT,
                pending_action TEXT,
                pending_path TEXT,
                language TEXT,
                selected_agent_provider TEXT,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                project_path TEXT NOT NULL,
                provider TEXT NOT NULL,
                external_session_id TEXT,
                title TEXT NOT NULL,
                mode TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE UNIQUE INDEX IF NOT EXISTS idx_session_external
            ON sessions(user_id, provider, external_session_id)
            WHERE external_session_id IS NOT NULL;

            CREATE INDEX IF NOT EXISTS idx_session_project
            ON sessions(user_id, project_path, provider, updated_at DESC);

            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(session_id) REFERENCES sessions(id) ON DELETE CASCADE
            );
            """
        )
        for column in ("language TEXT", "selected_agent_provider TEXT"):
            try:
                db.execute(f"ALTER TABLE user_state ADD COLUMN {column}")
            except sqlite3.OperationalError:
                pass


def get_state(user_id: int) -> dict:
    with connection() as db:
        row = db.execute("SELECT * FROM user_state WHERE user_id = ?", (user_id,)).fetchone()
    return dict(row) if row else {
        "user_id": user_id,
        "active_project_path": None,
        "active_session_id": None,
        "selected_mode": None,
        "pending_action": None,
        "pending_path": None,
        "language": None,
        "selected_agent_provider": None,
    }


def update_state(user_id: int, **fields: object) -> None:
    allowed = {
        "active_project_path", "active_session_id", "selected_mode", "pending_action", "pending_path",
        "language", "selected_agent_provider",
    }
    clean = {key: value for key, value in fields.items() if key in allowed}
    current = get_state(user_id)
    current.update(clean)
    with connection() as db:
        db.execute(
            """
            INSERT INTO user_state(
                user_id, active_project_path, active_session_id, selected_mode,
                pending_action, pending_path, language, selected_agent_provider, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                active_project_path=excluded.active_project_path,
                active_session_id=excluded.active_session_id,
                selected_mode=excluded.selected_mode,
                pending_action=excluded.pending_action,
                pending_path=excluded.pending_path,
                language=excluded.language,
                selected_agent_provider=excluded.selected_agent_provider,
                updated_at=excluded.updated_at
            """,
            (
                user_id,
                current.get("active_project_path"),
                current.get("active_session_id"),
                current.get("selected_mode"),
                current.get("pending_action"),
                current.get("pending_path"),
                current.get("language"),
                current.get("selected_agent_provider"),
                utc_now(),
            ),
        )


def create_session(
    user_id: int,
    project_path: str,
    provider: str,
    title: str,
    mode: str,
    external_session_id: str | None = None,
) -> int:
    now = utc_now()
    with connection() as db:
        cursor = db.execute(
            """
            INSERT INTO sessions(
                user_id, project_path, provider, external_session_id, title, mode, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, project_path, provider, external_session_id, title, mode, now, now),
        )
        return int(cursor.lastrowid)


def set_external_session_id(session_id: int, external_session_id: str) -> None:
    with connection() as db:
        db.execute(
            "UPDATE sessions SET external_session_id=?, updated_at=? WHERE id=?",
            (external_session_id, utc_now(), session_id),
        )


def get_session(session_id: int) -> dict | None:
    with connection() as db:
        row = db.execute("SELECT * FROM sessions WHERE id=?", (session_id,)).fetchone()
    return dict(row) if row else None


def list_sessions(user_id: int, project_path: str, provider: str) -> list[dict]:
    with connection() as db:
        rows = db.execute(
            """
            SELECT * FROM sessions
            WHERE user_id=? AND project_path=? AND provider=?
            ORDER BY updated_at DESC
            """,
            (user_id, project_path, provider),
        ).fetchall()
    return [dict(row) for row in rows]


def add_message(session_id: int, role: str, content: str) -> None:
    now = utc_now()
    with connection() as db:
        db.execute(
            "INSERT INTO messages(session_id, role, content, created_at) VALUES (?, ?, ?, ?)",
            (session_id, role, content, now),
        )
        db.execute("UPDATE sessions SET updated_at=? WHERE id=?", (now, session_id))


def list_messages(session_id: int) -> list[dict]:
    with connection() as db:
        rows = db.execute(
            "SELECT * FROM messages WHERE session_id=? ORDER BY id ASC", (session_id,)
        ).fetchall()
    return [dict(row) for row in rows]


def find_session_by_external(user_id: int, provider: str, external_session_id: str) -> dict | None:
    with connection() as db:
        row = db.execute(
            "SELECT * FROM sessions WHERE user_id=? AND provider=? AND external_session_id=?",
            (user_id, provider, external_session_id),
        ).fetchone()
    return dict(row) if row else None


def update_session_title(session_id: int, title: str) -> None:
    with connection() as db:
        db.execute(
            "UPDATE sessions SET title=?, updated_at=? WHERE id=?",
            (title, utc_now(), session_id),
        )


def session_message_count(session_id: int) -> int:
    with connection() as db:
        row = db.execute(
            "SELECT COUNT(*) AS count FROM messages WHERE session_id=?", (session_id,)
        ).fetchone()
    return int(row["count"])
