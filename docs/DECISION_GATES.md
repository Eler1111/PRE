# PRE — Decision Gates

Implements `DECISIONS.md` D-004. This is the map of where PRE runs on its
own and where it stops and asks the user.

Legend:
- **AUTO** — runs without asking. Result is written to `project.db` as
  `INFERENCE` unless it is a deterministic fact.
- **GATE** — PRE halts this branch of work, states what it needs in Polish
  chat, and waits. Produces a `Decision` record when answered.
- **HARD GATE** — cannot proceed under any confidence level, because the
  step requires something only the user can supply (an external
  generation, a creative choice, or an irreversible approval).

---

## Global phase

| Step | Mode | Notes |
|---|---|---|
| Screenplay import | AUTO | Original file preserved unchanged. GATE only if the format is unsupported or parsing fails. |
| Scene parsing, scene index, script order | AUTO | Deterministic. |
| Entity detection, appearances, dialogue | AUTO | Stored as FACT where textual, INFERENCE where derived. |
| Alias resolution | AUTO (high confidence) / GATE | Merging two labels into one canonical character is a GATE below the confidence threshold. Never auto-merge low-confidence aliases. |
| Location normalization | AUTO / GATE | Same rule: differently worded headings are not assumed to be the same place. |
| Prop significance | AUTO | Only production-relevant objects. Not every noun. |
| Chronology detection (flashback, dream, parallel) | AUTO / GATE | Ambiguous chronology becomes a ReviewFlag, not a silent guess. |
| State events, state timelines | AUTO | Always INFERENCE at this stage. |
| Continuity dependencies | AUTO | |
| Asset requirement plan | AUTO | Status `NOT_CREATED`. No assets generated. |
| **Continuity review** | **GATE (batched)** | All open ReviewFlags from global analysis presented as one grouped question set, not a stream. |
| **Approving inferred states as production truth** | **HARD GATE** | Per `CLAUDE.md`: AI inference is never automatically frozen as truth. |

---

## Scene production phase

| Step | Mode | Skill | Notes |
|---|---|---|---|
| **Scene selection** | **HARD GATE** | — | The user chooses the scene. |
| Load scene context from global model | AUTO | — | |
| Script Stress Test | AUTO | `tig-scene-engine` (AUDIT) | Runs and reports. Diagnosis is not a change. |
| **Accepting a "What if" fix** | **HARD GATE** | `tig-scene-engine` | If accepted and it alters screenplay text, it becomes a script revision proposal — never an in-place edit of the source. |
| Director's Read | AUTO → GATE | `tig-acting-task` §0–1c | PRE proposes the scene's one shared event and each character's physical channel. **Approving the named event is a GATE** — it is the core interpretive decision the whole scene hangs on. |
| Scene breakdown, required states | AUTO | — | |
| Existing approved asset lookup / reuse | AUTO | — | Reuse never asks. |
| Missing asset detection | AUTO | — | |
| Image prompt for a missing asset | AUTO | `lira` | |
| **Asset generation** | **HARD GATE** | — | Integrated mode: confirm before spending a paid generation. Assisted manual mode: PRE prepares model, references, prompt and parameters; the user generates externally and imports the result. |
| **Asset approval** | **HARD GATE** | — | Nothing enters production without explicit approval. |
| Asset stress test (10 generations) | AUTO to run | — | |
| **Stress test verdict (recognizable 10/10?)** | **HARD GATE** | — | Human judgment. A failed test means rewriting the descriptor or rebuilding the asset. |
| Voice block proposal | AUTO | `acting` §9 (per D-002) | |
| **Voice Lock** | **HARD GATE** | — | Permanent. Pasted verbatim into every prompt thereafter, never re-worded. |
| Acting master profile proposal | AUTO | `acting` §6 (per D-002) | |
| **Acting Profile lock** | **HARD GATE** | — | Permanent per character. |
| Per-scene acting task | AUTO | `tig-acting-task` | Rewritten per scene; follows the approved Director's Read. |
| Spatial map / blocking proposal | AUTO | — | |
| **Blocking approval** | **GATE** | — | Staging is named in `CLAUDE.md` as a user decision. |
| Deciding a diagram is needed | AUTO | `tig-blocking-map` | |
| Diagram generation prompt (step 1) | AUTO | `tig-blocking-map` | |
| **Diagram image generation** | **HARD GATE** | — | Runs outside Claude (Seedream / Nano Banana / GPT Image). PRE must not advance to the connector block until the generated image is returned. |
| Connector block (step 2) | AUTO | `tig-blocking-map` | |
| Coverage proposal | AUTO | — | |
| **Coverage approval** | **GATE** | — | `CLAUDE.md`: coverage choices are a user decision when artistically ambiguous. |
| Shot card creation | AUTO | — | IDs, numbering, versioning all automatic. |
| Video prompt assembly | AUTO | `cinedance` v4 | 11-block skeleton per D-001. |
| **Shot generation** | **HARD GATE** | — | Same two modes as asset generation. Every generation costs money. |
| Take import, logging, status | AUTO | — | Prompt version, what changed, verdict — all logged automatically. |
| **Take evaluation (approve / reject / iterate)** | **HARD GATE** | — | |
| Surgical iteration (one line changed) | AUTO to prepare | `cinedance` | Generation itself is still a gate. |
| **Simplify-the-shot decision after repeated failure** | **GATE** | — | After the failure threshold, PRE stops proposing rewordings and asks whether to split the shot, drop an action, or change the angle. |
| Assembly of approved takes | AUTO | — | |
| Coverage hole / failed shot detection | AUTO | — | |
| **Finished scene approval** | **HARD GATE** | — | |

---

## Rules that apply to every gate

1. **Ask in Polish, in the conversation.** A gate is a question in chat,
   not a modal, not a form.
2. **Ask with enough context to answer without scrolling back** — what is
   being decided, what PRE proposes, and what the alternatives cost.
3. **Never fabricate the answer to move on.** If a gate is open, the work
   downstream of it waits.
4. **Work not blocked by the gate continues.** An open gate on one asset
   does not stall analysis, logging, or preparation elsewhere in the
   scene.
5. **The gate survives a restart.** Pending gates are project state.
