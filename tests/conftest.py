from __future__ import annotations

from pathlib import Path

import pytest

from pre.analysis import import_screenplay
from pre.project import Project

FIXTURE = Path(__file__).resolve().parent.parent / "fixtures" / "synthetic_pl.fountain"


@pytest.fixture
def project(tmp_path: Path):
    project = Project.create(tmp_path / "Test", name="Test")
    try:
        yield project
    finally:
        try:
            project.close()
        except Exception:
            pass


@pytest.fixture
def analysed(project):
    """A project with the synthetic screenplay imported and analysed."""
    result = import_screenplay(project, FIXTURE)
    return project, result
