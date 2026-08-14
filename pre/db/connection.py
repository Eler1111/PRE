"""Opening, creating and safely closing a project database.

The database may live inside a synced folder (iCloud Drive, Dropbox), which
is a known corruption risk: the sync client can copy the database and its
write-ahead log out of order. D-010 answers this with a lock file, a clean
checkpoint on close, and a warning when the folder looks synced.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

SCHEMA_VERSION = 1

_SCHEMA_PATH = Path(__file__).parent / "schema.sql"
_SEED_PATH = Path(__file__).parent / "seed.sql"


def _configure(connection: sqlite3.Connection) -> None:
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    # WAL keeps readers from blocking the analysis pass. It costs an extra
    # -wal file, which is exactly why close_database() checkpoints it away.
    connection.execute("PRAGMA journal_mode = WAL")
    connection.execute("PRAGMA synchronous = FULL")


def create_database(path: Path) -> sqlite3.Connection:
    """Create a new project.db at ``path`` and apply the schema."""
    if path.exists():
        raise FileExistsError(f"Baza danych już istnieje: {path}")

    connection = sqlite3.connect(path)
    _configure(connection)
    connection.executescript(_SCHEMA_PATH.read_text(encoding="utf-8"))
    connection.executescript(_SEED_PATH.read_text(encoding="utf-8"))
    connection.execute(
        "INSERT INTO schema_version (version, applied_at) VALUES (?, ?)",
        (SCHEMA_VERSION, datetime.now(timezone.utc).isoformat()),
    )
    connection.commit()
    return connection


def open_database(path: Path) -> sqlite3.Connection:
    """Open an existing project.db."""
    if not path.exists():
        raise FileNotFoundError(f"Nie znaleziono bazy danych: {path}")

    connection = sqlite3.connect(path)
    _configure(connection)

    row = connection.execute(
        "SELECT version FROM schema_version ORDER BY version DESC LIMIT 1"
    ).fetchone()
    if row is None:
        raise RuntimeError(f"Baza danych bez wersji schematu: {path}")
    if row["version"] > SCHEMA_VERSION:
        raise RuntimeError(
            f"Projekt używa nowszej wersji schematu ({row['version']}) "
            f"niż ta wersja PRE ({SCHEMA_VERSION})."
        )
    return connection


def close_database(connection: sqlite3.Connection) -> None:
    """Commit, fold the write-ahead log back in, and close.

    The checkpoint matters on synced folders: it leaves project.db as a
    single consistent file with nothing important left in -wal.
    """
    try:
        connection.commit()
        connection.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    finally:
        connection.close()
