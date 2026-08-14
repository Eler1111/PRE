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
