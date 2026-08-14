"""Word (.docx) import.

A .docx is a ZIP holding ``word/document.xml``. Word documents rarely carry
reliable screenplay styles, so paragraphs are extracted as text and the
usual screenplay conventions — a capitalised heading, a capitalised cue
above its dialogue — do the rest.

Where a document does carry Final Draft-style paragraph styles, they are
used instead of guessing.
"""

from __future__ import annotations

import zipfile
from pathlib import Path
from xml.etree import ElementTree

from .structured import (
    ACTION,
    CHARACTER,
    DIALOGUE,
    HEADING,
    PARENTHETICAL,
    TRANSITION,
    classify_by_convention,
    render_fountain,
)

_W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

_STYLE_NAMES = {
    "sceneheading": HEADING,
    "scene-heading": HEADING,
    "sceneheader": HEADING,
    "slugline": HEADING,
    "action": ACTION,
    "character": CHARACTER,
    "dialogue": DIALOGUE,
    "dialog": DIALOGUE,
    "parenthetical": PARENTHETICAL,
    "transition": TRANSITION,
}


class DocxImporter:
    format_name = "DOCX"
    extensions = (".docx",)

    def can_import(self, path: Path) -> bool:
        return path.suffix.lower() in self.extensions

    def read(self, path: Path) -> tuple[str, str]:
        if not zipfile.is_zipfile(path):
            raise ValueError(
                f"Plik nie jest dokumentem Word: {path.name}. "
                "Starszy format .doc nie jest obsługiwany — zapisz jako .docx."
            )

        with zipfile.ZipFile(path) as archive:
            try:
                document = archive.read("word/document.xml")
            except KeyError as exc:
                raise ValueError(
                    f"Dokument Word nie zawiera treści: {path.name}"
                ) from exc

        paragraphs = _read_paragraphs(document)
        if not paragraphs:
            raise ValueError(f"Dokument Word jest pusty: {path.name}")

        text = "\n\n".join(body for _, body in paragraphs)
        if any(kind != ACTION for kind, _ in paragraphs):
            # The document carries real screenplay styles, so trust them.
            return text, render_fountain(paragraphs)

        # No styles at all — a screenplay typed straight into Word. The
        # conventions are all that is left to read it by.
        return text, render_fountain(classify_by_convention([body for _, body in paragraphs]))


def _read_paragraphs(document: bytes) -> list[tuple[str, str]]:
    root = ElementTree.fromstring(document)
    paragraphs: list[tuple[str, str]] = []

    for node in root.iter(f"{_W}p"):
        text = "".join(run.text or "" for run in node.iter(f"{_W}t")).strip()
        # A tab-only or empty paragraph is layout, not content.
        if not text:
            continue

        kind = ACTION
        style = node.find(f"{_W}pPr/{_W}pStyle")
        if style is not None:
            key = (style.get(f"{_W}val") or "").replace(" ", "").lower()
            kind = _STYLE_NAMES.get(key, ACTION)

        paragraphs.append((kind, text))

    return paragraphs
