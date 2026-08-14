"""Identifier generation.

IDs are procedural work, so the system owns them entirely — the user never
sees or types one. They are readable on purpose (``scene_001``), because
every production log, review flag and prompt file will quote them.
"""

from __future__ import annotations

import sqlite3
import uuid

_SEQUENTIAL_PREFIXES = {
    "scene": "scene",
    "entity": "ent",
    "state": "state",
}


def new_id(prefix: str) -> str:
    """A globally unique id with a readable prefix."""
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def sequential_id(
    connection: sqlite3.Connection,
    table: str,
    prefix: str,
    scope_column: str,
    scope_value: str,
    width: int = 3,
) -> str:
    """A stable, human-readable id numbered within one scope.

    Used where the number carries meaning to a reader — scenes within a
    script, entities within a project. The count is taken from the table
    itself so ids stay dense even across separate analysis runs.
    """
    count = connection.execute(
        f"SELECT COUNT(*) AS n FROM {table} WHERE {scope_column} = ?",
        (scope_value,),
    ).fetchone()["n"]

    while True:
        candidate = f"{prefix}_{count + 1:0{width}d}"
        exists = connection.execute(
            f"SELECT 1 FROM {table} WHERE id = ?", (candidate,)
        ).fetchone()
        if exists is None:
            return candidate
        count += 1
