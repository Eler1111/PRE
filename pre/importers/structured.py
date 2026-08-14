"""Rendering structurally-tagged screenplays into Fountain.

Final Draft and Celtx already know which paragraph is a scene heading and
which is a character cue. Rather than throw that away and re-guess it from
capitalisation, the structure is rendered as Fountain's explicit forcing
syntax — ``.HEADING`` and ``@Cue`` — which the parser reads directly.

Nothing is re-cased or reworded on the way through, and the original file
is preserved on disk regardless.
"""

from __future__ import annotations

HEADING = "heading"
ACTION = "action"
CHARACTER = "character"
DIALOGUE = "dialogue"
PARENTHETICAL = "parenthetical"
TRANSITION = "transition"
OTHER = "other"


def render_fountain(paragraphs: list[tuple[str, str]]) -> str:
    """Turn ``[(kind, text), ...]`` into Fountain source text."""
    lines: list[str] = []
    previous = None

    for kind, text in paragraphs:
        text = text.strip()
        if not text:
            continue

        if kind == HEADING:
            _blank(lines)
            lines.append(f".{text}")
        elif kind == CHARACTER:
            _blank(lines)
            lines.append(f"@{text}")
        elif kind in (DIALOGUE, PARENTHETICAL):
            # Dialogue must sit directly under its cue with no blank line,
            # otherwise it reads as action.
            if previous not in (CHARACTER, PARENTHETICAL, DIALOGUE):
                _blank(lines)
            lines.append(text)
        elif kind == TRANSITION:
            _blank(lines)
            lines.append(text if text.endswith(":") else f"{text}:")
        else:
            _blank(lines)
            lines.append(text)

        previous = kind

    return "\n".join(lines).strip() + "\n"


def _blank(lines: list[str]) -> None:
    if lines and lines[-1] != "":
        lines.append("")


# A cue is short; a capitalised line much longer than this is shouted
# action, a title card, or a chapter break.
_MAX_CUE_LENGTH = 60


def classify_by_convention(texts: list[str]) -> list[tuple[str, str]]:
    """Label paragraphs that carry no styling, using screenplay convention.

    Word documents are frequently typed with no styles at all, leaving only
    the conventions themselves: a heading opens with INT./WN., a cue is a
    short capitalised line, and what follows a cue is speech. Binding those
    together here is what keeps a speech attached to its speaker.
    """
    from ..analysis.screenplay import is_heading

    labelled: list[tuple[str, str]] = []
    previous = None

    for index, text in enumerate(texts):
        text = text.strip()
        if not text:
            continue

        has_next = index + 1 < len(texts) and texts[index + 1].strip()

        if is_heading(text):
            kind = HEADING
        elif text.startswith("(") and previous in (CHARACTER, PARENTHETICAL):
            kind = PARENTHETICAL
        elif previous in (CHARACTER, PARENTHETICAL):
            kind = DIALOGUE
        elif _looks_like_cue(text) and has_next:
            kind = CHARACTER
        else:
            kind = ACTION

        labelled.append((kind, text))
        previous = kind

    return labelled


def _looks_like_cue(text: str) -> bool:
    if len(text) > _MAX_CUE_LENGTH or text.endswith(":"):
        return False
    letters = [character for character in text if character.isalpha()]
    return bool(letters) and all(character.isupper() for character in letters)
