# PRE — Architecture Audit & Open Decisions

Status: working document, produced from a read-through of `CLAUDE.md`,
`docs/PRE_PROJECT_CONTEXT.md`, `docs/modules/01_global_script_analyzer.md`,
the three Higgsfield production briefs (`docs/references/`) and the six
production skills (`docs/skills/`).

This is not a spec. It is a list of contradictions, missing decisions and
ambiguities to resolve before Module 01 (Global Script Analyzer) is
implemented, and before the Orchestrator/skill-invocation architecture is
designed.

---

## 1. Contradictions in the base spec (CLAUDE.md / PRE_PROJECT_CONTEXT.md / Module 01)

### 1.1 Entity model: unified table vs. per-type tables
`01_global_script_analyzer.md` §8 mandates one `Entity` table with an
`entity_type` discriminator ("Do not create separate incompatible state
mechanisms per entity type"). `PRE_PROJECT_CONTEXT.md` §12 lists `Entity`
**and separately** `Character`, `Location`, `Prop`, `Vehicle`, `Animal` as if
they were distinct tables. Needs a decision: single table + discriminator,
or `Entity` + per-type extension tables.

### 1.2 `EntityAlias` missing from the master data model
`01_global_script_analyzer.md` §39 requires persisting `EntityAliases`, but
`PRE_PROJECT_CONTEXT.md` §12 does not list it. The master list needs the
addition.

### 1.3 `ContinuityDependency` has no provenance fields
`PRE_PROJECT_CONTEXT.md` §13 says the FACT/INFERENCE distinction is
"especially important for continuity and state propagation," yet
`ContinuityDependency` (§21) has only a bare `status` field — no
`information_status`, no `confidence`.

### 1.4 `State.valid_from/valid_to` as scene ranges vs. non-linear chronology
The worked example in §20 shows state validity as contiguous scene ranges
("Scenes 1–8"), but §7 and `PRE_PROJECT_CONTEXT.md` §15 both say state
propagation must not rely on script order, because of flashbacks/parallel
action. Needs an explicit representation (story_order? explicit scene-id
sets?) instead of a naive numeric range.

### 1.5 Overloaded/duplicated status fields
`State` carries `information_status`, `confidence`, **and**
`approval_status` — the relationship between the global `information_status`
enum (FACT/INFERENCE/APPROVED/REJECTED/OVERRIDDEN/UNKNOWN) and the separate
per-object `status` fields on `AssetRequirement`, `ReviewFlag`,
`VoiceRequirement`, `ActingRequirement`, `ContinuityDependency` is never
defined. Same enum reused? Independent state machines per object?

---

## 2. What the skills resolved from the original open questions

### 2.1 Skill runtime mechanism — resolved
The six skills are literal Claude Agent Skills (`SKILL.md`, some packaged as
`.skill` ZIP bundles with a `references/` folder), with YAML frontmatter
(`name`, `description`) written for **automatic triggering by Claude** based
on intent-matching phrases in `description`. This fixes the architecture
question from the first audit: **PRE's backend must run on Claude (Agent
SDK / Messages API with skills)**, not a generic/provider-neutral LLM
orchestration layer for this capability. The Orchestrator either lets Claude
select skills itself, or explicitly loads the right `SKILL.md` (+
`references/`) into a call's context per task type.

### 2.2 LIRA/CINEDANCE context separation — confirmed intentional
Cully Hill Boys brief, verbatim: *"We split them because the rules of one
job poison the other."* LIRA = image prompts only, CINEDANCE = video prompts
only. The Orchestrator must never merge them into one call/context.

### 2.3 Provider independence of the domain layer — reinforced, not new
LIRA and CINEDANCE are deeply Higgsfield/Seedance-specific (`@tags`, Soul
ID, FOV-in-degrees, NBP CHANGE/PRESERVE blocks). This confirms — it doesn't
change — the existing rule: this vocabulary must live only inside generated
`Prompt`/`PromptVersion` content, never inside the domain schema
(`Scene`, `Entity`, `State`, `Asset`, `Shot`).

---

## 3. New findings from the skill files themselves

### 3.1 ACTING vs. TIG Acting Task — two systems, unclear division of labor
`docs/skills/acting/SKILL.md` defines its own five pillars (Objective /
Obstacle & stakes / Tactics / Beats / Subtext) and a "master profile" format
(one 150–220 word paragraph, written once, then rewritten per scene — see
its §8 "Scene adaptation").

`docs/skills/tig-acting-task/SKILL.md` defines a **different** vocabulary
(Scene Direction / Motive / Goal / Obstacle / Tactic) and its own prompt
block (`ACTING TASK — [NAME]`), explicitly marked as bespoke: *"do NOT
substitute textbook craft definitions."* Its own description calls it
*"Companion to tig-scene-engine (structure level); this skill is the
performance level."*

The Oneiric brief's worked example (§06) uses the TIG Acting Task block
format, not the ACTING skill's prose-paragraph scene-adaptation format —
implying TIG Acting Task **replaces** ACTING §8 (scene adaptation) in
practice, while ACTING's master profile (identity, voice, physical habits)
stays the layer underneath it. **This division is never stated explicitly
anywhere in the source material — it is inferred.** Decision needed: confirm
(or reject) this two-layer model — ACTING = permanent identity, TIG Acting
Task = per-scene tactic — before building an Acting Agent.

### 3.2 "Director's Read" has no explicit skill mapping
CLAUDE.md / `PRE_PROJECT_CONTEXT.md` name "Script Stress Test" and
"Director's Read" as two workflow steps. Script Stress Test clearly maps to
TIG Scene Engine's AUDIT mode (Goal/Obstacle/Tactic/Reversal/Value Shift).
"Director's Read" most likely maps to TIG Acting Task §0–§1c (naming the
scene's one shared event and each character's physical channel through it —
matches the Oneiric brief's own description of "the director's read" in
§01 almost verbatim). But no source document states this mapping directly.
Needs confirmation before writing a spec for these two workflow phases.

### 3.3 No single canonical CINEDANCE prompt skeleton
Three different block lists exist:
- `docs/skills/cinedance/SKILL.md` (the actual skill, v4): 11 sections —
  SCENE CONTEXT · ACTIVE REFERENCES · LOCATION MAP · FIRST FRAME AND
  SPATIAL BLOCKING · FORMAT MODE · OPTICS · CAMERA · ACTION TIMING ·
  PHYSICS · LIGHTING · AUDIO · POSITIVE CONSTRAINTS. **No CHARACTER ACTING,
  no STYLE, no QUALITY.**
- Hell Grind / Cully Hill Boys production examples: 15 sections, including
  CHARACTER ACTING, STYLE (a fixed per-project Style Prefix), and QUALITY.
- Oneiric: yet another variant (adds GAZE/EYELINES, SEGMENTS, DIALOGUE as
  named sections).

A Prompt Agent implementation needs one canonical section list. Likely
answer: the v4 skill's 11 sections as the base + CHARACTER ACTING (fed by
the Acting Agent) + STYLE (per-project constant) as PRE-level additions on
top of what the skill emits — but this needs to be a deliberate decision,
not an accident of which example got copied first.

### 3.4 No single canonical asset-tag naming convention
Three conventions appear in practice:
- Hell Grind: `@roco`, `@loc_cave_front` — no project code, no version.
- Cully Hill Boys / Oneiric: `@char_CB_Kel_v9`,
  `@loc_ON_dorm_commonroom_front_s2` — `type_PROJECT_name_scene_version`.
- TIG Diagram (`tig-blocking-map`): `@staging_[PROJECT]_[scene]_[version]`,
  with `[PROJECT]` in ALL CAPS.

Per the Module 01 automation principle ("automate IDs, tags, versions"),
PRE should generate one deterministic tag scheme system-side (closest to
the Cully Hill Boys/Oneiric pattern) rather than let it be invented per
project. This is a concrete decision to make now, not later — it affects
the `Asset`/`AssetVersion` schema.

### 3.5 TIG Scene Engine can rewrite screenplay text (WRITE mode)
`docs/skills/tig-scene-engine/SKILL.md` has a WRITE/CO-WRITE mode that
outputs new scenes in Final Draft screenplay format. This runs directly
against CLAUDE.md's rule "Do not silently mutate screenplay source text" /
"Preserve original imported files." **Missing concept in the data model:**
a screenplay revision/proposal object — any WRITE-mode output must be
staged as a proposal requiring explicit user approval before it can affect
`Script.raw_text`, and if approved, must create a new tracked version, never
an in-place edit. Nothing in Module 01's schema (§39) currently accounts for
this.

### 3.6 TIG Scene Engine needs a project-level "story goal"
Its own AUDIT procedure says: *"If you don't know the story goal, ask for
it — you can't fully audit Goal without it."* `PRE_PROJECT_CONTEXT.md` §12
has no field for a top-level dramatic goal/logline. Without it, the
Orchestrator has to re-ask the user every time this skill runs. Needs a
field, likely on `Project`.

### 3.7 TIG Diagram is a stateful, two-step, human-in-the-loop process
Step 1 (Claude writes a diagram-generation prompt) and step 2 (Claude binds
colors to character tags) are separated by a **manual step outside
Claude**: the user must generate the actual diagram image in Seedream / Nano
Banana / ChatGPT and bring it back. This is not a single function call — the
Orchestrator needs to model it as a process with a checkpoint (skill must
not proceed to step 2 until the generated image is provided), which has no
equivalent anywhere yet in the domain model (closest concept:
`Diagram`, listed in `PRE_PROJECT_CONTEXT.md` §12, but with no state
machine).

---

## 4. Priority for resolution

Blocking for Module 01 schema specifically: **1.1, 1.2, 1.3, 1.4, 1.5**.

Blocking for the Orchestrator / skill-invocation layer (not Module 01, but
next after it): **2.1, 3.1, 3.2, 3.3, 3.4, 3.7**.

New data-model concepts surfaced, not yet speced anywhere: **3.5 (script
revision/proposal), 3.6 (story goal / logline field)**.
