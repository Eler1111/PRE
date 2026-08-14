"""Screenplay import adapters.

The original file is copied into the project's ``Script/`` folder and never
touched again. Everything downstream reads the preserved copy.

For text formats ``raw_text`` is the file's own content. For container
formats — PDF, DOCX, Celtx — it is the best textual representation that
could be extracted; the authoritative original stays on disk.
"""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from .celtx import CeltxImporter
from .docx import DocxImporter
from .fdx import FdxImporter
from .fountain import FountainImporter
from .pdf import PdfImporter
from .text import TextImporter


class ScriptImporter(Protocol):
    """Reads one screenplay format into raw and normalized text."""

    format_name: str
    extensions: tuple[str, ...]

    def can_import(self, path: Path) -> bool: ...

    def read(self, path: Path) -> tuple[str, str]:
        """Return ``(raw_text, normalized_text)``."""


# Ordered by how reliably the format preserves screenplay structure.
_IMPORTERS: list[ScriptImporter] = [
    FountainImporter(),
    FdxImporter(),
    CeltxImporter(),
    TextImporter(),
    DocxImporter(),
    PdfImporter(),
]


def supported_extensions() -> list[str]:
    return sorted({ext for importer in _IMPORTERS for ext in importer.extensions})


def importer_for(path: Path) -> ScriptImporter:
    """Pick the importer for ``path``.

    Formats PRE cannot read raise rather than being silently coerced — a
    half-parsed screenplay is worse than a clear refusal.
    """
    for importer in _IMPORTERS:
        if importer.can_import(path):
            return importer

    hint = ""
    if path.suffix.lower() == ".doc":
        hint = " Zapisz dokument jako .docx i spróbuj ponownie."
    elif path.suffix.lower() in (".rtf", ".pages", ".odt"):
        hint = " Wyeksportuj scenariusz do .docx, .pdf lub .fountain."

    raise ValueError(
        f"Nieobsługiwany format scenariusza: {path.suffix or path.name}. "
        f"Obsługiwane formaty: {', '.join(supported_extensions())}.{hint}"
    )


def extract_title(format_name: str, raw_text: str, normalized_text: str) -> str | None:
    """Read the screenplay title, where the format records one."""
    if format_name == "FOUNTAIN":
        from .fountain import extract_title as fountain_title

        return fountain_title(normalized_text)
    if format_name == "FDX":
        from .fdx import extract_title as fdx_title

        return fdx_title(raw_text)
    return None


__all__ = [
    "ScriptImporter",
    "CeltxImporter",
    "DocxImporter",
    "FdxImporter",
    "FountainImporter",
    "PdfImporter",
    "TextImporter",
    "importer_for",
    "supported_extensions",
    "extract_title",
]
