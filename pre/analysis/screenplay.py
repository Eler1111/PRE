"""Deterministic screenplay parsing.

Everything here is code's responsibility, never the model's: scene
boundaries, script order, headings, dialogue attribution and source
offsets. Semantic work — what a state event means, whether two names are
the same person — belongs to the analysis pass that runs after this one.

Both Polish and English screenplay conventions are recognised, since the
project's dialogue language is Polish by default.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

# ---------------------------------------------------------------- headings

INT = "INT"
EXT = "EXT"
INT_EXT = "INT/EXT"

_INT_EXT_TOKENS = {
    "INT": INT,
    "INTERIOR": INT,
    "WN": INT,
    "WNĘTRZE": INT,
    "WNETRZE": INT,
    "EXT": EXT,
    "EXTERIOR": EXT,
    "EST": EXT,
    "PL": EXT,
    "PLENER": EXT,
    "ZEW": EXT,
    "ZEWNĘTRZE": EXT,
    "ZEWNETRZE": EXT,
    "INT/EXT": INT_EXT,
    "EXT/INT": INT_EXT,
    "I/E": INT_EXT,
    "E/I": INT_EXT,
    "WN/PL": INT_EXT,
    "PL/WN": INT_EXT,
}

_TIME_OF_DAY = {
    "DAY": "DAY",
    "DZIEŃ": "DAY",
    "DZIEN": "DAY",
    "NIGHT": "NIGHT",
    "NOC": "NIGHT",
    "NOCĄ": "NIGHT",
    "MORNING": "MORNING",
    "RANO": "MORNING",
    "RANEK": "MORNING",
    "PORANEK": "MORNING",
    "EVENING": "EVENING",
    "WIECZÓR": "EVENING",
    "WIECZOR": "EVENING",
    "WIECZOREM": "EVENING",
    "DAWN": "DAWN",
    "ŚWIT": "DAWN",
    "SWIT": "DAWN",
    "DUSK": "DUSK",
    "ZMIERZCH": "DUSK",
    "ZMROK": "DUSK",
    "AFTERNOON": "AFTERNOON",
    "POPOŁUDNIE": "AFTERNOON",
    "POPOLUDNIE": "AFTERNOON",
    "NOON": "NOON",
    "POŁUDNIE": "NOON",
    "CONTINUOUS": "CONTINUOUS",
    "CIĄG DALSZY": "CONTINUOUS",
    "LATER": "LATER",
    "PÓŹNIEJ": "LATER",
    "POZNIEJ": "LATER",
}

# Chronology markers explicit enough to be read as FACT rather than guessed.
_CHRONOLOGY_MARKERS = {
    "FLASHBACK": "FLASHBACK",
    "RETROSPEKCJA": "FLASHBACK",
    "RETROSPEKCJI": "FLASHBACK",
    "FLASHFORWARD": "FLASHFORWARD",
    "FLASH FORWARD": "FLASHFORWARD",
    "ANTYCYPACJA": "FLASHFORWARD",
    "DREAM": "DREAM",
    "SEN": "DREAM",
    "SNU": "DREAM",
    "IMAGINED": "IMAGINED",
    "WYOBRAŻENIE": "IMAGINED",
    "WYOBRAZENIE": "IMAGINED",
}

_SEPARATORS = re.compile(r"\s+[-–—]\s+|\s+[-–—]$")
_SCENE_NUMBER_PREFIX = re.compile(r"^\s*(?:SCENA|SCENE|SC\.?)?\s*(\d+[A-Z]?)[.)]?\s+", re.I)
_SCENE_NUMBER_SUFFIX = re.compile(r"\s+#?(\d+[A-Z]?)#?\s*$")
_TRANSITION = re.compile(
    r"^(?:CUT TO|DISSOLVE TO|SMASH CUT TO|MATCH CUT TO|FADE (?:IN|OUT)|"
    r"FADE TO BLACK|CIĘCIE|CIECIE|PRZENIKANIE|ZACIEMNIENIE|ROZJAŚNIENIE|"
    r"ROZJASNIENIE|PRZEJŚCIE|PRZEJSCIE)\b.*[:.]?\s*$",
    re.I,
)
# Cue extensions: (O.S.), (V.O.), (CONT'D), (POZA KADREM), (Z OFF)...
_CUE_EXTENSION = re.compile(r"\s*\(([^)]*)\)\s*$")

_OFFSCREEN_HINTS = ("O.S.", "OS", "OFF", "POZA KADREM", "ZA KADREM")
_VOICE_OVER_HINTS = ("V.O.", "VO", "Z OFF", "NARRACJA", "VOICEOVER", "VOICE OVER")


def _strip_diacritics(value: str) -> str:
    decomposed = unicodedata.normalize("NFD", value)
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")


def normalize_name(value: str) -> str:
    """A comparison key for names: caseless, unaccented, whitespace-collapsed.

    Used only for matching. The screenplay's own wording is always kept
    alongside it, per D-006.
    """
    stripped = _CUE_EXTENSION.sub("", value).strip()
    stripped = _strip_diacritics(stripped).upper()
    stripped = re.sub(r"[^A-Z0-9 ]+", " ", stripped)
    return re.sub(r"\s+", " ", stripped).strip()


@dataclass(frozen=True)
class Heading:
    """A parsed scene heading. ``raw`` is preserved exactly as written."""

    raw: str
    int_ext: str | None
    location: str | None
    sub_location: str | None
    time_of_day: str | None
    time_of_day_raw: str | None
    scene_number: str | None
    chronology_status: str


def _match_time_of_day(segment: str) -> str | None:
    # A trailing marker — "DZIEŃ (RETROSPEKCJA)" — is chronology, not part
    # of the time of day. It is read separately by _detect_chronology, so
    # dropping it here loses nothing.
    without_marker = re.sub(r"\s*\([^)]*\)\s*$", "", segment)
    key = _strip_diacritics(without_marker).upper().strip(" .")
    for token, canonical in _TIME_OF_DAY.items():
        if key == _strip_diacritics(token).upper():
            return canonical
    return None


def _detect_chronology(text: str) -> str:
    upper = _strip_diacritics(text).upper()
    for marker, status in _CHRONOLOGY_MARKERS.items():
        if _strip_diacritics(marker).upper() in upper:
            return status
    return "UNKNOWN"


def is_heading(line: str) -> bool:
    """True if ``line`` opens a scene."""
    stripped = line.strip()
    if not stripped:
        return False
    # Fountain's forced heading.
    if stripped.startswith(".") and not stripped.startswith(".."):
        return True
    if _TRANSITION.match(stripped):
        return False

    candidate = _SCENE_NUMBER_PREFIX.sub("", stripped)
    token = re.split(r"[\s.:]+", candidate, maxsplit=1)[0]
    token = _strip_diacritics(token).upper().rstrip(".")
    return token in {_strip_diacritics(k).upper().rstrip(".") for k in _INT_EXT_TOKENS}


def parse_heading(line: str) -> Heading:
    """Break a scene heading into its parts, preserving the original text."""
    body = line.strip()

    # A leading "." is Fountain's forcing syntax, not part of the heading.
    if body.startswith(".") and not body.startswith(".."):
        body = body[1:].strip()
    raw = body

    scene_number = None
    prefix_match = _SCENE_NUMBER_PREFIX.match(body)
    if prefix_match:
        scene_number = prefix_match.group(1)
        body = body[prefix_match.end():]

    suffix_match = _SCENE_NUMBER_SUFFIX.search(body)
    if suffix_match:
        scene_number = scene_number or suffix_match.group(1)
        body = body[: suffix_match.start()]

    int_ext = None
    token_match = re.match(r"^([A-ZĄĆĘŁŃÓŚŹŻa-ząćęłńóśźż/]+)\.?[\s.:]+", body)
    if token_match:
        key = _strip_diacritics(token_match.group(1)).upper()
        for token, canonical in _INT_EXT_TOKENS.items():
            if key == _strip_diacritics(token).upper():
                int_ext = canonical
                body = body[token_match.end():]
                break

    segments = [seg.strip() for seg in _SEPARATORS.split(body) if seg and seg.strip()]

    time_of_day = None
    time_of_day_raw = None
    if len(segments) > 1:
        candidate = _match_time_of_day(segments[-1])
        if candidate:
            time_of_day = candidate
            time_of_day_raw = segments.pop()

    location = segments[0] if segments else None
    sub_location = " - ".join(segments[1:]) if len(segments) > 1 else None

    # "HOUSE / KITCHEN" is the other common way to write a sub-location.
    if location and "/" in location and int_ext != INT_EXT:
        head, _, tail = location.partition("/")
        location = head.strip()
        sub_location = tail.strip() if not sub_location else f"{tail.strip()} - {sub_location}"

    return Heading(
        raw=raw,
        int_ext=int_ext,
        location=location,
        sub_location=sub_location,
        time_of_day=time_of_day,
        time_of_day_raw=time_of_day_raw,
        scene_number=scene_number,
        chronology_status=_detect_chronology(raw),
    )


# ---------------------------------------------------------------- dialogue


@dataclass
class DialogueBlock:
    speaker_raw: str
    speaker_key: str
    parenthetical: str | None
    text: str
    delivery: str  # VISIBLE | OFFSCREEN | VOICE_ONLY
    start_offset: int
    end_offset: int


@dataclass
class ParsedScene:
    script_order: int
    heading: Heading
    raw_text: str
    start_offset: int
    end_offset: int
    action_text: str = ""
    dialogue: list[DialogueBlock] = field(default_factory=list)


def _is_cue(line: str, next_line: str) -> bool:
    stripped = line.strip()
    if not stripped or not next_line.strip():
        return False
    if stripped.startswith("@"):  # Fountain's forced cue
        return True
    if _TRANSITION.match(stripped):
        return False
    if stripped.startswith("(") or stripped.endswith(":"):
        return False
    body = _CUE_EXTENSION.sub("", stripped).rstrip("^").strip()
    if not body:
        return False
    letters = [ch for ch in body if ch.isalpha()]
    if not letters:
        return False
    # A cue is written in capitals; Polish diacritics upper-case correctly.
    return all(ch.isupper() for ch in letters)


def _delivery_from_extension(extension: str | None) -> str:
    if not extension:
        return "VISIBLE"
    key = _strip_diacritics(extension).upper().replace(".", "").replace("'", "")
    for hint in _VOICE_OVER_HINTS:
        if _strip_diacritics(hint).upper().replace(".", "") in key:
            return "VOICE_ONLY"
    for hint in _OFFSCREEN_HINTS:
        if _strip_diacritics(hint).upper().replace(".", "") in key:
            return "OFFSCREEN"
    return "VISIBLE"


def _parse_scene_body(scene: ParsedScene, body: str, body_offset: int) -> None:
    lines = body.split("\n")
    action_lines: list[str] = []

    index = 0
    while index < len(lines):
        line = lines[index]
        next_line = lines[index + 1] if index + 1 < len(lines) else ""

        if not _is_cue(line, next_line):
            action_lines.append(line)
            index += 1
            continue

        cue_raw = line.strip().lstrip("@").rstrip("^").strip()
        extension_match = _CUE_EXTENSION.search(cue_raw)
        extension = extension_match.group(1) if extension_match else None
        speaker_raw = _CUE_EXTENSION.sub("", cue_raw).strip()

        index += 1
        parenthetical = None
        if index < len(lines) and lines[index].strip().startswith("("):
            parenthetical = lines[index].strip()
            index += 1

        speech: list[str] = []
        start = body_offset + sum(len(l) + 1 for l in lines[:index])
        while index < len(lines) and lines[index].strip():
            if lines[index].strip().startswith("(") and not speech:
                parenthetical = lines[index].strip()
            else:
                speech.append(lines[index].strip())
            index += 1

        text = " ".join(speech).strip()
        if not text:
            action_lines.append(line)
            continue

        scene.dialogue.append(
            DialogueBlock(
                speaker_raw=speaker_raw,
                speaker_key=normalize_name(speaker_raw),
                parenthetical=parenthetical,
                text=text,
                delivery=_delivery_from_extension(extension),
                start_offset=start,
                end_offset=start + len(text),
            )
        )

    scene.action_text = "\n".join(action_lines).strip()


def parse_screenplay(text: str) -> list[ParsedScene]:
    """Split a screenplay into scenes with dialogue and action separated.

    Text before the first heading (title page, front matter) is not a scene
    and is deliberately dropped from the scene list — the full original is
    preserved on the script record regardless.
    """
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = normalized.split("\n")

    offsets: list[int] = []
    running = 0
    for line in lines:
        offsets.append(running)
        running += len(line) + 1

    boundaries = [i for i, line in enumerate(lines) if is_heading(line)]
    scenes: list[ParsedScene] = []

    for order, line_index in enumerate(boundaries, start=1):
        end_line = boundaries[order] if order < len(boundaries) else len(lines)
        start_offset = offsets[line_index]
        end_offset = offsets[end_line] if end_line < len(lines) else len(normalized)
        raw_text = normalized[start_offset:end_offset].rstrip()

        scene = ParsedScene(
            script_order=order,
            heading=parse_heading(lines[line_index]),
            raw_text=raw_text,
            start_offset=start_offset,
            end_offset=start_offset + len(raw_text),
        )
        body_start = line_index + 1
        body = "\n".join(lines[body_start:end_line])
        _parse_scene_body(scene, body, offsets[body_start] if body_start < len(lines) else end_offset)
        scenes.append(scene)

    return scenes
