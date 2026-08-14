"""PDF import.

PDFs carry layout, not structure, so the text layer is extracted and the
usual screenplay conventions do the parsing. Page furniture — page
numbers, CONTINUED and (MORE) markers — is stripped, because left in place
it lands in the middle of scenes and turns into false action lines.

Needs ``pypdf``. It is the only non-standard-library dependency in the
project and is imported lazily, so everything else works without it.
"""

from __future__ import annotations

import re
from pathlib import Path

from .text import normalize_text

# A line holding nothing but a page number, in any of the usual dressings.
_PAGE_NUMBER = re.compile(r"^\s*\(?\d{1,4}[.)]?\s*\)?\s*$")
_CONTINUED = re.compile(
    r"^\s*\(?\s*(CONTINUED|CONT'?D|CIĄG DALSZY|CIAG DALSZY|C\.?D\.?N?\.?)"
    r"\s*:?\s*(\(\d+\))?\s*\)?\s*$",
    re.I,
)
_MORE = re.compile(r"^\s*\(\s*(MORE|WIĘCEJ|WIECEJ)\s*\)\s*$", re.I)

# Below this, the PDF almost certainly has no text layer at all.
_MIN_USABLE_CHARACTERS = 200

# Above this share of blank lines, extraction kept the block structure and
# nothing needs rebuilding.
_STRUCTURED_ENOUGH = 0.10


class PdfImporter:
    format_name = "PDF"
    extensions = (".pdf",)

    def can_import(self, path: Path) -> bool:
        return path.suffix.lower() in self.extensions

    def read(self, path: Path) -> tuple[str, str]:
        reader = _open_pdf(path)
        pages = [page.extract_text() or "" for page in reader.pages]
        raw_text = "\n".join(pages)

        if len(raw_text.strip()) < _MIN_USABLE_CHARACTERS:
            raise ValueError(
                f"PDF nie zawiera warstwy tekstowej: {path.name}. "
                "To prawdopodobnie skan. Rozpoznaj tekst (OCR) albo użyj "
                "wersji scenariusza w formacie Fountain, DOCX lub FDX."
            )

        text = restore_paragraph_breaks(strip_page_furniture(raw_text))
        return raw_text, normalize_text(text)


def _open_pdf(path: Path):
    try:
        from pypdf import PdfReader
    except ImportError as exc:  # pragma: no cover - depends on environment
        raise ValueError(
            "Import PDF wymaga biblioteki pypdf. Zainstaluj ją poleceniem: "
            "pip install pypdf"
        ) from exc

    reader = PdfReader(str(path))
    if reader.is_encrypted:
        try:
            reader.decrypt("")
        except Exception as exc:
            raise ValueError(
                f"PDF jest zabezpieczony hasłem: {path.name}"
            ) from exc
    return reader


def restore_paragraph_breaks(text: str) -> str:
    """Rebuild the blank lines that separate screenplay blocks.

    Extraction often drops vertical space, which matters because a dialogue
    block is bounded by blank lines — without them, everything after a cue
    is swallowed into one speech. Screenplay indentation is enough to
    recover the structure: action and headings sit at the left margin,
    while cues, parentheticals and dialogue are all indented.

    A new block therefore starts at every line back at the left margin, and
    at the first indented line after one. Cue, parenthetical and dialogue
    stay together, which is what binds a speech to its speaker.

    Left alone when the text already has blank lines, or when extraction
    lost the indentation and there is nothing to reason from.
    """
    # Trailing newlines are not structure; counting them would make an
    # unstructured extraction look like a well-separated one.
    lines = text.replace("\r\n", "\n").replace("\r", "\n").strip("\n").split("\n")
    populated = [line for line in lines if line.strip()]
    if not populated:
        return text

    blank_ratio = (len(lines) - len(populated)) / len(lines)
    if blank_ratio >= _STRUCTURED_ENOUGH:
        return text

    indents = {len(line) - len(line.lstrip(" ")) for line in populated}
    if len(indents) < 2:
        return text

    base = min(indents)
    rebuilt: list[str] = []
    previous_indent: int | None = None

    for line in lines:
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        starts_block = indent == base or previous_indent == base
        if starts_block and rebuilt:
            rebuilt.append("")
        rebuilt.append(line)
        previous_indent = indent

    return "\n".join(rebuilt)


def strip_page_furniture(text: str) -> str:
    """Remove page numbers and page-break markers from extracted text.

    A screenplay page break splits dialogue with "(MORE)" and resumes it
    with "CONTINUED:". Both are printing artifacts; keeping them would put
    invented lines inside scenes.
    """
    kept: list[str] = []
    for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        if _PAGE_NUMBER.match(line) or _CONTINUED.match(line) or _MORE.match(line):
            continue
        kept.append(line)
    return "\n".join(kept)
