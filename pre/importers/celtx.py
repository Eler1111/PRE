"""Celtx (.celtx) import.

A .celtx file is a ZIP container holding the script as HTML, where each
paragraph carries its screenplay class — ``sceneheading``, ``character``,
``dialog`` and so on. Exported Celtx HTML uses the same classes, so both
are read by the same parser.
"""

from __future__ import annotations

import zipfile
from html.parser import HTMLParser
from pathlib import Path

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

_CLASSES = {
    "sceneheading": HEADING,
    "scene-heading": HEADING,
    "slug": HEADING,
    "action": ACTION,
    "character": CHARACTER,
    "dialog": DIALOGUE,
    "dialogue": DIALOGUE,
    "parenthetical": PARENTHETICAL,
    "paren": PARENTHETICAL,
    "transition": TRANSITION,
    "shot": ACTION,
}


class _ScriptHtmlParser(HTMLParser):
    """Collect classed paragraphs from Celtx script HTML."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.paragraphs: list[tuple[str, str]] = []
        self._kind: str | None = None
        self._buffer: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "br" and self._kind is not None:
            self._buffer.append(" ")
            return
        if tag not in ("p", "div"):
            return
        classes = dict(attrs).get("class") or ""
        for token in classes.replace(",", " ").split():
            kind = _CLASSES.get(token.lower())
            if kind:
                self._flush()
                self._kind = kind
                return

    def handle_endtag(self, tag: str) -> None:
        if tag in ("p", "div"):
            self._flush()

    def handle_data(self, data: str) -> None:
        if self._kind is not None:
            self._buffer.append(data)

    def _flush(self) -> None:
        if self._kind is None:
            return
        text = " ".join("".join(self._buffer).split())
        if text:
            self.paragraphs.append((self._kind, text))
        self._kind = None
        self._buffer = []

    def close(self) -> None:  # noqa: D102
        super().close()
        self._flush()


class CeltxImporter:
    format_name = "CELTX"
    extensions = (".celtx",)

    def can_import(self, path: Path) -> bool:
        return path.suffix.lower() in self.extensions

    def read(self, path: Path) -> tuple[str, str]:
        html = _read_script_html(path)
        parser = _ScriptHtmlParser()
        parser.feed(html)
        parser.close()

        if not parser.paragraphs:
            raise ValueError(
                f"Nie znaleziono tekstu scenariusza w pliku Celtx: {path.name}. "
                "Jeśli projekt zawiera kilka dokumentów, wyeksportuj sam scenariusz."
            )

        return html, render_fountain(parser.paragraphs)


def _read_script_html(path: Path) -> str:
    """Pull the script HTML out of the container, or read it directly."""
    if not zipfile.is_zipfile(path):
        # An exported Celtx HTML file, saved with a .celtx extension.
        return path.read_text(encoding="utf-8", errors="replace")

    with zipfile.ZipFile(path) as archive:
        candidates = [
            name
            for name in archive.namelist()
            if name.lower().endswith((".html", ".htm"))
        ]
        if not candidates:
            raise ValueError(
                f"Plik Celtx nie zawiera dokumentu scenariusza: {path.name}"
            )
        # A project can hold several documents; the script is the longest.
        best = max(candidates, key=lambda name: archive.getinfo(name).file_size)
        return archive.read(best).decode("utf-8", errors="replace")
