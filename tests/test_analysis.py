"""The deterministic global analysis pass, run against the synthetic script."""

from __future__ import annotations

from pathlib import Path

import pytest

from pre.analysis import import_screenplay
from pre.queries import (
    evidence_for,
    find_entity,
    list_scenes,
    open_review_flags,
    project_counts,
    scenes_with_entity,
)

FIXTURE = Path(__file__).resolve().parent.parent / "fixtures" / "synthetic_pl.fountain"


# ------------------------------------------------------------------ import


def test_preserves_the_original_file(analysed):
    project, _ = analysed
    copies = list(project.script_dir.iterdir())
    assert len(copies) == 1
    assert copies[0].read_bytes() == FIXTURE.read_bytes()


def test_stores_raw_text_unmodified(analysed):
    project, result = analysed
    row = project.connection.execute(
        "SELECT raw_text FROM script WHERE id = ?", (result.script_id,)
    ).fetchone()
    assert row["raw_text"] == FIXTURE.read_text(encoding="utf-8")


def test_reads_the_title_from_the_title_page(analysed):
    project, result = analysed
    row = project.connection.execute(
        "SELECT title FROM script WHERE id = ?", (result.script_id,)
    ).fetchone()
    assert row["title"] == "SCENARIUSZ TESTOWY 01"


def test_rejects_unsupported_formats(project, tmp_path):
    unsupported = tmp_path / "screenplay.rtf"
    unsupported.write_text(r"{\rtf1 WN. MAGAZYN - DZIEN}", encoding="utf-8")
    with pytest.raises(ValueError, match="Nieobsługiwany format"):
        import_screenplay(project, unsupported)


# ------------------------------------------------------------------- scenes


def test_every_scene_is_found_in_screenplay_order(analysed):
    project, result = analysed
    scenes = list_scenes(project)
    assert result.scene_count == len(scenes) == 10
    assert [scene["script_order"] for scene in scenes] == list(range(1, 11))


def test_recurring_location_is_one_entity_across_times_of_day(analysed):
    project, _ = analysed
    warehouse = find_entity(project, "MAGAZYN_01", "LOCATION")
    assert warehouse is not None

    scenes = [s for s in list_scenes(project) if s["location_name"] == "MAGAZYN_01"]
    times = {scene["time_of_day"] for scene in scenes}
    # Same place, three times of day — one location entity, not three.
    assert times == {"DAY", "NIGHT", "MORNING"}


def test_explicit_flashback_is_marked_and_others_are_not_assumed_linear(analysed):
    project, _ = analysed
    scenes = list_scenes(project)
    flashbacks = [s for s in scenes if s["chronology_status"] == "FLASHBACK"]
    assert len(flashbacks) == 1
    assert "RETROSPEKCJA" in flashbacks[0]["heading_raw"]

    # Scenes without a marker stay UNKNOWN rather than being called linear.
    assert all(
        s["chronology_status"] == "UNKNOWN" for s in scenes if s not in flashbacks
    )


def test_story_order_is_left_empty_until_chronology_is_analysed(analysed):
    project, _ = analysed
    # Silently reusing script order as story order is exactly the failure
    # that makes a flashback inherit the present-day state.
    assert all(scene["story_order"] is None for scene in list_scenes(project))


# ----------------------------------------------------------------- entities


def test_speaking_characters_are_facts(analysed):
    project, _ = analysed
    character = find_entity(project, "POSTAĆ_01", "CHARACTER")
    assert character is not None
    assert character["information_status"] == "FACT"


def test_character_appearances_span_the_screenplay(analysed):
    project, _ = analysed
    character = find_entity(project, "POSTAĆ_01", "CHARACTER")
    orders = {row["script_order"] for row in scenes_with_entity(project, character["id"])}
    assert orders >= {1, 2, 3, 4, 5, 6, 7}


def test_offscreen_and_visible_appearances_are_distinguished(analysed):
    project, _ = analysed
    character = find_entity(project, "POSTAĆ_01", "CHARACTER")
    kinds = {row["appearance_type"] for row in scenes_with_entity(project, character["id"])}
    assert "VISIBLE" in kinds


def test_appearance_inferred_from_action_is_not_a_fact(analysed):
    project, _ = analysed
    character = find_entity(project, "POSTAĆ_01", "CHARACTER")
    rows = scenes_with_entity(project, character["id"])
    inferred = [row for row in rows if row["information_status"] == "INFERENCE"]
    # A name in an action line means presence is likely, not certain.
    assert inferred, "obecność wywnioskowana z didaskaliów powinna istnieć"
    assert all(row["confidence"] < 1.0 for row in inferred)


def test_aliases_preserve_the_screenplay_wording(analysed):
    project, _ = analysed
    character = find_entity(project, "POSTAĆ_01", "CHARACTER")
    aliases = project.connection.execute(
        "SELECT alias_raw FROM entity_alias WHERE entity_id = ?", (character["id"],)
    ).fetchall()
    assert "POSTAĆ_01" in {row["alias_raw"] for row in aliases}


def test_entity_is_findable_by_alias(analysed):
    project, _ = analysed
    by_canonical = find_entity(project, "POSTAĆ_01", "CHARACTER")
    by_alias = find_entity(project, "postac 01", "CHARACTER")
    assert by_alias is not None and by_alias["id"] == by_canonical["id"]


# ------------------------------------------------------------- review flags


def test_spelling_variant_is_flagged_not_merged(analysed):
    """"MAGAZYN PÓŁNOCNY" and "MAGAZYN PÓŁNOCY" — typo, or two places?"""
    project, _ = analysed
    flags = [f for f in open_review_flags(project) if f["category"] == "POSSIBLE_ALIAS"]
    assert flags, "podobne nazwy lokacji powinny trafić do decyzji użytkownika"

    # Both survive as separate entities until somebody decides which it is.
    assert find_entity(project, "MAGAZYN PÓŁNOCNY", "LOCATION") is not None
    assert find_entity(project, "MAGAZYN PÓŁNOCY", "LOCATION") is not None


def test_semantic_ambiguity_is_left_unresolved_rather_than_guessed(analysed):
    """Is "MAGAZYN PÓŁNOCNY" the same hall as "MAGAZYN_01"?

    Only reading the scene answers that, so the deterministic pass must not
    quietly merge them — an unresolved question is the correct outcome here.
    """
    project, _ = analysed
    warehouse = find_entity(project, "MAGAZYN_01", "LOCATION")
    northern = find_entity(project, "MAGAZYN PÓŁNOCNY", "LOCATION")
    assert warehouse["id"] != northern["id"]


def test_numbered_siblings_are_not_flagged_as_aliases(analysed):
    project, _ = analysed
    questions = " ".join(flag["question"] for flag in open_review_flags(project))
    # POSTAĆ_01 and POSTAĆ_02 differ only by number; they are two people.
    assert "POSTAĆ_01" not in questions or "POSTAĆ_02" not in questions


# ------------------------------------------------------------ requirements


def test_speaking_characters_get_a_voice_requirement(analysed):
    project, _ = analysed
    counts = project_counts(project)
    assert counts.voice_requirements == counts.speaking_characters
    assert counts.speaking_characters >= 3


def test_voice_requirement_defaults_to_the_project_language(analysed):
    project, _ = analysed
    languages = {
        row["language"]
        for row in project.connection.execute(
            "SELECT language FROM voice_requirement WHERE project_id = ?", (project.id,)
        ).fetchall()
    }
    assert languages == {"pl"}


def test_recurring_characters_get_an_acting_requirement(analysed):
    project, _ = analysed
    assert project_counts(project).acting_requirements >= 3


def test_requirements_are_recorded_but_nothing_is_produced(analysed):
    project, _ = analysed
    counts = project_counts(project)
    assert counts.assets_created == 0
    # Module 01 records that assets will be needed; it never creates one.
    for table in ("voice_requirement", "acting_requirement"):
        statuses = {
            row["production_status"]
            for row in project.connection.execute(
                f"SELECT production_status FROM {table} WHERE project_id = ?", (project.id,)
            ).fetchall()
        }
        assert statuses <= {"NOT_CREATED"}


# -------------------------------------------------------------- provenance


def test_evidence_points_back_at_the_screenplay(analysed):
    project, _ = analysed
    character = find_entity(project, "POSTAĆ_01", "CHARACTER")
    evidence = evidence_for(project, "entity", character["id"])
    assert evidence, "system musi umieć pokazać, skąd wie o postaci"
    assert evidence[0]["text_span"]


def test_import_is_logged(analysed):
    project, _ = analysed
    rows = project.connection.execute(
        "SELECT event_type FROM production_log WHERE project_id = ?", (project.id,)
    ).fetchall()
    assert "SCRIPT_IMPORTED" in {row["event_type"] for row in rows}
