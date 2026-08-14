# PRE Prototype v0 — Claude Code Instructions

## Project

PRE = Production Reference Environment.

PRE is a private AI film-production environment designed to automate a proven AI-film production workflow derived from methodologies documented in several Higgsfield film projects.

Prototype v0 must reproduce that workflow as faithfully as practical, while automating procedural work and exposing the system primarily through a Polish-language chat interface.

Do not redesign the production methodology merely because another architecture appears cleaner.

First reproduce and automate the proven workflow. Improvements may be introduced later only when testing demonstrates a concrete advantage.

---

## Primary product goal

The prototype must ultimately allow the user to:

1. import a complete screenplay,
2. analyze the whole screenplay,
3. select a scene,
4. prepare all required production elements,
5. design blocking and coverage,
6. generate shots,
7. review and iterate takes,
8. assemble selected takes,
9. obtain a filmed version of the scene.

Everything built in the prototype must serve this path.

---

## Core workflow

Screenplay Import  
→ Global Script Analysis  
→ Entity / State / Continuity Model  
→ Scene Selection  
→ Script Stress Test  
→ Director's Read  
→ Scene Breakdown  
→ Asset Preparation  
→ Asset Stress Test  
→ Voice Lock  
→ Acting Profile  
→ Spatial Map / Blocking  
→ Diagram when needed  
→ Coverage  
→ Shot Cards  
→ CINEDANCE Prompt  
→ Generation  
→ Take Supervision  
→ Assembly  
→ Finished Scene

---

## Non-negotiable principles

### 1. Chat-first

The primary user interface is a Polish-language chat.

The user should not need to know which agent or skill is being used.

Visual modules are secondary surfaces used when useful.

### 2. Polish-first UI

User interface and user-facing communication are in Polish.

Film dialogue is Polish by default unless the project specifies another language.

Internal technical prompts may use English when required by models or skills.

### 3. Analyze the whole screenplay

PRE analyzes the complete screenplay before production of an individual scene.

Global analysis creates the film model, continuity information, state requirements and production requirements.

### 4. Do not generate all assets globally

Global screenplay analysis identifies required states and asset requirements.

Actual visual assets are generated lazily, scene by scene, when a required state is first needed.

### 5. State exists before Asset

Fundamental hierarchy:

Entity  
→ State  
→ Asset

A State is story and continuity truth.

An Asset is a production representation of that state.

Never infer project truth solely from existing media files.

### 6. Project state is not chat history

Chat operates on project state.

Chat does not store project state.

Persistent project data must be stored in the project model/database.

### 7. `project.db` is the structured source of truth

Store structured project information in the project database.

Media files remain normal files in the project directory.

### 8. Preserve the adopted production workflow

Prototype v0 must preserve:

- asset-first production before production-shot generation,
- explicit state variants,
- stable descriptors,
- locked voice identity,
- acting as behavior and task rather than emotion labels,
- explicit spatial geography,
- diagram-based staging when useful,
- independently complete shot prompts,
- surgical prompt iteration,
- prompt and take version logging,
- simplification or redesign of shots that repeatedly fail,
- editorial work running in parallel with generation.

### 9. Automate procedural work

Automate whenever possible:

- IDs,
- tags,
- versions,
- descriptor reuse,
- state tracking,
- continuity dependencies,
- missing asset detection,
- voice block reuse,
- shot card creation,
- prompt assembly,
- audits,
- production logs,
- take status.

Keep human intervention primarily at creative decision gates.

### 10. Provider-independent domain model

Prototype v0 may heavily use Claude and Higgsfield.

Do not bake Claude-specific or Higgsfield-specific assumptions into permanent domain entities.

Provider/model integrations must be replaceable adapters.

---

## Skills available to the project

Existing private production skills may be used as internal capability modules:

- LIRA
- CINEDANCE
- ACTING
- TIG Scene Engine
- TIG Diagram
- TIG Acting Task

Do not expose these as mandatory user-facing workflow choices.

The Orchestrator decides when they are needed.

---

## Development rules

- Prefer explicit structured data over hidden conversational memory.
- Do not silently mutate screenplay source text.
- Preserve original imported files.
- Every inferred fact must be distinguishable from screenplay facts and approved production decisions.
- Every important change should be traceable.
- Avoid generic dashboard features that do not directly serve the production workflow.
- Do not create premature abstractions for features not yet needed.
- Build vertical working slices.
- Add tests for continuity, state propagation and project persistence early.
- Do not automatically freeze AI inference as project truth.
- Permanent code, schemas, fixtures and tests must remain independent of any specific film production.

---

## Information status

Where relevant, project information must distinguish:

- `FACT` — explicitly supported by screenplay/source material.
- `INFERENCE` — derived by AI or system logic.
- `APPROVED` — explicitly accepted as production truth.
- `REJECTED` — explicitly rejected.
- `OVERRIDDEN` — replaced by a later decision.
- `UNKNOWN` — unresolved.

---

## Current development priority

The first module is:

**Module 01 — Global Script Analyzer**

Its purpose is to import the complete screenplay and build the initial global film model:

- scenes,
- entities,
- appearances,
- dialogue,
- states,
- state events,
- continuity dependencies,
- asset requirements,
- review flags.

It must not generate visual assets.

Read:

`docs/PRE_PROJECT_CONTEXT.md`

and:

`docs/modules/01_global_script_analyzer.md`

before implementing Module 01.