"""Creating and opening a PRE project on disk.

A project is a folder (``Nazwa.pre``) holding project.db plus the media
directories. Its location is the user's choice — internal disk, external
drive, or a synced folder such as iCloud Drive (D-010).
"""

from __future__ import annotations

import os
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .db.connection import close_database, create_database, open_database
from .ids import new_id

PROJECT_SUFFIX = ".pre"
DB_FILENAME = "project.db"
LOCK_FILENAME = ".pre.lock"

PROJECT_DIRECTORIES = (
    "Script",
    "Assets",
    "References",
    "States",
    "Diagrams",
    "Shots",
    "Takes",
    "Audio",
    "Video",
    "Animatic",
    "Exports",
)

# Folder names used by the common sync clients. Matched case-insensitively
# against the project path's components.
_SYNC_FOLDER_MARKERS = (
    "com~apple~clouddocs",
    "mobile documents",
    "icloud drive",
    "icloud~",
    "dropbox",
    "google drive",
    "googledrive",
    "onedrive",
    "pcloud",
    "yandex.disk",
    "mega",
)


class ProjectLockedError(RuntimeError):
    """The project is already open, possibly on another machine."""


@dataclass(frozen=True)
class SyncWarning:
    """A project folder that looks like it is inside a sync client."""

    marker: str
    message: str


def detect_sync_folder(path: Path) -> SyncWarning | None:
    """Return a warning if ``path`` looks like it sits inside a sync folder.

    A live SQLite database in a synced folder can be copied mid-write, so
    the user is told in Polish rather than left to discover a corrupt
    project later. Media files there are fine; the database is the risk.
    """
    parts = [part.lower() for part in path.resolve().parts]
    for marker in _SYNC_FOLDER_MARKERS:
        if any(marker in part for part in parts):
            return SyncWarning(
                marker=marker,
                message=(
                    "Uwaga: projekt znajduje się w folderze synchronizowanym "
                    "w chmurze. Pliki wideo i obrazy są tam bezpieczne, ale "
                    "baza projektu może zostać uszkodzona, jeśli otworzysz "
                    "ten projekt na dwóch komputerach jednocześnie. PRE "
                    "pilnuje tego blokadą, ale zamykaj projekt przed "
                    "przejściem na inny komputer."
                ),
            )
    return None


class Project:
    """An open PRE project: its folder, its database and its lock."""

    def __init__(self, path: Path, connection: sqlite3.Connection, project_id: str):
        self.path = path
        self.connection = connection
        self.id = project_id
        self._lock_path = path / LOCK_FILENAME

    # ------------------------------------------------------------ lifecycle

    @classmethod
    def create(cls, path: Path, name: str, *, story_goal: str | None = None) -> "Project":
        """Create a new project folder and database at ``path``."""
        path = Path(path)
        if path.suffix != PROJECT_SUFFIX:
            path = path.with_name(path.name + PROJECT_SUFFIX)
        if path.exists():
            raise FileExistsError(f"Folder projektu już istnieje: {path}")

        path.mkdir(parents=True)
        for directory in PROJECT_DIRECTORIES:
            (path / directory).mkdir()

        connection = create_database(path / DB_FILENAME)
        project_id = new_id("proj")
        connection.execute(
            "INSERT INTO project (id, name, story_goal, created_at) "
            "VALUES (?, ?, ?, ?)",
            (project_id, name, story_goal, datetime.now(timezone.utc).isoformat()),
        )
        connection.commit()

        project = cls(path, connection, project_id)
        project._acquire_lock()
        return project

    @classmethod
    def open(cls, path: Path) -> "Project":
        """Open an existing project folder."""
        path = Path(path)
        db_path = path / DB_FILENAME
        if not db_path.exists():
            raise FileNotFoundError(f"To nie jest projekt PRE: {path}")

        lock_path = path / LOCK_FILENAME
        if lock_path.exists():
            raise ProjectLockedError(
                f"Projekt jest już otwarty ({lock_path.read_text(encoding='utf-8').strip()}). "
                "Jeśli poprzednia sesja zakończyła się awaryjnie, usuń plik "
                f"{LOCK_FILENAME} z folderu projektu."
            )

        connection = open_database(db_path)
        row = connection.execute("SELECT id FROM project LIMIT 1").fetchone()
        if row is None:
            connection.close()
            raise RuntimeError(f"Projekt bez rekordu projektu: {path}")

        project = cls(path, connection, row["id"])
        project._acquire_lock()
        return project

    def close(self) -> None:
        close_database(self.connection)
        self._release_lock()

    def __enter__(self) -> "Project":
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    # ---------------------------------------------------------------- locks

    def _acquire_lock(self) -> None:
        # Exclusive create, so two processes cannot both believe they own it.
        try:
            fd = os.open(self._lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError as exc:
            raise ProjectLockedError(f"Projekt jest już otwarty: {self.path}") from exc
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(
                f"host={os.uname().nodename} pid={os.getpid()} "
                f"opened_at={datetime.now(timezone.utc).isoformat()}\n"
            )

    def _release_lock(self) -> None:
        self._lock_path.unlink(missing_ok=True)

    # ------------------------------------------------------------ accessors

    @property
    def script_dir(self) -> Path:
        return self.path / "Script"

    def sync_warning(self) -> SyncWarning | None:
        return detect_sync_folder(self.path)
