"""Fountain screenplay import.

Fountain is the priority format: it is plain text, so the original survives
import untouched and source offsets stay usable as evidence.
"""

from __future__ import annotations

import re
from pathlib import Path

from .text import normalize_text

# Title-page keys appear as "Key: value" lines before the first scene.
_TITLE_PAGE_KEY = re.compile(
    r"^(title|credit|author|authors|source|draft date|contact|copyright|notes|"
    r"tytuł|tytul|autor|autorzy|scenariusz)\s*:", re.I
)
_BONEYARD = re.compile(r"/\*.*?\*/", re.S)
_NOTE = re.compile(r"\[\[.*?\]\]", re.S)


class FountainImporter:
    format_name = "FOUNTAIN"
    extensions = (".fountain", ".spmd")

    def can_import(self, path: Path) -> bool:
        return path.suffix.lower() in self.extensions

    def read(self, path: Path) -> tuple[str, str]:
        raw_text = path.read_text(encoding="utf-8")
        # Boneyard and notes are author scratch, not screenplay content, so
        # they are dropped from the normalized text but survive in raw_text.
        stripped = _NOTE.sub("", _BONEYARD.sub("", raw_text))
        return raw_text, normalize_text(stripped)


def extract_title(normalized_text: str) -> str | None:
    """Read the title from a Fountain title page, if present."""
    for line in normalized_text.split("\n"):
        if not line.strip():
            break
        match = _TITLE_PAGE_KEY.match(line.strip())
        if match and match.group(1).lower() in {"title", "tytuł", "tytul"}:
            return line.split(":", 1)[1].strip() or None
    return None
