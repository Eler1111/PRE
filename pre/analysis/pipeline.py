"""The deterministic global analysis pass.

This is the half of Module 01 that code owns outright: file handling, scene
storage, ordering, ids, persistence, and the facts the screenplay states
outright — who speaks, where a scene is set, which scene something appears
in.

What it deliberately does not do: infer state events, resolve aliases,
judge prop significance, or guess chronology beyond explicit markers. That
is the semantic pass, and inventing it here would freeze guesses as facts.
"""

from __future__ import annotations

import difflib
import re
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from ..ids import new_id, sequential_id
from ..importers import extract_title, importer_for
from ..project import Project
from .screenplay import ParsedScene, normalize_name, parse_screenplay

# Two names this similar are probably the same subject, but "probably" is
# not good enough to merge — it raises a review flag instead.
_ALIAS_SIMILARITY = 0.86

# A character in this many scenes carries enough weight to need a locked
# acting profile later.
_RECURRING_SCENE_COUNT = 2


@dataclass
class ImportResult:
    script_id: str
    scene_count: int
    character_count: int
    location_count: int
    review_flag_count: int


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def import_screenplay(project: Project, source_path: Path) -> ImportResult:
    """Import a screenplay and run the deterministic analysis pass."""
    source_path = Path(source_path)
    if not source_path.exists():
        raise FileNotFoundError(f"Nie znaleziono pliku: {source_path}")

    importer = importer_for(source_path)
    raw_text, normalized_text = importer.read(source_path)

    # The original is preserved byte-for-byte; analysis reads the copy.
    project.script_dir.mkdir(exist_ok=True)
    preserved = project.script_dir / source_path.name
    if preserved.exists():
        preserved = project.script_dir / f"{source_path.stem}_{new_id('v')}{source_path.suffix}"
    shutil.copy2(source_path, preserved)

    connection = project.connection
    script_id = new_id("script")
    title = extract_title(importer.format_name, raw_text, normalized_text)

    connection.execute(
        "INSERT INTO script (id, project_id, title, source_file, source_format, "
        "imported_at, raw_text, normalized_text, parse_status, analysis_status) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            script_id,
            project.id,
            title or source_path.stem,
            str(preserved.relative_to(project.path)),
            importer.format_name,
            _now(),
            raw_text,
            normalized_text,
            "PARSED",
            "DETERMINISTIC_PASS_DONE",
        ),
    )

    scenes = parse_screenplay(normalized_text)
    if not scenes:
        connection.execute(
            "UPDATE script SET parse_status = ? WHERE id = ?", ("NO_SCENES_FOUND", script_id)
        )
        connection.commit()
        raise ValueError(
            "Nie znaleziono żadnej sceny. Sprawdź, czy nagłówki scen są zapisane "
            "w formacie WN./PL. lub INT./EXT."
        )

    scene_ids = _persist_scenes(project, script_id, scenes)
    locations = _persist_locations(project, scenes, scene_ids)
    characters = _persist_characters(project, scenes, scene_ids)
    _persist_requirements(project, characters)
    flags = _flag_similar_names(project)

    connection.execute(
        "INSERT INTO production_log (id, project_id, event_type, summary, detail, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (
            new_id("log"),
            project.id,
            "SCRIPT_IMPORTED",
            f"Zaimportowano scenariusz: {title or source_path.name}",
            f"{len(scenes)} scen, {len(characters)} postaci, {len(locations)} lokacji",
            _now(),
        ),
    )
    connection.commit()

    return ImportResult(
        script_id=script_id,
        scene_count=len(scenes),
        character_count=len(characters),
        location_count=len(locations),
        review_flag_count=flags,
    )


def _persist_scenes(
    project: Project, script_id: str, scenes: list[ParsedScene]
) -> dict[int, str]:
    """Store scenes and return ``{script_order: scene_id}``."""
    connection = project.connection
    scene_ids: dict[int, str] = {}

    for scene in scenes:
        scene_id = sequential_id(connection, "scene", "scene", "script_id", script_id)
        heading = scene.heading
        connection.execute(
            "INSERT INTO scene (id, script_id, scene_number, script_order, heading_raw, "
            "int_ext, sub_location, time_of_day, time_of_day_raw, raw_text, "
            "normalized_text, chronology_status, story_order) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL)",
            (
                scene_id,
                script_id,
                heading.scene_number,
                scene.script_order,
                heading.raw,
                heading.int_ext,
                heading.sub_location,
                heading.time_of_day,
                heading.time_of_day_raw,
                scene.raw_text,
                scene.raw_text,
                heading.chronology_status,
            ),
        )
        scene_ids[scene.script_order] = scene_id

    return scene_ids


def _get_or_create_entity(
    project: Project,
    entity_type: str,
    canonical_name: str,
    display_name: str,
    information_status: str,
) -> str:
    connection = project.connection
    key = normalize_name(canonical_name)
    row = connection.execute(
        "SELECT id FROM entity WHERE project_id = ? AND entity_type = ? "
        "AND canonical_name = ?",
        (project.id, entity_type, key),
    ).fetchone()
    if row:
        return row["id"]

    prefix = {"CHARACTER": "char", "LOCATION": "loc", "PROP": "prop"}.get(
        entity_type, "ent"
    )
    entity_id = sequential_id(connection, "entity", prefix, "project_id", project.id)
    connection.execute(
        "INSERT INTO entity (id, project_id, entity_type, canonical_name, display_name, "
        "information_status, confidence, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (entity_id, project.id, entity_type, key, display_name, information_status,
         1.0 if information_status == "FACT" else None, _now()),
    )
    return entity_id


def _add_alias(project: Project, entity_id: str, alias_raw: str, status: str) -> None:
    project.connection.execute(
        "INSERT OR IGNORE INTO entity_alias (id, entity_id, alias_raw, alias_normalized, "
        "information_status, confidence, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (new_id("alias"), entity_id, alias_raw, normalize_name(alias_raw), status,
         1.0 if status == "FACT" else None, _now()),
    )


def _add_appearance(
    project: Project,
    scene_id: str,
    entity_id: str,
    appearance_type: str,
    speaks: bool,
    status: str,
    confidence: float | None,
) -> None:
    project.connection.execute(
        "INSERT INTO entity_appearance (id, scene_id, entity_id, appearance_type, speaks, "
        "information_status, confidence) VALUES (?, ?, ?, ?, ?, ?, ?) "
        "ON CONFLICT(scene_id, entity_id, appearance_type) DO UPDATE SET "
        "speaks = MAX(speaks, excluded.speaks)",
        (new_id("app"), scene_id, entity_id, appearance_type, int(speaks), status, confidence),
    )


def _add_evidence(
    project: Project, subject_table: str, subject_id: str, scene_id: str, span: str
) -> None:
    project.connection.execute(
        "INSERT INTO source_evidence (id, project_id, subject_table, subject_id, scene_id, "
        "text_span) VALUES (?, ?, ?, ?, ?, ?)",
        (new_id("ev"), project.id, subject_table, subject_id, scene_id, span[:500]),
    )


def _persist_locations(
    project: Project, scenes: list[ParsedScene], scene_ids: dict[int, str]
) -> dict[str, str]:
    """Create a location entity per distinct heading location."""
    locations: dict[str, str] = {}

    for scene in scenes:
        location = scene.heading.location
        if not location:
            continue
        key = normalize_name(location)
        if not key:
            continue

        entity_id = locations.get(key)
        if entity_id is None:
            # The heading states the location outright, so this is a FACT.
            entity_id = _get_or_create_entity(
                project, "LOCATION", location, location, "FACT"
            )
            locations[key] = entity_id
            _add_evidence(
                project, "entity", entity_id, scene_ids[scene.script_order], scene.heading.raw
            )

        _add_alias(project, entity_id, location, "FACT")
        project.connection.execute(
            "UPDATE scene SET location_entity_id = ? WHERE id = ?",
            (entity_id, scene_ids[scene.script_order]),
        )
        _add_appearance(
            project, scene_ids[scene.script_order], entity_id, "VISIBLE", False, "FACT", 1.0
        )

    return locations


def _persist_characters(
    project: Project, scenes: list[ParsedScene], scene_ids: dict[int, str]
) -> dict[str, str]:
    """Create character entities from dialogue cues, then find them in action."""
    connection = project.connection
    characters: dict[str, str] = {}

    # Pass one: everyone who speaks. A dialogue cue is explicit screenplay
    # text, so these are facts.
    for scene in scenes:
        scene_id = scene_ids[scene.script_order]
        for order, block in enumerate(scene.dialogue):
            if not block.speaker_key:
                continue
            entity_id = characters.get(block.speaker_key)
            if entity_id is None:
                entity_id = _get_or_create_entity(
                    project, "CHARACTER", block.speaker_raw, block.speaker_raw, "FACT"
                )
                characters[block.speaker_key] = entity_id
                _add_evidence(project, "entity", entity_id, scene_id, block.speaker_raw)

            _add_alias(project, entity_id, block.speaker_raw, "FACT")
            _add_appearance(project, scene_id, entity_id, block.delivery, True, "FACT", 1.0)

            connection.execute(
                "INSERT INTO dialogue_line (id, scene_id, entity_id, speaker_raw, "
                "parenthetical, text, order_in_scene, start_offset, end_offset) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (new_id("dlg"), scene_id, entity_id, block.speaker_raw, block.parenthetical,
                 block.text, order, block.start_offset, block.end_offset),
            )

    # Pass two: known names appearing in action text. Presence is likely but
    # not certain — a name can be spoken about rather than present — so this
    # is recorded as inference, never as fact.
    for scene in scenes:
        if not scene.action_text:
            continue
        scene_id = scene_ids[scene.script_order]
        action_key = normalize_name(scene.action_text)
        for key, entity_id in characters.items():
            if re.search(rf"\b{re.escape(key)}\b", action_key):
                _add_appearance(project, scene_id, entity_id, "VISIBLE", False, "INFERENCE", 0.7)

    return characters


def _persist_requirements(project: Project, characters: dict[str, str]) -> None:
    """Record that voices and acting profiles will be needed. Not created."""
    connection = project.connection
    language = connection.execute(
        "SELECT dialogue_language FROM project WHERE id = ?", (project.id,)
    ).fetchone()["dialogue_language"]

    for entity_id in characters.values():
        speaking_scenes = connection.execute(
            "SELECT COUNT(DISTINCT scene_id) AS n FROM entity_appearance "
            "WHERE entity_id = ? AND speaks = 1",
            (entity_id,),
        ).fetchone()["n"]
        total_scenes = connection.execute(
            "SELECT COUNT(DISTINCT scene_id) AS n FROM entity_appearance WHERE entity_id = ?",
            (entity_id,),
        ).fetchone()["n"]

        if speaking_scenes:
            connection.execute(
                "INSERT OR IGNORE INTO voice_requirement (id, project_id, entity_id, "
                "speaking_scene_count, language, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (new_id("voice"), project.id, entity_id, speaking_scenes, language, _now()),
            )

        if speaking_scenes or total_scenes >= _RECURRING_SCENE_COUNT:
            reason = (
                "Postać mówiąca" if speaking_scenes
                else f"Postać powracająca ({total_scenes} scen)"
            )
            connection.execute(
                "INSERT OR IGNORE INTO acting_requirement (id, project_id, entity_id, "
                "priority, reason, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (new_id("acting"), project.id, entity_id, total_scenes, reason, _now()),
            )


def _differs_only_by_number(left: str, right: str) -> bool:
    """True when two names are identical once their digits are removed."""
    strip = lambda value: re.sub(r"\s+", " ", re.sub(r"\d+", "", value)).strip()
    return left != right and strip(left) == strip(right)


def _flag_similar_names(project: Project) -> int:
    """Raise a review flag where two entities of a type look like one subject.

    Deliberately does not merge. Merging near-identical names automatically
    is how a screenplay ends up with one character split in two, or two
    locations collapsed into one that were never the same place.
    """
    connection = project.connection
    flags = 0

    for entity_type, label in (("CHARACTER", "postać"), ("LOCATION", "lokacja")):
        rows = connection.execute(
            "SELECT id, canonical_name, display_name FROM entity "
            "WHERE project_id = ? AND entity_type = ? ORDER BY canonical_name",
            (project.id, entity_type),
        ).fetchall()

        for i, left in enumerate(rows):
            for right in rows[i + 1:]:
                ratio = difflib.SequenceMatcher(
                    None, left["canonical_name"], right["canonical_name"]
                ).ratio()
                if ratio < _ALIAS_SIMILARITY:
                    continue
                # "POKÓJ 1" and "POKÓJ 2", or two numbered guards, are
                # deliberately enumerated and almost never the same subject.
                if _differs_only_by_number(left["canonical_name"], right["canonical_name"]):
                    continue
                connection.execute(
                    "INSERT INTO review_flag (id, project_id, entity_id, category, question, "
                    "evidence, confidence, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        new_id("flag"),
                        project.id,
                        left["id"],
                        "POSSIBLE_ALIAS",
                        f"Czy „{left['display_name']}” i „{right['display_name']}” "
                        f"to ta sama {label}?",
                        f"{left['canonical_name']} ≈ {right['canonical_name']}",
                        round(ratio, 2),
                        _now(),
                    ),
                )
                flags += 1

    return flags
