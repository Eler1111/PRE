"""Project persistence: the film model must survive a restart."""

from __future__ import annotations

from pathlib import Path

import pytest

from pre.analysis import import_screenplay
from pre.db.connection import SCHEMA_VERSION
from pre.project import DB_FILENAME, PROJECT_DIRECTORIES, Project, ProjectLockedError
from pre.project import detect_sync_folder
from pre.queries import list_scenes

FIXTURE = Path(__file__).resolve().parent.parent / "fixtures" / "synthetic_pl.fountain"


def test_create_builds_the_project_folder(tmp_path):
    with Project.create(tmp_path / "Film", name="Film") as project:
        assert project.path.name == "Film.pre"
        assert (project.path / DB_FILENAME).exists()
        for directory in PROJECT_DIRECTORIES:
            assert (project.path / directory).is_dir()


def test_create_does_not_fabricate_placeholder_media(tmp_path):
    with Project.create(tmp_path / "Film", name="Film") as project:
        for directory in PROJECT_DIRECTORIES:
            assert list((project.path / directory).iterdir()) == []


def test_project_state_survives_a_restart(tmp_path):
    project = Project.create(tmp_path / "Film", name="Film")
    import_screenplay(project, FIXTURE)
    before = [scene["heading_raw"] for scene in list_scenes(project)]
    project.close()

    reopened = Project.open(tmp_path / "Film.pre")
    try:
        after = [scene["heading_raw"] for scene in list_scenes(reopened)]
    finally:
        reopened.close()

    assert before == after
    assert before, "analiza nie zapisała żadnych scen"


def test_second_open_is_refused_while_the_project_is_open(tmp_path):
    project = Project.create(tmp_path / "Film", name="Film")
    try:
        with pytest.raises(ProjectLockedError):
            Project.open(project.path)
    finally:
        project.close()


def test_lock_is_released_on_close(tmp_path):
    project = Project.create(tmp_path / "Film", name="Film")
    project.close()
    reopened = Project.open(tmp_path / "Film.pre")
    reopened.close()


def test_close_leaves_no_stray_write_ahead_log(tmp_path):
    """A synced folder must not receive a half-written database."""
    project = Project.create(tmp_path / "Film", name="Film")
    import_screenplay(project, FIXTURE)
    project.close()

    wal = tmp_path / "Film.pre" / f"{DB_FILENAME}-wal"
    assert not wal.exists() or wal.stat().st_size == 0


def test_schema_version_is_recorded(tmp_path):
    with Project.create(tmp_path / "Film", name="Film") as project:
        row = project.connection.execute(
            "SELECT version FROM schema_version"
        ).fetchone()
        assert row["version"] == SCHEMA_VERSION


@pytest.mark.parametrize(
    "path",
    [
        "/Users/x/Library/Mobile Documents/com~apple~CloudDocs/Film.pre",
        "/Users/x/Dropbox/Film.pre",
        "/Users/x/Google Drive/Film.pre",
    ],
)
def test_warns_about_synced_folders(path):
    warning = detect_sync_folder(Path(path))
    assert warning is not None
    assert "synchronizowanym" in warning.message


def test_ordinary_folder_produces_no_warning(tmp_path):
    assert detect_sync_folder(tmp_path) is None
