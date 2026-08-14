"""Structured reads of the project model.

Everything the chat can be asked after an analysis — "pokaż sceny",
"w których scenach występuje X", "jakie są niejasności" — is answered from
these, never from conversation memory. The chat layer formats; it does not
remember.
"""

from __future__ import annotations

from dataclasses import dataclass

from .project import Project


@dataclass(frozen=True)
class ProjectCounts:
    scenes: int
    characters: int
    speaking_characters: int
    locations: int
    props: int
    character_state_events: int
    location_state_events: int
    prop_state_events: int
    voice_requirements: int
    acting_requirements: int
    open_review_flags: int
    assets_created: int


def project_counts(project: Project) -> ProjectCounts:
    """Counts straight from the database.

    These numbers must come from structured data, never from a separate
    model summary that has drifted from what was actually stored.
    """
    connection = project.connection

    def scalar(sql: str, params: tuple = ()) -> int:
        row = connection.execute(sql, params).fetchone()
        return int(row[0]) if row and row[0] is not None else 0

    def entities_of(entity_type: str) -> int:
        return scalar(
            "SELECT COUNT(*) FROM entity WHERE project_id = ? AND entity_type = ? "
            "AND information_status != 'REJECTED'",
            (project.id, entity_type),
        )

    def events_for(entity_type: str) -> int:
        return scalar(
            "SELECT COUNT(*) FROM state_event se JOIN entity e ON e.id = se.entity_id "
            "WHERE e.project_id = ? AND e.entity_type = ?",
            (project.id, entity_type),
        )

    return ProjectCounts(
        scenes=scalar(
            "SELECT COUNT(*) FROM scene s JOIN script sc ON sc.id = s.script_id "
            "WHERE sc.project_id = ?",
            (project.id,),
        ),
        characters=entities_of("CHARACTER"),
        speaking_characters=scalar(
            "SELECT COUNT(DISTINCT entity_id) FROM entity_appearance ea "
            "JOIN entity e ON e.id = ea.entity_id "
            "WHERE e.project_id = ? AND ea.speaks = 1",
            (project.id,),
        ),
        locations=entities_of("LOCATION"),
        props=entities_of("PROP"),
        character_state_events=events_for("CHARACTER"),
        location_state_events=events_for("LOCATION"),
        prop_state_events=events_for("PROP"),
        voice_requirements=scalar(
            "SELECT COUNT(*) FROM voice_requirement WHERE project_id = ?", (project.id,)
        ),
        acting_requirements=scalar(
            "SELECT COUNT(*) FROM acting_requirement WHERE project_id = ?", (project.id,)
        ),
        open_review_flags=scalar(
            "SELECT COUNT(*) FROM review_flag WHERE project_id = ? AND status = 'OPEN'",
            (project.id,),
        ),
        # Module 01 never creates assets. This stays zero by design, and the
        # summary says so out loud.
        assets_created=scalar(
            "SELECT COUNT(*) FROM asset_requirement WHERE project_id = ? "
            "AND production_status NOT IN ('NOT_CREATED')",
            (project.id,),
        ),
    )


def list_scenes(project: Project) -> list[dict]:
    """Every scene in screenplay order."""
    rows = project.connection.execute(
        "SELECT s.id, s.scene_number, s.script_order, s.heading_raw, s.int_ext, "
        "       s.sub_location, s.time_of_day, s.chronology_status, s.story_order, "
        "       e.display_name AS location_name "
        "FROM scene s "
        "JOIN script sc ON sc.id = s.script_id "
        "LEFT JOIN entity e ON e.id = s.location_entity_id "
        "WHERE sc.project_id = ? ORDER BY s.script_order",
        (project.id,),
    ).fetchall()
    return [dict(row) for row in rows]


def find_entity(project: Project, name: str, entity_type: str | None = None) -> dict | None:
    """Look an entity up by any of its names, canonical or alias."""
    from .analysis.screenplay import normalize_name

    key = normalize_name(name)
    sql = (
        "SELECT DISTINCT e.* FROM entity e "
        "LEFT JOIN entity_alias a ON a.entity_id = e.id "
        "WHERE e.project_id = ? AND (e.canonical_name = ? OR a.alias_normalized = ?)"
    )
    params: list = [project.id, key, key]
    if entity_type:
        sql += " AND e.entity_type = ?"
        params.append(entity_type)

    row = project.connection.execute(sql, tuple(params)).fetchone()
    return dict(row) if row else None


def scenes_with_entity(project: Project, entity_id: str) -> list[dict]:
    """Which scenes an entity appears in, and how."""
    rows = project.connection.execute(
        "SELECT s.script_order, s.scene_number, s.heading_raw, ea.appearance_type, "
        "       ea.speaks, ea.information_status, ea.confidence "
        "FROM entity_appearance ea JOIN scene s ON s.id = ea.scene_id "
        "WHERE ea.entity_id = ? ORDER BY s.script_order",
        (entity_id,),
    ).fetchall()
    return [dict(row) for row in rows]


def entity_states(project: Project, entity_id: str) -> list[dict]:
    """An entity's states, each with the explicit set of scenes it holds in.

    Per D-008 the scenes are enumerated, not expressed as a range — a
    flashback simply is not in the list.
    """
    states = project.connection.execute(
        "SELECT * FROM state WHERE entity_id = ? ORDER BY created_at", (entity_id,)
    ).fetchall()

    result = []
    for state in states:
        scenes = project.connection.execute(
            "SELECT s.script_order, s.scene_number, s.heading_raw "
            "FROM state_scene ss JOIN scene s ON s.id = ss.scene_id "
            "WHERE ss.state_id = ? ORDER BY s.script_order",
            (state["id"],),
        ).fetchall()
        entry = dict(state)
        entry["scenes"] = [dict(row) for row in scenes]
        result.append(entry)
    return result


def open_review_flags(project: Project) -> list[dict]:
    """Unresolved production questions, newest last."""
    rows = project.connection.execute(
        "SELECT rf.*, e.display_name AS entity_name, s.script_order "
        "FROM review_flag rf "
        "LEFT JOIN entity e ON e.id = rf.entity_id "
        "LEFT JOIN scene s ON s.id = rf.scene_id "
        "WHERE rf.project_id = ? AND rf.status = 'OPEN' ORDER BY rf.created_at",
        (project.id,),
    ).fetchall()
    return [dict(row) for row in rows]


def scene_asset_requirements(project: Project, script_order: int) -> list[dict]:
    """What a given scene will need produced."""
    rows = project.connection.execute(
        "SELECT ar.*, e.display_name AS entity_name, e.entity_type, st.name AS state_name "
        "FROM asset_requirement ar "
        "JOIN entity e ON e.id = ar.entity_id "
        "LEFT JOIN state st ON st.id = ar.state_id "
        "JOIN scene s ON s.id = ar.first_needed_scene_id "
        "JOIN script sc ON sc.id = s.script_id "
        "WHERE sc.project_id = ? AND s.script_order = ?",
        (project.id, script_order),
    ).fetchall()
    return [dict(row) for row in rows]


def evidence_for(project: Project, subject_table: str, subject_id: str) -> list[dict]:
    """The screenplay text behind a stored claim.

    This is what lets the system answer "skąd to wiesz?" with the actual
    lines rather than a restatement.
    """
    rows = project.connection.execute(
        "SELECT se.text_span, se.start_offset, se.end_offset, s.script_order, s.heading_raw "
        "FROM source_evidence se LEFT JOIN scene s ON s.id = se.scene_id "
        "WHERE se.project_id = ? AND se.subject_table = ? AND se.subject_id = ?",
        (project.id, subject_table, subject_id),
    ).fetchall()
    return [dict(row) for row in rows]
