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

### 3.0 Two generations of tooling — not two layers of one system
**RESOLVED — see `DECISIONS.md` D-001 (generation 2 / Oneiric adopted as
canonical) and D-002 (LIRA and the ACTING master-profile/voice layer
retained, because generation 2 has no successor for either).** Kept below
for the reasoning.

Confirmed from the attachment lists in the briefs themselves:

- **Hell Grind + Cully Hill Boys** (generation 1) shipped with exactly three
  skills, all plain `.md`: `ACTING_SKILL.md`, `LIRA_SKILL.md`,
  `CINEDANCE_HIGGSFIELD_SKILL.md` (the 15-block version, with CHARACTER
  ACTING / STYLE / QUALITY as explicit sections).
- **Oneiric** (generation 2) shipped four skills, all packaged `.skill`
  bundles: `tig-scene-engine.skill`, `CINEDANCE HIGGSFIELD SKILL.skill`
  (v4, 11-block, no CHARACTER ACTING/STYLE/QUALITY), `tig-diagram.skill`,
  `tig-acting-task.skill`. Its own tools list ("a scene-drama engine, an
  acting system, and CINEDANCE" + "The Diagram Skill") maps `tig-scene-engine`
  → "scene-drama engine" and `tig-acting-task` → "acting system." **Neither
  `ACTING_SKILL.md` nor `LIRA_SKILL.md` is attached to or referenced by the
  Oneiric brief at all.**

So this is **version history, not a two-layer architecture**: on Oneiric,
`tig-acting-task` stands in for what `ACTING_SKILL.md` did on the two
earlier films, and CINEDANCE v4 (`.skill`) is the successor to the
15-block `.md` CINEDANCE. `tig-scene-engine` and `tig-diagram` are net-new
capabilities that didn't exist yet on Hell Grind/Cully. This replaces the
earlier "two complementary layers" hypothesis below (§3.1, kept for
record) — the open question is no longer *how do ACTING and TIG Acting
Task combine*, but **which generation of the toolset should PRE adopt as
canonical**: the earlier, production-proven set from two completed
features, or the more refined/disciplined latest set from the most recent
film — and what happens to LIRA (image prompts), which has no `TIG`
successor and presumably still applies to both generations.

### 3.1 (superseded by 3.0; RESOLVED by D-001/D-002) ACTING vs. TIG Acting Task
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

Originally read as two complementary layers (ACTING = permanent identity,
TIG Acting Task = per-scene tactic). **Per §3.0 above, that reading is
likely wrong** — they are two successive versions of the same role, from
two different productions, not two parts of one pipeline. Still open: does
TIG Acting Task's own master-profile equivalent (it has none — it assumes
identity/voice locking happened elsewhere) mean Oneiric still relied on
something like ACTING's master-profile format informally, just without a
dedicated skill for it? Needs a decision either way (see §3.0).

### 3.2 "Director's Read" has no explicit skill mapping
CLAUDE.md / `PRE_PROJECT_CONTEXT.md` name "Script Stress Test" and
"Director's Read" as two workflow steps. Script Stress Test clearly maps to
TIG Scene Engine's AUDIT mode (Goal/Obstacle/Tactic/Reversal/Value Shift).
"Director's Read" most likely maps to TIG Acting Task §0–§1c (naming the
scene's one shared event and each character's physical channel through it —
matches the Oneiric brief's own description of "the director's read" in
§01 almost verbatim). But no source document states this mapping directly.
Needs confirmation before writing a spec for these two workflow phases.

### 3.3 No single canonical CINEDANCE prompt skeleton — again a generation gap
**RESOLVED by D-001: CINEDANCE v4's 11-block skeleton is canonical.**
Per §3.0, this is the same version split, not three independent variants:
- Hell Grind / Cully Hill Boys used the **generation-1** `.md` CINEDANCE:
  15 sections, including CHARACTER ACTING, STYLE (a fixed per-project Style
  Prefix), and QUALITY.
- Oneiric used **generation-2** CINEDANCE v4 (`docs/skills/cinedance/SKILL.md`,
  the `.skill` bundle): 11 sections — SCENE CONTEXT · ACTIVE REFERENCES ·
  LOCATION MAP · FIRST FRAME AND SPATIAL BLOCKING · FORMAT MODE · OPTICS ·
  CAMERA · ACTION TIMING · PHYSICS · LIGHTING · AUDIO · POSITIVE
  CONSTRAINTS. No CHARACTER ACTING, no STYLE, no QUALITY as named sections.
  Its worked example (Oneiric §04, Scene 2) instead folds performance
  direction into SEGMENTS/DIALOGUE/CHARACTER ACTING-less prose, and drops a
  dedicated STYLE block in favor of inline style language.

Same open question as §3.0: adopt v4 as canonical (it is the newer,
more disciplined, most-recently-battle-tested version), and treat the
generation-1 STYLE-Prefix-as-fixed-block practice as a PRE-level
convention layered on top rather than part of the skill itself? This is
one decision, not two — resolving §3.0 (which generation is canonical)
resolves this too.

### 3.4 No single canonical asset-tag naming convention
Three conventions appear in practice — and unlike §3.0/§3.3, this one does
**not** cleanly split by generation, since Cully Hill Boys (generation 1)
already used the more disciplined scheme on its own:
- Hell Grind: `@roco`, `@loc_cave_front` — no project code, no version.
- Cully Hill Boys **and** Oneiric: `@char_CB_Kel_v9`,
  `@loc_ON_dorm_commonroom_front_s2` — `type_PROJECT_name_scene_version`.
- TIG Diagram (`tig-blocking-map`, generation-2 only): its own
  `@staging_[PROJECT]_[scene]_[version]`, with `[PROJECT]` in ALL CAPS.

Reading: the versioned `type_PROJECT_name_scene_version` scheme is a
production-learned improvement that appeared starting with Cully Hill Boys
and simply carried forward into Oneiric — it looks like the convention to
standardize on regardless of which skill generation PRE adopts. TIG
Diagram's separate `@staging_` prefix is additive (a new tag type for a
new artifact kind), not a competing scheme.

Per the Module 01 automation principle ("automate IDs, tags, versions"),
PRE should generate this scheme system-side rather than let it be invented
per project. Still a concrete decision to lock down — it affects the
`Asset`/`AssetVersion` schema.

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

**Resolved:** §3.0, §3.1, §3.3 → `DECISIONS.md` D-001, D-002. §3.7's
human-in-the-loop requirement is now specified as a HARD GATE in
`DECISION_GATES.md`; what remains of §3.7 is the `Diagram` state machine in
the schema. §3.5's approval requirement is likewise gated, but the script
revision/proposal object it needs is still unspeced.

**Still blocking for the Module 01 schema: §1.1, §1.2, §1.3, §1.4, §1.5.**
These are the next thing to settle — none of them can be deferred past the
first migration.

Still open for the Orchestrator / skill-invocation layer: **§2.1** (how
skills are loaded and dispatched at runtime), **§3.2** (confirm the
Director's Read → `tig-acting-task` §0–1c mapping), **§3.4** (lock the
asset tag scheme), **§3.7** (`Diagram` state machine).

New data-model concepts surfaced, still unspeced: **§3.5** (script
revision/proposal object), **§3.6** (story goal / logline field on
`Project`).

Not yet chosen at all: the technology stack — language, framework, how the
chat surface is delivered, and how Claude skills are invoked from the
backend.
