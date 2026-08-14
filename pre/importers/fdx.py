"""Final Draft (.fdx) import.

FDX is XML with the paragraph types already labelled, so the structure is
read rather than inferred.
"""

from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree

from .structured import (
    ACTION,
    CHARACTER,
    DIALOGUE,
    HEADING,
    OTHER,
    PARENTHETICAL,
    TRANSITION,
    render_fountain,
)

_PARAGRAPH_TYPES = {
    "Scene Heading": HEADING,
    "Action": ACTION,
    "Character": CHARACTER,
    "Dialogue": DIALOGUE,
    "Parenthetical": PARENTHETICAL,
    "Transition": TRANSITION,
    "Shot": ACTION,
    "General": ACTION,
}

# Structural noise Final Draft writes at page breaks.
_PAGE_BREAK_MARKERS = {"(MORE)", "(CIĄG DALSZY)", "(CIAG DALSZY)"}


class FdxImporter:
    format_name = "FDX"
    extensions = (".fdx",)

    def can_import(self, path: Path) -> bool:
        return path.suffix.lower() in self.extensions

    def read(self, path: Path) -> tuple[str, str]:
        raw_text = path.read_text(encoding="utf-8", errors="replace")
        try:
            root = ElementTree.fromstring(raw_text)
        except ElementTree.ParseError as exc:
            raise ValueError(
                f"Nie udało się odczytać pliku Final Draft: {path.name} ({exc})"
            ) from exc

        paragraphs: list[tuple[str, str]] = []
        for paragraph in root.iter("Paragraph"):
            kind = _PARAGRAPH_TYPES.get(paragraph.get("Type", ""), OTHER)
            text = "".join(node.text or "" for node in paragraph.iter("Text")).strip()
            if not text or text.upper() in _PAGE_BREAK_MARKERS:
                continue
            paragraphs.append((kind, text))

        if not paragraphs:
            raise ValueError(f"Plik Final Draft nie zawiera tekstu scenariusza: {path.name}")

        return raw_text, render_fountain(paragraphs)


def extract_title(raw_text: str) -> str | None:
    """Read the title from the FDX title page, if it has one."""
    try:
        root = ElementTree.fromstring(raw_text)
    except ElementTree.ParseError:
        return None

    title_page = root.find("TitlePage")
    if title_page is None:
        return None
    for paragraph in title_page.iter("Paragraph"):
        text = "".join(node.text or "" for node in paragraph.iter("Text")).strip()
        if text:
            return text
    return None
