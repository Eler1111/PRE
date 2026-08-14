# Module 01 — Global Script Analyzer

## Status

Prototype v0 / first implementation module.

## Purpose

Global Script Analyzer imports and analyzes the complete screenplay before individual scene production begins.

Its purpose is to build the initial global model of the film.

The module identifies:

- scenes,
- entities,
- appearances,
- dialogue,
- story chronology,
- state-changing events,
- states,
- continuity dependencies,
- production requirements,
- ambiguities requiring review.

It does **not** generate character sheets, locations, props, video or audio assets.

---

# 1. Primary workflow

Input screenplay  
↓  
File preservation  
↓  
Parsing  
↓  
Normalization  
↓  
Scene Index  
↓  
Entity Detection  
↓  
Entity Resolution  
↓  
State Event Detection  
↓  
State Timeline Construction  
↓  
Continuity Analysis  
↓  
Asset Requirement Plan  
↓  
Review Flags  
↓  
Persist to `project.db`

---

# 2. Input

Initial implementation should support at least one reliable screenplay input format.

Preferred priority:

1. Fountain / structured plain text
2. TXT
3. PDF
4. FDX
5. DOCX

Do not block prototype development on supporting every format.

Architecture must allow import adapters.

Possible interface:

`ScriptImporter`

with implementations such as:

- `FountainImporter`
- `TextImporter`
- `PdfImporter`
- `FdxImporter`
- `DocxImporter`

The original imported file must always be preserved unchanged.

---

# 3. Script object

Create a normalized internal Script representation.

Conceptually:

```text
Script
- id
- project_id
- title
- source_file
- source_format
- imported_at
- raw_text
- normalized_text
- parse_status
- analysis_status
```

The original source remains authoritative for original screenplay content.

---

# 4. Scene parsing

The module identifies every screenplay scene.

Conceptual Scene structure:

```text
Scene
- id
- script_id
- scene_number
- script_order
- heading_raw
- int_ext
- location_id
- sub_location
- time_of_day
- raw_text
- normalized_text
- chronology_status
- story_order
```

Preserve original scene headings.

Do not rewrite screenplay content.

---

# 5. Scene Index

Build a complete list of scenes.

Neutral example:

```text
SCENA 1
LOCATION_01 / AREA_A
Noc

SCENA 2
LOCATION_02
Noc

SCENA 3
LOCATION_01 / AREA_B
Rano
```

Each Scene must retain a stable internal ID even if display labels later change.

---

# 6. Script Order

Every scene receives explicit screenplay order.

Example:

```text
scene_001 → script_order 1
scene_002 → script_order 2
scene_003 → script_order 3
```

Never use database insertion order as screenplay order.

---

# 7. Story / Continuity Order

The Analyzer should attempt to identify non-linear chronology.

Possible values:

```text
LINEAR
FLASHBACK
FLASHFORWARD
DREAM
IMAGINED
PARALLEL
UNKNOWN
```

Do not silently force uncertain scenes into chronological order.

Store ambiguous chronology as an inference or ReviewFlag.

State propagation must not rely only on script order.

---

# 8. Entity model

All meaningful persistent production subjects derive conceptually from Entity.

```text
Entity
- id
- project_id
- entity_type
- canonical_name
- display_name
- description
- status
```

Initial entity types:

```text
CHARACTER
LOCATION
PROP
VEHICLE
ANIMAL
OTHER
```

Do not create separate incompatible state mechanisms per entity type.

---

# 9. Character Registry

Detect characters across the entire screenplay.

Neutral example:

```text
CHARACTER_01

aliases:
- CHARACTER A
- THE DRIVER

appears:
1, 3, 4, 7, 11

speaks:
1, 3, 7
```

Create stable canonical entity IDs.

---

# 10. Entity aliases and resolution

The Analyzer should detect probable aliases.

Multiple screenplay labels may refer to the same entity.

Entity merges must preserve original mentions.

Do not automatically merge low-confidence aliases into approved canonical identity.

Use:

- FACT where explicit,
- INFERENCE where likely,
- ReviewFlag where uncertain.

---

# 11. Entity Appearance

Track where each entity appears.

Conceptual structure:

```text
EntityAppearance
- id
- scene_id
- entity_id
- appearance_type
- source_span
- information_status
```

Possible appearance types:

```text
VISIBLE
OFFSCREEN
MENTIONED
DIALOGUE_ONLY
VOICE_ONLY
UNKNOWN
```

This will later help scene breakdown and asset loading.

---

# 12. Location Registry

Normalize recurring locations.

Support hierarchy where useful.

Neutral example:

```text
LOCATION_01
├── AREA_A
├── AREA_B
├── AREA_C
└── AREA_D
```

Do not assume differently worded location headings necessarily represent different physical locations.

Do not automatically merge ambiguous places.

---

# 13. Props and production-significant objects

Detect objects likely to matter for production.

Prioritize objects that are:

- handled,
- carried,
- transferred,
- opened,
- read,
- worn,
- broken,
- damaged,
- lost,
- recovered,
- shown closely,
- plot-relevant,
- present across multiple scenes.

Do not create asset requirements for every incidental object mentioned in prose.

---

# 14. State model

A State represents the condition of an Entity during part of the story.

Conceptually:

```text
State
- id
- entity_id
- name
- valid_from
- valid_to
- persistence_type
- information_status
- confidence
- approval_status
```

The exact schema may evolve.

Core rule:

**State exists independently of Asset.**

---

# 15. State Events

Detect events that change an entity's state.

Conceptual structure:

```text
StateEvent
- id
- entity_id
- scene_id
- event_type
- description
- source_span
- persistence_estimate
- information_status
- confidence
```

---

# 16. Character State Event categories

At minimum detect or support:

```text
COSTUME_CHANGE
WETNESS
BLOOD
INJURY
DIRT
HAIR_CHANGE
MAKEUP_CHANGE
AGING
PHYSICAL_TRANSFORMATION
DISGUISE
UNIFORM_CHANGE
CARRIED_OBJECT_CHANGE
MISSING_OBJECT
OTHER
```

Do not make the category list impossible to extend.

---

# 17. Location State Event categories

At minimum support:

```text
TIME_OF_DAY
WEATHER
SEASON
DAMAGE
DESTRUCTION
FIRE
FLOOD
OCCUPATION
FURNITURE_CHANGE
DECORATION_CHANGE
CONSTRUCTION_STATE
LIGHTING_STATE
OTHER
```

---

# 18. Prop / Vehicle State Event categories

At minimum support:

```text
INTACT
DAMAGED
OPEN
CLOSED
FULL
EMPTY
CLEAN
DIRTY
BLOODIED
BURNED
BROKEN
MISSING_COMPONENT
LOCATION_CHANGE
OWNERSHIP_CHANGE
OTHER
```

---

# 19. Persistence

The system must distinguish state persistence.

Suggested values:

```text
SCENE_LOCAL
PERSISTENT
PERSISTENT_UNTIL_CHANGED
UNCERTAIN
```

Example:

A character holding a glass is usually scene-local.

A visible injury may persist across multiple scenes.

Do not propagate temporary physical actions as persistent state without evidence.

---

# 20. State Timeline

Build proposed state timelines for each persistent entity.

Neutral example:

```text
CHARACTER_01

STATE 01
Scenes 1–8
Costume A
Clean

EVENT
Scene 9
Falls into water

STATE 02
Scenes 9–11
Costume A
Wet

EVENT
Scene 12
Changes clothes

STATE 03
Scenes 12–20
Costume B
Clean

EVENT
Scene 21
Visible injury

STATE 04
Scenes 21–27
Costume B
Visible injury
```

The timeline may initially contain INFERENCE states.

Do not automatically mark inferred state ranges APPROVED.

---

# 21. Continuity Dependency

Create dependencies when one event influences later scenes.

Conceptual structure:

```text
ContinuityDependency
- id
- source_scene_id
- target_scene_id
- entity_id
- state_property
- dependency_type
- status
```

If a source decision later changes, dependent scene data can be marked stale or requiring review.

---

# 22. Information status

Every non-trivial extracted or inferred claim must support provenance status.

Values:

```text
FACT
INFERENCE
APPROVED
REJECTED
OVERRIDDEN
UNKNOWN
```

### FACT

Directly supported by screenplay text.

### INFERENCE

Derived by model/system reasoning.

### APPROVED

Accepted production truth.

### REJECTED

Explicitly rejected.

### OVERRIDDEN

Replaced by later approved information.

### UNKNOWN

Unresolved.

Do not collapse FACT and INFERENCE.

---

# 23. Source evidence

Where practical, extracted facts and important inferences should retain source evidence.

Conceptually:

```text
SourceEvidence
- source_scene_id
- text_span
- start_offset
- end_offset
```

The system should eventually be able to answer:

„Skąd PRE wie, że CHARACTER_01 ma ten stan w tej scenie?”

and point to the relevant screenplay evidence.

---

# 24. Confidence

AI-generated inferences should support confidence.

Confidence is internal decision support.

It may help determine whether PRE:

- proceeds automatically,
- proposes something,
- asks for confirmation.

Do not present fake numerical precision to users unnecessarily.

---

# 25. Review Flags

Create ReviewFlags when important ambiguity cannot be safely resolved.

Conceptual structure:

```text
ReviewFlag
- id
- project_id
- scene_id
- entity_id
- category
- question
- evidence
- confidence
- status
```

Possible statuses:

```text
OPEN
RESOLVED
DISMISSED
```

ReviewFlags should represent real unresolved production questions, not generic AI uncertainty.

---

# 26. Relationships

Detect relationships only when useful and grounded.

Potential relationship types:

```text
FAMILY
ROMANTIC
AUTHORITY
EMPLOYMENT
ALLIANCE
CONFLICT
OWNERSHIP
OTHER
```

A relationship may itself have:

- FACT,
- INFERENCE,
- APPROVED status.

Avoid speculative psychological profiling during global extraction.

---

# 27. Dialogue requirements

Identify:

- speaking characters,
- scenes containing dialogue,
- languages where explicit,
- special accent/dialect requirements where explicit,
- off-screen voice requirements.

Do not generate full Voice Bible profiles during Module 01.

Instead create requirements.

---

# 28. Voice Requirement

Conceptually:

```text
VoiceRequirement
- character_id
- speaking_scene_count
- language
- special_requirements
- status
```

Module 01 only records that a voice profile will later be required.

---

# 29. Acting Requirement

Identify which recurring characters are likely to need an Acting Master Profile.

Do not generate full profiles globally in Module 01.

Conceptually:

```text
ActingRequirement
- character_id
- priority
- reason
- status
```

---

# 30. Asset Requirement Plan

Create requirements for states that will eventually need production assets.

Conceptual structure:

```text
AssetRequirement
- id
- entity_id
- state_id
- asset_type
- first_needed_scene_id
- last_needed_scene_id
- status
```

Initial status:

```text
NOT_CREATED
```

Possible later values:

```text
IN_PROGRESS
CREATED
TESTING
APPROVED
REJECTED
SUPERSEDED
```

Module 01 creates the requirement.

It does not create the asset.

---

# 31. Lazy asset generation rule

When a scene later becomes active:

1. determine required states,
2. query AssetRequirements,
3. locate an existing approved asset,
4. reuse it if available,
5. create a missing asset only if required.

Module 01 must provide enough data for this future behavior.

---

# 32. Production Requirement Summary

At the end of analysis, PRE should be able to summarize structured project data, for example:

```text
Sceny: 84
Postacie: 26
Postacie mówiące: 11
Lokacje: 19
Istotne rekwizyty: 68
Stany postaci: 53
Stany lokacji: 21
Stany rekwizytów: 14
Voice Profiles wymagane: 11
Acting Profiles wymagane: 9
Niejasności continuity: 7
```

These numbers must come from structured data, not a separate LLM summary disconnected from the database.

---

# 33. User-facing completion message

After successful analysis, PRE should provide a concise Polish summary and explicitly state that assets have not yet been generated.

Example:

```text
Scenariusz przeanalizowany.

84 sceny
26 postaci
19 lokacji
68 istotnych rekwizytów
53 wykryte zmiany stanów postaci
21 zmian stanów lokacji
14 zmian stanów rekwizytów
7 niejasności continuity wymagających decyzji.

Nie utworzono jeszcze żadnych assetów.
```

---

# 34. User queries after analysis

The data layer must support future chat commands such as:

```text
Pokaż wszystkie sceny.
```

```text
Pokaż CHARACTER_01.
```

```text
Jakie stany ma CHARACTER_01?
```

```text
W których scenach występuje CHARACTER_02?
```

```text
Pokaż wszystkie niejasności continuity.
```

```text
Jakich assetów wymaga scena 21?
```

The chat layer itself may be implemented separately, but these queries must be straightforward from persisted project data.

---

# 35. Deterministic vs semantic responsibilities

Do not make Global Script Analyzer one giant LLM prompt.

Use deterministic software where possible.

## Deterministic responsibilities

Code should own:

- file handling,
- project creation,
- IDs,
- scene storage,
- ordering,
- database persistence,
- validation,
- versioning,
- relationship integrity,
- schema enforcement,
- source spans where possible,
- status transitions.

## Semantic responsibilities

LLM/agent reasoning may own:

- entity resolution,
- semantic location matching,
- prop significance,
- state-event interpretation,
- persistence inference,
- chronology inference,
- continuity ambiguity detection.

Preferred conceptual pipeline:

```text
SOURCE FILE
↓
PARSER
↓
NORMALIZED SCENES
↓
SEMANTIC ANALYSIS
↓
STRUCTURED OUTPUT
↓
VALIDATOR
↓
PROJECT DATABASE
```

Never rely on:

```text
LLM reads screenplay and simply remembers everything.
```

---

# 36. Structured semantic output

LLM output should be constrained to structured schemas.

Do not parse important production state from unconstrained prose when avoidable.

Use explicit typed outputs for:

- entity candidates,
- alias candidates,
- state events,
- chronology flags,
- relationships,
- continuity flags,
- asset requirements.

Validate every response before persistence.

---

# 37. Incremental processing

Architecture should allow screenplay analysis to be processed scene-by-scene or in chunks while still producing a global model.

Do not require the entire screenplay to fit into a single model request.

After local passes, perform global reconciliation passes for:

- aliases,
- recurring locations,
- state continuity,
- chronology,
- repeated props.

This is important for feature-length scripts.

---

# 38. Re-analysis

The architecture must support future screenplay edits.

Do not assume analysis happens only once.

Eventually, when screenplay text changes, PRE should be able to determine affected scenes and recompute dependent analysis without destroying approved production decisions unnecessarily.

Full implementation of incremental invalidation may be postponed, but schema/design must not make it impossible.

---

# 39. Persistence

All validated Module 01 results must persist in the project database.

At minimum preserve:

- Script
- Scenes
- Entities
- EntityAliases
- EntityAppearances
- States
- StateEvents
- ContinuityDependencies
- Relationships
- AssetRequirements
- VoiceRequirements
- ActingRequirements
- ReviewFlags
- Decisions
- source/provenance information

---

# 40. Project directory behavior

When a new project is created:

```text
Film.pre/
├── project.db
├── Script/
├── Assets/
├── References/
├── States/
├── Diagrams/
├── Shots/
├── Takes/
├── Audio/
├── Video/
├── Animatic/
└── Exports/
```

Module 01 primarily uses:

```text
project.db
Script/
```

Do not create fake placeholder media.

---

# 41. Synthetic acceptance-test screenplay

Create a completely synthetic screenplay fixture specifically for testing Module 01.

It must not reuse characters, locations, props or story events from any real or active production.

It should contain:

- recurring CHARACTER_01,
- recurring CHARACTER_02,
- recurring LOCATION_01,
- costume change,
- water exposure,
- wet state in a later scene,
- injury,
- later treatment or bandage,
- PROP_01 carried across scenes,
- PROP_01 changing condition,
- day/night location variation,
- flashback,
- deliberately ambiguous continuity case.

The fixture exists only to exercise parser and continuity logic.

---

# 42. Acceptance criteria

Module 01 is considered functional when it can:

1. create a PRE project,
2. import the synthetic test screenplay,
3. preserve the original screenplay,
4. parse all scenes,
5. preserve script order,
6. identify recurring characters,
7. resolve obvious aliases,
8. identify recurring locations,
9. identify important props,
10. detect explicit state events,
11. propose persistent states,
12. distinguish flashback chronology from normal progression,
13. build state timelines,
14. build continuity dependencies,
15. create AssetRequirements without creating assets,
16. create ReviewFlags for deliberately ambiguous cases,
17. persist everything,
18. reload the project without losing state,
19. produce the Polish project summary,
20. answer basic structured queries from persisted project data.

---

# 43. Failure conditions

The module is NOT acceptable if:

- screenplay facts exist only in LLM/chat memory,
- state information disappears after restart,
- every noun becomes a production asset,
- AI inference is stored as unquestioned FACT,
- states are derived from existing media files,
- asset files are generated during global analysis,
- flashbacks incorrectly inherit current timeline state,
- aliases create duplicate major characters without review,
- changing conversation context changes stored project truth,
- the system cannot explain screenplay evidence behind major state decisions,
- code or test fixtures become dependent on a specific film production.

---

# 44. Out of scope for Module 01

Do not implement yet:

- image generation,
- LIRA asset prompting,
- asset stress testing,
- Voice Bible generation,
- Acting Master Profile generation,
- Script Stress Test,
- Director's Read,
- Diagram generation,
- Blocking,
- Coverage,
- Shot Cards,
- CINEDANCE video prompts,
- video generation,
- Take Supervisor,
- Assembly,
- advanced timeline UI.

These belong to later modules.

---

# 45. Engineering priority

Build the smallest robust implementation that proves:

**A complete screenplay can be converted into a persistent, queryable film model containing scenes, entities, states and continuity requirements.**

Do not spend the first implementation cycle polishing a dashboard.

The first milestone is a correct film model, not a beautiful interface.