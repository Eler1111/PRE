# PRE Prototype v0 — Project Context

## 1. What PRE is

PRE means **Production Reference Environment**.

It is a private AI film-production environment whose purpose is to automate a proven AI-film production methodology derived from production workflows documented in several Higgsfield film projects.

PRE Prototype v0 is not intended to invent a new filmmaking methodology.

Its first purpose is to reproduce the strongest known version of that workflow, automate procedural work around it, and make the process accessible primarily through a Polish-language conversational interface.

The target is not a prompt generator.

The target is:

**screenplay → selected scene → filmed and assembled scene**

---

# 2. Product philosophy

## Chat is the control room

The main interface is a Polish-language chat.

The user should be able to work naturally:

- „Wczytaj scenariusz.”
- „Pokaż sceny.”
- „Pracujemy nad sceną 12.”
- „Przeanalizuj tę scenę.”
- „Jakich assetów brakuje?”
- „Przesuń postać bliżej okna.”
- „Zaproponuj coverage.”
- „Zrób MCU postaci A.”
- „Oceń ten dubel.”
- „Spróbuj jeszcze raz, ale popraw tylko eyeline.”
- „Zmontuj scenę.”

The user should not manually choose agents or skills.

PRE Orchestrator interprets the user's intent and invokes the appropriate internal capability.

---

# 3. Supporting visual modules

Chat remains the main control surface.

Additional modules appear only when useful.

Potential modules include:

- Script Preview
- Scene Analysis
- Assets
- Character States
- Location States
- Prop States
- Voice Bible
- Acting Profiles
- Diagram / Blocking
- Spatial Map
- Coverage
- Shot Cards
- Prompts
- Media / Takes
- Production Log
- Assembly

Later versions may add:

- Coverage Lining
- State Timeline UI
- Animatic
- 3D Blocking
- Advanced Editorial Timeline

These are supporting views, not the primary navigation model.

---

# 4. Overall architecture concept

Conceptually:

User  
↓  
Polish Chat  
↓  
PRE Orchestrator  
↓  
specialized agents/capabilities

Possible internal roles:

- Script / Scene Agent
- Asset Agent
- Acting Agent
- Spatial / Diagram Agent
- Coverage / Shot Agent
- Prompt Agent
- Generation Agent
- Take Supervisor
- Editorial Agent

These roles may use existing skills.

---

# 5. Existing private production skills

Prototype v0 may directly use the existing private production skills:

## LIRA

Image-generation and image-edit prompting.

Used for:

- characters,
- character states,
- locations,
- location states,
- props,
- image edits,
- model routing.

## CINEDANCE

Video prompt construction and audit.

Used for:

- active references,
- spatial blocking,
- first-frame control,
- optics,
- camera,
- action timing,
- physics,
- lighting,
- audio,
- dialogue,
- continuity locks,
- prompt QA.

## ACTING

Character-performance system.

Used for:

- acting master profiles,
- scene adaptation,
- objectives,
- obstacles,
- tactics,
- beats,
- subtext,
- eye-life,
- physical behavior,
- voice identity rules.

## TIG Scene Engine

Used for scene-level dramatic analysis such as:

- Goal,
- Obstacle,
- Tactic,
- Reversal,
- Value Shift,
- scene weaknesses,
- Script Stress Test,
- Director's Read.

## TIG Diagram

Used for complex staging and multi-character spatial control.

## TIG Acting Task

Used for short scene-specific performance tasks and eye-work.

These skills are implementation capabilities, not visible product architecture.

---

# 6. Workflow source

PRE Prototype v0 follows a combined production methodology derived from the workflows documented in the Higgsfield projects **HELL GRIND**, **CULLY HILL BOYS** and **ONEIRIC**.

These project names identify methodological sources only.

They must not become assumptions, entities, fixtures, example data, naming conventions or hard-coded production content inside PRE.

The combined methodology contributes principles including:

- asset-first production,
- descriptors,
- explicit state variants,
- location geography,
- spatial maps,
- prompt skeletons,
- prompt iteration,
- production logs,
- consistency,
- voice locking,
- acting locking,
- preliminary shotlists,
- shot cards,
- state/version management,
- voice/accent conditions,
- asset stress testing,
- Script Stress Test,
- Director's Read,
- Diagram-based staging,
- scene-drama analysis,
- structured scene production,
- parallel editorial supervision.

Prototype v0 should implement this methodology before attempting major redesign.

---

# 7. Full target production workflow

## Global phase

1. Import complete screenplay.
2. Normalize screenplay structure.
3. Analyze all scenes.
4. Build Scene Index.
5. Build Entity Registry.
6. Detect story chronology.
7. Detect state-changing events.
8. Build State Timelines.
9. Build Continuity Dependencies.
10. Build Asset Requirement Plan.

No visual assets are generated yet.

## Scene production phase

11. User selects a scene.
12. PRE loads global context relevant to that scene.
13. Run Script Stress Test.
14. Run Director's Read.
15. Perform scene breakdown.
16. Determine required entity states.
17. Check existing approved assets.
18. Create missing assets only when required.
19. Stress-test important assets.
20. Lock/reuse Voice Bible entries.
21. Lock/reuse Acting Master Profiles.
22. Build scene spatial map.
23. Build blocking.
24. Use Diagram Skill if staging requires it.
25. Design coverage.
26. Create Shot Cards.
27. Build final video prompts through CINEDANCE.
28. Generate shots automatically where integrations allow.
29. For manual external steps, PRE prepares exact instructions and required files.
30. Import generated takes.
31. Evaluate and log takes.
32. Iterate surgically.
33. Select approved takes.
34. Assemble the scene.
35. Identify coverage holes or failed shots.
36. Generate replacements or missing shots.
37. Produce finished scene.

---

# 8. Global screenplay analysis principle

PRE must analyze the complete screenplay before serious scene production.

This does not mean all production assets are created upfront.

The purpose is to understand the complete continuity structure of the film.

Global analysis identifies:

- all scenes,
- recurring characters,
- recurring locations,
- props and vehicles,
- story chronology,
- costume changes,
- injuries,
- blood,
- wetness,
- dirt,
- transformations,
- location damage,
- weather variants,
- time-of-day variants,
- prop damage or disappearance,
- other persistent state changes.

This allows PRE to understand future production needs before generating assets.

---

# 9. State before Asset

This is a fundamental architectural rule.

Hierarchy:

Entity  
→ State  
→ Asset

Neutral example:

Entity:

`CHARACTER_01`

Possible States:

- `CHARACTER_01_STATE_01` — Costume A / Clean
- `CHARACTER_01_STATE_02` — Costume A / Wet
- `CHARACTER_01_STATE_03` — Costume B / Clean
- `CHARACTER_01_STATE_04` — Costume B / Visible Injury

These states are screenplay/continuity concepts.

They may all be known after Global Script Analysis.

The corresponding visual assets may not yet exist.

An asset is created only when production reaches a scene requiring that state.

---

# 10. Lazy asset generation

Asset creation happens on demand.

Example:

Scene 9 requires:

`CHARACTER_01_STATE_02`

PRE checks:

`AssetRequirement → NOT_CREATED`

PRE begins the appropriate asset-generation workflow.

Later Scene 10 requires the same state.

PRE checks:

`CHARACTER_01_STATE_02 → approved asset exists`

The existing asset is reused.

This prevents unnecessary generation and improves continuity.

---

# 11. Asset-first production still applies

Lazy asset generation does not mean generating shots without preparation.

Before a production shot can use an entity, the required asset must exist, be versioned and, where necessary, approved/stress-tested.

The sequence is:

state requirement known globally  
→ scene becomes active  
→ required asset generated  
→ asset validated  
→ production shot generated

---

# 12. Project data model

Conceptually, the persistent project contains:

- Project
- Script
- Scene
- Entity
- Character
- Location
- Prop
- Vehicle
- Animal
- State
- StateEvent
- EntityAppearance
- Relationship
- ContinuityDependency
- AssetRequirement
- Asset
- AssetVersion
- VoiceRequirement
- VoiceProfile
- ActingRequirement
- ActingProfile
- SpatialMap
- Diagram
- CoveragePlan
- Shot
- ShotCard
- Prompt
- PromptVersion
- Take
- TakeEvaluation
- Decision
- ReviewFlag
- ProductionLog
- Assembly

The exact database schema may evolve.

The conceptual distinctions should remain stable.

---

# 13. Information provenance

PRE must distinguish what is known from what is inferred.

## FACT

Explicitly supported by screenplay or imported project source.

## INFERENCE

Derived by AI/system reasoning.

## APPROVED

Accepted by the user or authorized production workflow as project truth.

## REJECTED

Explicitly rejected.

## OVERRIDDEN

Previously valid but superseded.

## UNKNOWN

Unresolved.

This distinction is especially important for continuity and state propagation.

---

# 14. Confidence

AI-generated inferences may include a confidence estimate internally.

Confidence should help determine whether PRE:

- proceeds automatically,
- presents a suggestion,
- asks the user for a creative or continuity decision.

Confidence must not convert inference into fact.

---

# 15. Script order vs story chronology

PRE must not assume that screenplay scene order equals chronological story order.

The system should support at least:

- Script Order
- Story / Continuity Order

This is necessary for:

- flashbacks,
- flashforwards,
- dreams,
- imagined sequences,
- parallel action,
- framing stories.

State propagation should follow continuity logic, not blindly follow scene numbers.

---

# 16. Chat and project state

Conversation history is not the authoritative project memory.

Neutral example:

User:

„Przesuń CHARACTER_01 bliżej okna.”

Correct system behavior:

1. interpret command,
2. update relevant project object,
3. determine dependent objects,
4. mark affected downstream data if necessary,
5. confirm result in Polish chat.

The change must survive restarting the application.

Therefore:

**Chat operates on project state. Chat does not store project state.**

---

# 17. Project directory

Conceptual project structure:

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

Structured relationships live in `project.db`.

Media remains as normal files.

Do not store large binary media inside the database unless later testing provides a compelling reason.

---

# 18. Automation policy

Automate all procedural work that does not require an artistic decision.

Examples:

- creating IDs,
- naming/tagging,
- versioning,
- maintaining state ranges,
- copying stable descriptors,
- checking missing assets,
- tracking prompt versions,
- logging takes,
- reusing voice locks,
- continuity warnings,
- preparing generation packages,
- marking stale dependent data.

The user should primarily decide:

- interpretation,
- staging preferences,
- performance direction,
- coverage choices when artistically ambiguous,
- selection among meaningful alternatives,
- approval/rejection of generated material.

---

# 19. External generation

PRE should support two generation modes.

## Integrated mode

If a model/API is programmatically available, PRE can submit the generation and import the result automatically.

## Assisted manual mode

If generation requires an external web interface or subscription feature:

PRE prepares:

- exact model to use,
- configured workflow note where relevant,
- required reference files,
- exact prompt,
- parameters,
- generation instructions.

The user performs the external step and imports the result back into PRE.

The rest of the workflow continues normally.

---

# 20. Provider independence

Prototype v0 may begin with Claude and Higgsfield-centric integrations.

However:

- domain objects must remain provider-independent,
- project state must remain provider-independent,
- state/continuity logic must remain provider-independent,
- shot cards must remain provider-independent where practical.

Provider-specific prompt compilers and adapters should sit below the domain layer.

Possible future adapters:

- ClaudeAdapter
- OpenAIAdapter
- HiggsfieldAdapter
- LocalModelAdapter
- OtherProviderAdapter

---

# 21. Neutrality of examples and tests

PRE is a general film-production system.

Permanent specifications, schemas, fixtures and automated tests must not depend on characters, locations, props or events from any real or active production.

Use neutral synthetic identifiers or deliberately invented fixture content, for example:

- `CHARACTER_01`
- `CHARACTER_02`
- `LOCATION_01`
- `PROP_01`
- `VEHICLE_01`

Synthetic test screenplays should be designed specifically to exercise functionality such as:

- recurring entities,
- costume changes,
- wetness,
- injury,
- prop continuity,
- location variants,
- flashbacks,
- ambiguity.

No production-specific character or location should become a default assumption in code.

---

# 22. Prototype success criterion

PRE Prototype v0 succeeds when:

1. a complete screenplay can be imported,
2. PRE understands its scene/entity/state structure,
3. the user can select a scene,
4. PRE prepares the scene following the adopted workflow,
5. required assets are created or reused,
6. blocking and coverage are established,
7. shot prompts are generated,
8. takes are generated/imported and evaluated,
9. selected takes are assembled,
10. the user obtains a coherent filmed version of the selected scene.

A polished dashboard without this complete path is not a successful prototype.