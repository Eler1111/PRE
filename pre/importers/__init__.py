"""Screenplay import adapters.

The original file is copied into the project's ``Script/`` folder and never
touched again. Everything downstream reads the preserved copy.
"""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from .fountain import FountainImporter
from .text import TextImporter


class ScriptImporter(Protocol):
    """Reads one screenplay format into raw and normalized text."""

    format_name: str
    extensions: tuple[str, ...]

    def can_import(self, path: Path) -> bool: ...

    def read(self, path: Path) -> tuple[str, str]:
        """Return ``(raw_text, normalized_text)``."""


_IMPORTERS: list[ScriptImporter] = [FountainImporter(), TextImporter()]


def importer_for(path: Path) -> ScriptImporter:
    """Pick the importer for ``path``.

    Formats PRE cannot read yet raise rather than being silently coerced —
    a half-parsed screenplay is worse than a clear refusal.
    """
    for importer in _IMPORTERS:
        if importer.can_import(path):
            return importer
    raise ValueError(
        f"Nieobsługiwany format scenariusza: {path.suffix or path.name}. "
        f"Obsługiwane formaty: "
        f"{', '.join(sorted({ext for imp in _IMPORTERS for ext in imp.extensions}))}."
    )


__all__ = ["ScriptImporter", "FountainImporter", "TextImporter", "importer_for"]
