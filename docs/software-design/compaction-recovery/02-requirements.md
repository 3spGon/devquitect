# Compaction Recovery requirements

Status: Approved
Last updated: 2026-09-19

## Confirmed

- Requirements below derive from the supplied initiative, current repository contracts, or current official Codex hook behavior.
- The delivery checkpoint remains the sole durable execution-state authority; repository evidence remains the authority for what actually exists.

## Assumptions

None.

## Open decisions

- The exact backward-compatible checkpoint schema transition is deferred to technical design under `DEC-CR-002`.

## Functional requirements

### Delivery state

- **REQ-CR-001** — `09-delivery-status.md` shall remain the only durable task-execution state file.
- **REQ-CR-002** — The delivery checkpoint shall explicitly preserve the reconstructable execution frontier: current slice, completed work relevant to resumption, current partial action and affected paths when known, next action, work that must not be repeated without contradictory repository evidence, pending verification, and blockers.
- **REQ-CR-003** — Existing checkpoint facts such as slice status and verified evidence shall not be duplicated into competing authorities inside the frontier.
- **REQ-CR-004** — Project Plan Execution shall refresh the frontier after meaningful progress boundaries, including completing a functional change, resolving a consequential decision, completing a migration, moving from implementation to verification, or resolving verification failures. Reads and individual routine commands shall not force checkpoint writes.

### Recovery behavior

- **REQ-CR-005** — Compactation, startup/resume, handoff, context reset, and equivalent loss-of-operational-context signals shall enter the same conservative recovery contract before implementation continues.
- **REQ-CR-006** — Recovery shall re-read the selected delivery checkpoint, validate its approved plan relationship, identify the current slice and frontier, inspect relevant repository and verification evidence, read only the required context for that frontier, and then either resume or report a discrepancy.
- **REQ-CR-007** — Recovery shall not infer `verified`, `deferred`, acceptance, authorization, or completion from conversational or compacted memory.
- **REQ-CR-008** — Confirmed completed work shall not be repeated unless current repository evidence contradicts the checkpoint. Partial work shall be inspected and continued rather than overwritten or restarted.
- **REQ-CR-009** — When checkpoint and repository disagree, recovery shall classify and expose the discrepancy before continuing; neither source shall be trusted blindly.
- **REQ-CR-010** — When several delivery checkpoints remain plausible, recovery shall not choose silently.

### Runtime trigger

- **REQ-CR-011** — The Devquitect plugin shall ship a synchronous Codex lifecycle hook matching `SessionStart` with `source: "compact"`.
- **REQ-CR-012** — The hook shall run before the next model request and inject only bounded recovery context. It shall not copy the implementation plan, checkpoint body, repository inventory, or tool logs into the conversation.
- **REQ-CR-013** — With no active Devquitect delivery checkpoint, the hook shall produce no recovery instruction. With one candidate it shall identify that checkpoint. With multiple candidates it shall identify the ambiguity without selecting one.
- **REQ-CR-014** — The hook shall not create a recovery marker, secondary durable task-state file, or competing execution log.
- **REQ-CR-015** — A missing, disabled, untrusted, timed-out, or failed hook shall never be presented as successful automatic recovery. The skill-level resume contract remains available, but automatic compactation protection is unavailable until the runtime hook executes.

### Operator interaction

- **REQ-CR-016** — Installation or update guidance shall tell the operator that Codex requires review/trust for new or changed unmanaged hooks.
- **REQ-CR-017** — Recovery feedback shall be concise and action-oriented for success, ambiguity, unsupported runtime, and checkpoint/repository disagreement states. No custom visual interface is required.

### Packaging and compatibility

- **REQ-CR-018** — Structural validation and deterministic packaging shall recognize only the declared Devquitect hook manifest and referenced hook files; unrelated root files shall remain excluded.
- **REQ-CR-019** — Package reproducibility, normalized ordering, stable timestamps, and artifact identity shall remain intact when hook inputs are included.
- **REQ-CR-020** — Existing delivery checkpoints shall remain readable. Missing new frontier data shall be treated as unknown and conservatively reconstructed, not fabricated.

## Quality requirements

- **REQ-CR-021** — Runtime recovery context shall remain small enough to avoid materially worsening context pressure; the implementation plan shall define and deterministically enforce a bounded output contract.
- **REQ-CR-022** — Hook discovery and checkpoint selection shall use only repository-local evidence available from the documented hook input and plugin environment.
- **REQ-CR-023** — Hook handling shall avoid new third-party runtime dependencies; the delivery workflow's existing Python runtime prerequisite may be reused only if technical design confirms it is available at hook execution time.
- **REQ-CR-024** — Recovery shall preserve unrelated working-tree changes and the single-writer revision protocol.

## Acceptance scenarios

- **ACC-CR-001 — Single compactation:** with A/B complete, C partial, and D pending, one compactation causes checkpoint rehydration, repository inspection, and continuation of C; A/B are not repeated and D is not started early.
- **ACC-CR-002 — Repeated compactation:** the same invariant holds across one, two, and four compactations in one delivery.
- **ACC-CR-003 — Stale conversation:** stale conversational content conflicts with the checkpoint; repository evidence plus checkpoint state control recovery.
- **ACC-CR-004 — Partial implementation:** modified files for the active slice are inspected and continued without overwrite or restart.
- **ACC-CR-005 — Repository disagreement:** a deliberate checkpoint/repository contradiction is detected and reconciled or surfaced before implementation resumes.
- **ACC-CR-006 — No active delivery:** a compactation outside active Devquitect delivery adds no recovery noise.
- **ACC-CR-007 — Ambiguous delivery:** multiple plausible active checkpoints stop silent selection and expose the minimum required choice.
- **ACC-CR-008 — Hook unavailable:** automatic protection is reported unavailable; no false claim of recovered state is emitted.
- **ACC-CR-009 — Package contract:** the built plugin contains the declared hook configuration and script, contains no undeclared hook inputs, and remains reproducible.

## Verification requirements

- Deterministic tests shall cover hook event parsing and output for compact versus non-compact sources, zero/one/multiple active checkpoints, malformed checkpoints, bounded output, and failure behavior.
- Deterministic validation and packaging tests shall cover allowed hook inputs, rejected undeclared inputs, manifest linkage, reproducibility, and artifact digest changes.
- Relevant positive and negative Devquitect cases shall protect the critical delivery-state and recovery contracts.
- Model-backed behavioral evaluation shall cover `ACC-CR-001` through `ACC-CR-005`, including one, two, and four compactations, only when explicitly authorized under repository policy.
- Credential-free repository verification remains mandatory after implementation changes.

## Non-goals

- Reducing compactation frequency, storing complete tool logs, adding general memory, integrating Context Mode, adding embeddings, creating a database, or coordinating concurrent agents.
