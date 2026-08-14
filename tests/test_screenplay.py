"""Parsing: headings, ordering, dialogue attribution.

Polish and English conventions both have to work, since the project's
dialogue language is Polish by default.
"""

from __future__ import annotations

import pytest

from pre.analysis.screenplay import (
    is_heading,
    normalize_name,
    parse_heading,
    parse_screenplay,
)


@pytest.mark.parametrize(
    "line",
    [
        "WN. MAGAZYN_01 - DZIEŃ",
        "PL. NABRZEŻE_01 - NOC",
        "INT. WAREHOUSE - DAY",
        "EXT. STREET - NIGHT",
        "ZEW. PARK - RANO",
        "WNĘTRZE. DOM - WIECZÓR",
        "12. WN. MAGAZYN_01 - DZIEŃ",
        ".FORCED HEADING",
    ],
)
def test_recognises_headings(line):
    assert is_heading(line)


@pytest.mark.parametrize(
    "line",
    [
        "POSTAĆ_01",
        "Idzie pustą ulicą.",
        "CUT TO:",
        "ZACIEMNIENIE.",
        "",
    ],
)
def test_rejects_non_headings(line):
    assert not is_heading(line)


def test_parses_polish_heading():
    heading = parse_heading("WN. MAGAZYN_01 - DZIEŃ")
    assert heading.int_ext == "INT"
    assert heading.location == "MAGAZYN_01"
    assert heading.time_of_day == "DAY"
    assert heading.time_of_day_raw == "DZIEŃ"
    # The original wording survives parsing untouched.
    assert heading.raw == "WN. MAGAZYN_01 - DZIEŃ"


def test_parses_english_heading():
    heading = parse_heading("EXT. HARBOUR - NIGHT")
    assert heading.int_ext == "EXT"
    assert heading.location == "HARBOUR"
    assert heading.time_of_day == "NIGHT"


def test_parses_sub_location():
    heading = parse_heading("WN. DOM_01 - KUCHNIA - NOC")
    assert heading.location == "DOM_01"
    assert heading.sub_location == "KUCHNIA"
    assert heading.time_of_day == "NIGHT"


def test_detects_explicit_flashback_marker():
    heading = parse_heading("WN. MAGAZYN_01 - DZIEŃ (RETROSPEKCJA)")
    assert heading.chronology_status == "FLASHBACK"


def test_chronology_unknown_without_a_marker():
    # Absence of a marker is not evidence of linearity — it stays unknown
    # for the semantic pass rather than being assumed.
    assert parse_heading("WN. MAGAZYN_01 - DZIEŃ").chronology_status == "UNKNOWN"


def test_scene_numbers_follow_the_screenplay_not_insertion():
    scenes = parse_screenplay(
        "WN. A - DZIEŃ\n\nAkcja.\n\nPL. B - NOC\n\nAkcja.\n\nWN. C - RANO\n\nAkcja.\n"
    )
    assert [scene.script_order for scene in scenes] == [1, 2, 3]
    assert [scene.heading.location for scene in scenes] == ["A", "B", "C"]


def test_front_matter_is_not_a_scene():
    scenes = parse_screenplay("Title: Test\nAuthor: X\n\nWN. A - DZIEŃ\n\nAkcja.\n")
    assert len(scenes) == 1


def test_separates_dialogue_from_action():
    scenes = parse_screenplay(
        "WN. A - DZIEŃ\n\nStoi przy oknie.\n\nPOSTAĆ_01\nMam to.\n\nOdchodzi.\n"
    )
    scene = scenes[0]
    assert len(scene.dialogue) == 1
    assert scene.dialogue[0].speaker_raw == "POSTAĆ_01"
    assert scene.dialogue[0].text == "Mam to."
    # Speech never leaks into the action text, and vice versa.
    assert "Mam to." not in scene.action_text
    assert "Stoi przy oknie." in scene.action_text


def test_captures_parenthetical():
    scenes = parse_screenplay("WN. A - DZIEŃ\n\nPOSTAĆ_01\n(cicho)\nNie tak.\n")
    assert scenes[0].dialogue[0].parenthetical == "(cicho)"
    assert scenes[0].dialogue[0].text == "Nie tak."


@pytest.mark.parametrize(
    "cue,delivery",
    [
        ("POSTAĆ_01", "VISIBLE"),
        ("POSTAĆ_01 (O.S.)", "OFFSCREEN"),
        ("POSTAĆ_01 (POZA KADREM)", "OFFSCREEN"),
        ("POSTAĆ_01 (V.O.)", "VOICE_ONLY"),
        ("POSTAĆ_01 (Z OFF)", "VOICE_ONLY"),
    ],
)
def test_reads_delivery_from_cue_extension(cue, delivery):
    scenes = parse_screenplay(f"WN. A - DZIEŃ\n\n{cue}\nSłowa.\n")
    assert scenes[0].dialogue[0].delivery == delivery


def test_transition_is_not_a_character_cue():
    scenes = parse_screenplay("WN. A - DZIEŃ\n\nAkcja.\n\nCUT TO:\n\nDalej.\n")
    assert scenes[0].dialogue == []


def test_normalize_name_is_a_matching_key_only():
    assert normalize_name("POSTAĆ_01") == normalize_name("postac 01")
    assert normalize_name("POSTAĆ_01 (O.S.)") == normalize_name("POSTAĆ_01")
