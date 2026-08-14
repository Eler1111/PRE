"""Plain-text screenplay import."""

from __future__ import annotations

import re
from pathlib import Path


class TextImporter:
    format_name = "TXT"
    extensions = (".txt",)

    def can_import(self, path: Path) -> bool:
        return path.suffix.lower() in self.extensions

    def read(self, path: Path) -> tuple[str, str]:
        raw_text = path.read_text(encoding="utf-8")
        return raw_text, normalize_text(raw_text)


def normalize_text(raw_text: str) -> str:
    """Normalize line endings and trailing whitespace only.

    Normalization must never change what the screenplay says: no
    re-wrapping, no case changes, no reformatting of headings. Offsets into
    the normalized text stay meaningful as evidence.
    """
    text = raw_text.replace("\r\n", "\n").replace("\r", "\n")
    text = "\n".join(line.rstrip() for line in text.split("\n"))
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip("\n") + "\n"
