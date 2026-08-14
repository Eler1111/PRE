-- PRE project database schema.
--
-- Implements the Module 01 data model. See docs/DECISIONS.md:
--   D-005  one entity table with a type discriminator
--   D-006  entity_alias is a first-class table
--   D-007  continuity dependencies carry provenance
--   D-008  state validity is an explicit set of scenes, never a range
--   D-009  information_status and production_status are separate axes

PRAGMA foreign_keys = ON;

CREATE TABLE schema_version (
    version     INTEGER NOT NULL,
    applied_at  TEXT    NOT NULL
);

-- ---------------------------------------------------------------- project

CREATE TABLE project (
    id           TEXT PRIMARY KEY,
    name         TEXT NOT NULL,
    -- tig-scene-engine cannot audit a scene's Goal without the story goal,
    -- so it lives on the project rather than being asked for every run.
    story_goal   TEXT,
    logline      TEXT,
    dialogue_language TEXT NOT NULL DEFAULT 'pl',
    created_at   TEXT NOT NULL
);

CREATE TABLE script (
    id              TEXT PRIMARY KEY,
    project_id      TEXT NOT NULL REFERENCES project(id) ON DELETE CASCADE,
    title           TEXT,
    -- Path relative to the project folder. The original import is never
    -- modified; this always points at the preserved copy.
    source_file     TEXT NOT NULL,
    source_format   TEXT NOT NULL,
    imported_at     TEXT NOT NULL,
    raw_text        TEXT NOT NULL,
    normalized_text TEXT NOT NULL,
    parse_status    TEXT NOT NULL,
    analysis_status TEXT NOT NULL
);

CREATE TABLE scene (
    id                TEXT PRIMARY KEY,
    script_id         TEXT NOT NULL REFERENCES script(id) ON DELETE CASCADE,
    -- The number as written in the screenplay, if any. Display only.
    scene_number      TEXT,
    -- Position in the screenplay. Never derived from insertion order.
    script_order      INTEGER NOT NULL,
    heading_raw       TEXT NOT NULL,
    int_ext           TEXT,
    location_entity_id TEXT REFERENCES entity(id) ON DELETE SET NULL,
    sub_location      TEXT,
    time_of_day       TEXT,
    time_of_day_raw   TEXT,
    raw_text          TEXT NOT NULL,
    normalized_text   TEXT NOT NULL,
    chronology_status TEXT NOT NULL DEFAULT 'UNKNOWN'
        CHECK (chronology_status IN ('LINEAR','FLASHBACK','FLASHFORWARD',
                                     'DREAM','IMAGINED','PARALLEL','UNKNOWN')),
    -- Position in story chronology, distinct from script_order. NULL until
    -- chronology analysis has run; never silently defaulted to script_order.
    story_order       INTEGER,
    UNIQUE (script_id, script_order)
);

CREATE INDEX idx_scene_script_order ON scene(script_id, script_order);

-- ---------------------------------------------------------------- entities

-- D-005: characters, locations, props, vehicles and animals share one table.
-- The source productions blur these categories in practice (a car interior
-- is a prop; a crowd is one asset), so the type is a column, not a schema.
CREATE TABLE entity (
    id             TEXT PRIMARY KEY,
    project_id     TEXT NOT NULL REFERENCES project(id) ON DELETE CASCADE,
    entity_type    TEXT NOT NULL
        CHECK (entity_type IN ('CHARACTER','LOCATION','PROP','VEHICLE',
                               'ANIMAL','CROWD','OTHER')),
    canonical_name TEXT NOT NULL,
    display_name   TEXT,
    description    TEXT,
    -- D-009: provenance, kept strictly apart from production progress.
    information_status TEXT NOT NULL DEFAULT 'INFERENCE'
        CHECK (information_status IN ('FACT','INFERENCE','APPROVED',
                                      'REJECTED','OVERRIDDEN','UNKNOWN')),
    confidence     REAL,
    -- Locations may nest (a building and its rooms). Same table, per D-005.
    parent_entity_id TEXT REFERENCES entity(id) ON DELETE SET NULL,
    created_at     TEXT NOT NULL,
    UNIQUE (project_id, entity_type, canonical_name)
);

CREATE INDEX idx_entity_project_type ON entity(project_id, entity_type);

-- D-006: the screenplay's own wording is preserved, always.
CREATE TABLE entity_alias (
    id            TEXT PRIMARY KEY,
    entity_id     TEXT NOT NULL REFERENCES entity(id) ON DELETE CASCADE,
    alias_raw     TEXT NOT NULL,
    alias_normalized TEXT NOT NULL,
    information_status TEXT NOT NULL DEFAULT 'INFERENCE'
        CHECK (information_status IN ('FACT','INFERENCE','APPROVED',
                                      'REJECTED','OVERRIDDEN','UNKNOWN')),
    confidence    REAL,
    created_at    TEXT NOT NULL,
    UNIQUE (entity_id, alias_normalized)
);

CREATE TABLE entity_appearance (
    id              TEXT PRIMARY KEY,
    scene_id        TEXT NOT NULL REFERENCES scene(id) ON DELETE CASCADE,
    entity_id       TEXT NOT NULL REFERENCES entity(id) ON DELETE CASCADE,
    appearance_type TEXT NOT NULL
        CHECK (appearance_type IN ('VISIBLE','OFFSCREEN','MENTIONED',
                                   'DIALOGUE_ONLY','VOICE_ONLY','UNKNOWN')),
    speaks          INTEGER NOT NULL DEFAULT 0,
    information_status TEXT NOT NULL DEFAULT 'INFERENCE'
        CHECK (information_status IN ('FACT','INFERENCE','APPROVED',
                                      'REJECTED','OVERRIDDEN','UNKNOWN')),
    confidence      REAL,
    UNIQUE (scene_id, entity_id, appearance_type)
);

CREATE INDEX idx_appearance_entity ON entity_appearance(entity_id);

CREATE TABLE dialogue_line (
    id           TEXT PRIMARY KEY,
    scene_id     TEXT NOT NULL REFERENCES scene(id) ON DELETE CASCADE,
    entity_id    TEXT REFERENCES entity(id) ON DELETE SET NULL,
    speaker_raw  TEXT NOT NULL,
    parenthetical TEXT,
    text         TEXT NOT NULL,
    order_in_scene INTEGER NOT NULL,
    start_offset INTEGER,
    end_offset   INTEGER
);

CREATE INDEX idx_dialogue_scene ON dialogue_line(scene_id, order_in_scene);

CREATE TABLE relationship (
    id            TEXT PRIMARY KEY,
    project_id    TEXT NOT NULL REFERENCES project(id) ON DELETE CASCADE,
    from_entity_id TEXT NOT NULL REFERENCES entity(id) ON DELETE CASCADE,
    to_entity_id  TEXT NOT NULL REFERENCES entity(id) ON DELETE CASCADE,
    relationship_type TEXT NOT NULL
        CHECK (relationship_type IN ('FAMILY','ROMANTIC','AUTHORITY',
                                     'EMPLOYMENT','ALLIANCE','CONFLICT',
                                     'OWNERSHIP','OTHER')),
    description   TEXT,
    information_status TEXT NOT NULL DEFAULT 'INFERENCE'
        CHECK (information_status IN ('FACT','INFERENCE','APPROVED',
                                      'REJECTED','OVERRIDDEN','UNKNOWN')),
    confidence    REAL
);

-- ------------------------------------------------------------------ states

-- A State is story and continuity truth. It exists independently of any
-- Asset, and Module 01 never creates assets.
CREATE TABLE state (
    id           TEXT PRIMARY KEY,
    entity_id    TEXT NOT NULL REFERENCES entity(id) ON DELETE CASCADE,
    name         TEXT NOT NULL,
    description  TEXT,
    persistence_type TEXT NOT NULL DEFAULT 'UNCERTAIN'
        CHECK (persistence_type IN ('SCENE_LOCAL','PERSISTENT',
                                    'PERSISTENT_UNTIL_CHANGED','UNCERTAIN')),
    information_status TEXT NOT NULL DEFAULT 'INFERENCE'
        CHECK (information_status IN ('FACT','INFERENCE','APPROVED',
                                      'REJECTED','OVERRIDDEN','UNKNOWN')),
    confidence   REAL,
    created_at   TEXT NOT NULL
);

-- D-008: the scenes a state holds in are enumerated explicitly. There is no
-- valid_from/valid_to, because script order is not story order — a numeric
-- range would silently assert the present-day state inside a flashback.
CREATE TABLE state_scene (
    state_id     TEXT NOT NULL REFERENCES state(id) ON DELETE CASCADE,
    scene_id     TEXT NOT NULL REFERENCES scene(id) ON DELETE CASCADE,
    information_status TEXT NOT NULL DEFAULT 'INFERENCE'
        CHECK (information_status IN ('FACT','INFERENCE','APPROVED',
                                      'REJECTED','OVERRIDDEN','UNKNOWN')),
    confidence   REAL,
    PRIMARY KEY (state_id, scene_id)
);

CREATE INDEX idx_state_scene_scene ON state_scene(scene_id);

-- Categories are seeded as reference data, not as a CHECK constraint: the
-- module spec requires the list to stay extensible.
CREATE TABLE state_event_category (
    code        TEXT PRIMARY KEY,
    applies_to  TEXT NOT NULL,
    description TEXT
);

CREATE TABLE state_event (
    id           TEXT PRIMARY KEY,
    entity_id    TEXT NOT NULL REFERENCES entity(id) ON DELETE CASCADE,
    scene_id     TEXT NOT NULL REFERENCES scene(id) ON DELETE CASCADE,
    event_type   TEXT NOT NULL,
    description  TEXT,
    persistence_estimate TEXT
        CHECK (persistence_estimate IN ('SCENE_LOCAL','PERSISTENT',
                                        'PERSISTENT_UNTIL_CHANGED',
                                        'UNCERTAIN')),
    -- The state this event brings into effect, once resolved.
    resulting_state_id TEXT REFERENCES state(id) ON DELETE SET NULL,
    information_status TEXT NOT NULL DEFAULT 'INFERENCE'
        CHECK (information_status IN ('FACT','INFERENCE','APPROVED',
                                      'REJECTED','OVERRIDDEN','UNKNOWN')),
    confidence   REAL,
    created_at   TEXT NOT NULL
);

CREATE INDEX idx_state_event_entity ON state_event(entity_id);
CREATE INDEX idx_state_event_scene ON state_event(scene_id);

-- D-007: carries provenance, so the system can tell which links it may
-- recompute and which were the user's deliberate decision.
CREATE TABLE continuity_dependency (
    id              TEXT PRIMARY KEY,
    project_id      TEXT NOT NULL REFERENCES project(id) ON DELETE CASCADE,
    source_scene_id TEXT NOT NULL REFERENCES scene(id) ON DELETE CASCADE,
    target_scene_id TEXT NOT NULL REFERENCES scene(id) ON DELETE CASCADE,
    entity_id       TEXT NOT NULL REFERENCES entity(id) ON DELETE CASCADE,
    state_property  TEXT,
    dependency_type TEXT NOT NULL,
    information_status TEXT NOT NULL DEFAULT 'INFERENCE'
        CHECK (information_status IN ('FACT','INFERENCE','APPROVED',
                                      'REJECTED','OVERRIDDEN','UNKNOWN')),
    confidence      REAL,
    is_stale        INTEGER NOT NULL DEFAULT 0,
    created_at      TEXT NOT NULL
);

CREATE INDEX idx_continuity_target ON continuity_dependency(target_scene_id);

-- ------------------------------------------------------------ requirements

-- Module 01 records that an asset will be needed. It never creates one.
CREATE TABLE asset_requirement (
    id                   TEXT PRIMARY KEY,
    project_id           TEXT NOT NULL REFERENCES project(id) ON DELETE CASCADE,
    entity_id            TEXT NOT NULL REFERENCES entity(id) ON DELETE CASCADE,
    state_id             TEXT REFERENCES state(id) ON DELETE SET NULL,
    asset_type           TEXT NOT NULL,
    first_needed_scene_id TEXT REFERENCES scene(id) ON DELETE SET NULL,
    last_needed_scene_id  TEXT REFERENCES scene(id) ON DELETE SET NULL,
    -- D-009: production progress, never mixed with information_status.
    production_status    TEXT NOT NULL DEFAULT 'NOT_CREATED'
        CHECK (production_status IN ('NOT_CREATED','IN_PROGRESS','CREATED',
                                     'TESTING','APPROVED','REJECTED',
                                     'SUPERSEDED')),
    created_at           TEXT NOT NULL
);

CREATE TABLE voice_requirement (
    id                   TEXT PRIMARY KEY,
    project_id           TEXT NOT NULL REFERENCES project(id) ON DELETE CASCADE,
    entity_id            TEXT NOT NULL REFERENCES entity(id) ON DELETE CASCADE,
    speaking_scene_count INTEGER NOT NULL DEFAULT 0,
    language             TEXT,
    special_requirements TEXT,
    production_status    TEXT NOT NULL DEFAULT 'NOT_CREATED'
        CHECK (production_status IN ('NOT_CREATED','IN_PROGRESS','CREATED',
                                     'TESTING','APPROVED','REJECTED',
                                     'SUPERSEDED')),
    created_at           TEXT NOT NULL,
    UNIQUE (project_id, entity_id)
);

CREATE TABLE acting_requirement (
    id                TEXT PRIMARY KEY,
    project_id        TEXT NOT NULL REFERENCES project(id) ON DELETE CASCADE,
    entity_id         TEXT NOT NULL REFERENCES entity(id) ON DELETE CASCADE,
    priority          INTEGER NOT NULL DEFAULT 0,
    reason            TEXT,
    production_status TEXT NOT NULL DEFAULT 'NOT_CREATED'
        CHECK (production_status IN ('NOT_CREATED','IN_PROGRESS','CREATED',
                                     'TESTING','APPROVED','REJECTED',
                                     'SUPERSEDED')),
    created_at        TEXT NOT NULL,
    UNIQUE (project_id, entity_id)
);

-- -------------------------------------------------- provenance and gates

-- Answers "skąd PRE wie, że ...?" by pointing at the screenplay itself.
CREATE TABLE source_evidence (
    id            TEXT PRIMARY KEY,
    project_id    TEXT NOT NULL REFERENCES project(id) ON DELETE CASCADE,
    subject_table TEXT NOT NULL,
    subject_id    TEXT NOT NULL,
    scene_id      TEXT REFERENCES scene(id) ON DELETE CASCADE,
    text_span     TEXT NOT NULL,
    start_offset  INTEGER,
    end_offset    INTEGER
);

CREATE INDEX idx_evidence_subject ON source_evidence(subject_table, subject_id);

CREATE TABLE review_flag (
    id          TEXT PRIMARY KEY,
    project_id  TEXT NOT NULL REFERENCES project(id) ON DELETE CASCADE,
    scene_id    TEXT REFERENCES scene(id) ON DELETE CASCADE,
    entity_id   TEXT REFERENCES entity(id) ON DELETE CASCADE,
    category    TEXT NOT NULL,
    question    TEXT NOT NULL,
    evidence    TEXT,
    confidence  REAL,
    status      TEXT NOT NULL DEFAULT 'OPEN'
        CHECK (status IN ('OPEN','RESOLVED','DISMISSED')),
    created_at  TEXT NOT NULL,
    resolved_at TEXT
);

CREATE INDEX idx_review_flag_status ON review_flag(project_id, status);

-- A pending decision gate. Persistent, so closing the app and returning
-- resumes at the same open question (D-004 rule 3).
CREATE TABLE decision_gate (
    id           TEXT PRIMARY KEY,
    project_id   TEXT NOT NULL REFERENCES project(id) ON DELETE CASCADE,
    workflow_step TEXT NOT NULL,
    question     TEXT NOT NULL,
    context      TEXT,
    options      TEXT,
    status       TEXT NOT NULL DEFAULT 'OPEN'
        CHECK (status IN ('OPEN','ANSWERED','CANCELLED')),
    created_at   TEXT NOT NULL
);

CREATE INDEX idx_gate_status ON decision_gate(project_id, status);

-- What was asked, what was chosen, and what it affected (D-004 rule 4).
CREATE TABLE decision (
    id             TEXT PRIMARY KEY,
    project_id     TEXT NOT NULL REFERENCES project(id) ON DELETE CASCADE,
    gate_id        TEXT REFERENCES decision_gate(id) ON DELETE SET NULL,
    question       TEXT NOT NULL,
    answer         TEXT NOT NULL,
    subject_table  TEXT,
    subject_id     TEXT,
    decided_at     TEXT NOT NULL,
    decided_by     TEXT NOT NULL DEFAULT 'user'
);

CREATE TABLE production_log (
    id         TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES project(id) ON DELETE CASCADE,
    event_type TEXT NOT NULL,
    summary    TEXT NOT NULL,
    detail     TEXT,
    created_at TEXT NOT NULL
);

CREATE INDEX idx_production_log_project ON production_log(project_id, created_at);
