from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from typing import Iterator

from app.config import AppSettings


@contextmanager
def get_connection(settings: AppSettings) -> Iterator[sqlite3.Connection]:
    settings.database_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(settings.database_path)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()


def check_database(settings: AppSettings) -> dict:
    try:
        with get_connection(settings) as connection:
            connection.execute("SELECT 1").fetchone()
            table_count = connection.execute(
                "SELECT COUNT(*) AS count FROM sqlite_master WHERE type = 'table'"
            ).fetchone()["count"]
    except sqlite3.Error as exc:
        return {"ok": False, "path": str(settings.database_path), "error": str(exc)}

    return {"ok": True, "path": str(settings.database_path), "table_count": table_count}
