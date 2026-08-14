# PRE — Decision Log

Durable project decisions. Each entry is a settled choice, not a proposal.
Supersede an entry by adding a new one that references it — never edit a
past decision in place.

---

## D-001 — Canonical skill generation: Oneiric (generation 2)

**Status:** decided
**Resolves:** `ARCHITECTURE_AUDIT.md` §3.0, §3.1, §3.3

PRE adopts the **generation-2 skill set**, as used on ONEIRIC:

| Role | Skill | Source |
|---|---|---|
| Scene dramatic structure / Script Stress Test | `tig-scene-engine` | `docs/skills/tig-scene-engine/` |
| Per-scene performance direction | `tig-acting-task` | `docs/skills/tig-acting-task/` |
| Multi-character staging diagrams | `tig-blocking-map` (TIG Diagram) | `docs/skills/tig-blocking-map/` |
| Video prompt construction | `cinedance` v4 (11-block) | `docs/skills/cinedance/` |

Rationale: it is the most recent and most disciplined version of the
toolchain, refined across three productions. Where generation 1 and
generation 2 disagree, generation 2 wins.

**Consequences:**
- The canonical video-prompt skeleton is CINEDANCE v4's 11 sections, not
  the generation-1 15-section layout.
- `docs/skills/acting/SKILL.md` and the 15-block CINEDANCE format are
  retained in the repo as historical reference, not as the active spec —
  with the one exception in D-002.

---

## D-002 — Two generation-1 capabilities are retained, because generation 2 has no successor

**Status:** decided
**Depends on:** D-001

Adopting generation 2 wholesale would leave two holes, because ONEIRIC's
attachment list simply has no equivalent skill. Both are explicitly
required by `CLAUDE.md`'s core workflow, so both are retained:

**1. LIRA — image prompts.** Generation 2 ships no image-prompt skill, yet
ONEIRIC still produced character sheets and location plates (Soul Cinema,
Soul 2.0, Seedream, Nano Banana). `docs/skills/lira/SKILL.md` remains the
active skill for all image generation and image editing. It is unaffected
by D-001.

**2. ACTING master profile + voice prompt formula — permanent identity
only.** `tig-acting-task` is explicitly a per-scene skill; it assumes
identity and voice locking already happened elsewhere and provides no
format for them. `CLAUDE.md` requires both **Voice Lock** and **Acting
Profile** as workflow steps. Therefore `docs/skills/acting/SKILL.md` §6
(master profile format) and §9 (voice prompt formula) remain active **for
the permanent per-character identity layer only**.

The resulting split, which is now the project's rule:

- **Permanent, locked once per character:** ACTING §6 master profile +
  ACTING §9 voice prompt. Written during asset preparation, pasted
  verbatim thereafter, never adapted per scene.
- **Per scene, rewritten every time:** `tig-acting-task`'s
  `ACTING TASK — [NAME]` block (scene direction, motive, goal, obstacle,
  tactic, moment-to-moment eye work).

ACTING §8 ("scene adaptation") is **not** used — `tig-acting-task`
replaces it.

---

## D-003 — Chat is the entire interface

**Status:** decided
**Restates and hardens:** `CLAUDE.md` principle 1, `PRE_PROJECT_CONTEXT.md` §2

The application is a single Polish-language conversation. The user works
by talking to the system; there is no primary navigation model, no
dashboard, no wizard, no step-by-step form to fill in.

Generated and structured artifacts — scene lists, asset sheets, state
timelines, diagrams, shot cards, prompts, takes — are surfaced **beside**
the conversation as supporting views, rendered when relevant. They are
outputs to look at, never the place where work is driven from.

The user never selects an agent, a skill, or a workflow phase by name.
The Orchestrator infers intent from the conversation and invokes what is
needed.

---

## D-004 — Automate everything procedural; stop at decision gates and ask

**Status:** decided
**Implements:** `CLAUDE.md` principle 9, `PRE_PROJECT_CONTEXT.md` §18
**Detailed in:** `docs/DECISION_GATES.md`

PRE runs the Higgsfield workflow automatically from end to end, except at
defined **decision gates**, where it stops, states what it needs, and
waits for the user's answer in chat before continuing.

Rules:

1. **A gate is a stop, not a suggestion.** At a gate the system does not
   pick a default and proceed. It halts that branch of work and asks.
2. **Gates are creative or irreversible, never procedural.** Anything the
   system can derive, name, number, version, reuse, or check is done
   silently. Interpretation, staging, performance, coverage, approvals,
   and anything that spends a paid generation or overwrites approved
   truth is a gate.
3. **Gate state is persistent.** A pending gate lives in `project.db`, not
   in the conversation. Closing the app and returning must resume at the
   same open question.
4. **Every answered gate produces a `Decision` record** — what was asked,
   what was chosen, when, and what it affected. This is what makes
   approved production truth traceable and distinguishable from
   inference.
5. **Confidence routes the gate** (`PRE_PROJECT_CONTEXT.md` §14): high
   confidence proceeds automatically, medium proposes and asks for
   confirmation, low asks openly. Confidence never converts an inference
   into a fact.
6. **Batch where it respects the user's attention.** Many small
   same-kind questions (e.g. continuity ambiguities from global analysis)
   are presented as one grouped gate, not as a stream of interruptions.

---

## D-005 — One `Entity` table with a type discriminator

**Status:** decided
**Resolves:** `ARCHITECTURE_AUDIT.md` §1.1

Characters, locations, props, vehicles and animals live in **one `Entity`
table** with an `entity_type` column — not in five separate tables.

Rationale, drawn from the source productions themselves: the categories
blur in real use. Cully Hill Boys treated a car interior as a **prop, not a
location**. Hell Grind treated a crowd as a **single asset**. Rigid
per-type tables would force those cases into the wrong shape and make new
types expensive to add.

Where a type genuinely needs fields the others do not (a character's voice
profile, acting profile), those live in small per-type extension tables
keyed to `Entity` — never as a duplicated parallel hierarchy. State,
versioning, appearances and asset requirements work identically for every
entity type, per `01_global_script_analyzer.md` §8.

---

## D-006 — `EntityAlias` is a first-class table

**Status:** decided
**Resolves:** `ARCHITECTURE_AUDIT.md` §1.2

The same character appears in a screenplay under several labels ("ROCO",
"THE DRIVER", "MAN IN JACKET"). Aliases get their own table, carrying the
**original screenplay wording** plus the link to the canonical entity, its
`information_status` and its confidence.

Merging is never destructive: original mentions are always preserved, and
a low-confidence merge is a decision gate, not an automatic action.

This corrects an omission — `01_global_script_analyzer.md` §39 requires
persisting aliases, but `PRE_PROJECT_CONTEXT.md` §12 forgot to list the
table.

---

## D-007 — `ContinuityDependency` carries provenance

**Status:** decided
**Resolves:** `ARCHITECTURE_AUDIT.md` §1.3

Continuity dependencies get `information_status` and `confidence`, like
every other non-trivial claim in the system.

Without them the system cannot tell which links it may silently recompute
when an upstream decision changes, and which ones were the user's
deliberate choice and must not be touched. `PRE_PROJECT_CONTEXT.md` §13
already calls this distinction "especially important for continuity and
state propagation" — the structure now allows it.

---

## D-008 — State validity is an explicit set of scenes, never a numeric range

**Status:** decided
**Resolves:** `ARCHITECTURE_AUDIT.md` §1.4

A `State` does not store `valid_from`/`valid_to` as scene numbers. It
stores the **explicit set of scenes in which the state holds**.

Rationale: script order is not story order. If a state were recorded as
"scenes 12–27" and scene 21 is a flashback to ten years earlier, the naive
range silently asserts the wrong costume, wounds and props for that scene.
`01_global_script_analyzer.md` §7 and `PRE_PROJECT_CONTEXT.md` §15 both
forbid relying on script order — but the worked example in §20 shows
contiguous ranges. This resolves the contradiction in favor of the rule.

A contiguous range ("sceny 12–20") remains valid as a **display
convenience** in chat and in views. It is never the stored truth.

State events (what starts and ends a state) remain stored separately, as
the evidence the scene set is derived from.

---

## D-009 — Two independent status axes, never merged

**Status:** decided
**Resolves:** `ARCHITECTURE_AUDIT.md` §1.5

Two different questions were sharing the words APPROVED and REJECTED. They
are now separate columns with distinct names and distinct vocabularies:

- **`information_status`** — where the claim comes from and how far it is
  trusted: `FACT` · `INFERENCE` · `APPROVED` · `REJECTED` · `OVERRIDDEN` ·
  `UNKNOWN`.
- **`production_status`** — how far through production an artifact is:
  `NOT_CREATED` · `IN_PROGRESS` · `CREATED` · `TESTING` · `APPROVED` ·
  `REJECTED` · `SUPERSEDED`.

"The system inferred this character is wet in scene 10" and "the wet
character asset passed its stress test and is cleared for shooting" are
unrelated statements. No object mixes the two axes into one field, and
`State`'s redundant `approval_status` is dropped — approval lives on
`information_status`.

---

## D-010 — Local-first application; project location is the user's choice

**Status:** decided
**Resolves:** `ARCHITECTURE_AUDIT.md` §4 (stack)

**Stack:** Python backend, SQLite (`project.db`), chat interface served as
a local web page in the browser. The browser is chosen because the chat's
side surfaces must render images, diagrams and video.

**Execution:** the application runs on the user's own machine for
prototype v0.

**Project location is configurable.** A project folder may live on an
internal disk, an external drive, or inside a synced cloud folder such as
iCloud Drive, Dropbox or Google Drive. Nothing in the code assumes a fixed
path; all file access goes through one project-storage boundary.

**Known hazard, handled deliberately:** a live SQLite database inside a
file-sync folder is a well-documented corruption risk — the sync client can
copy the database and its journal out of order, or two machines can open
the same project at once. PRE therefore:

1. takes a **lock file** in the project folder, so the same project cannot
   be opened on two machines simultaneously;
2. **checkpoints and closes the database cleanly** when the project is
   closed, so the synced files are always in a consistent state;
3. warns in chat, in Polish, when a project is opened from a folder that
   looks like a sync target.

Media files in a synced folder are unproblematic and genuinely useful.

**True cloud hosting** — the application itself running on a server,
reachable from anywhere — is deliberately *not* built for v0, but must
stay reachable as a later configuration change rather than a rewrite. The
same boundaries that make providers replaceable (`CLAUDE.md` principle 10)
apply here: storage access, database access and any assumption of a single
local user stay behind interfaces. Building both targets now would double
the work with no benefit while there is one user on one machine.
