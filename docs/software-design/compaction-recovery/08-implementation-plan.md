# Plan de implementación — Compaction Recovery

Status: Approved
Last updated: 2026-09-21
Plan revision: 4

## Confirmed

Gate 1 and Gate 2 were explicitly approved on 2026-09-19. This plan implements the approved
[requirements](02-requirements.md), [architecture](04-architecture.md),
[data model](05-data-model.md), [interfaces](06-api-contracts.md), and
[decisions](07-decisions.md). The confirmed Change Profile remains cross-cutting/full as recorded
in [00-status.md](00-status.md).

Planning is not implementation authorization. No product source, plugin version, installation,
commit, publication, model-backed evaluation, or external system is changed by approving this
document.

The user explicitly approved implementation plan revision 1 on 2026-09-19. The user later
authorized revision 2 to resolve the SLICE-002/SLICE-003 validation-boundary dependency. On
2026-09-21, the user authorized revision 3 to use `gpt-5.6-luna` with high reasoning effort for
SLICE-004's model-backed verification and comparison. This approval completes software
definition; it does not authorize any implementation slice beyond the currently authorized
delivery slice.

On 2026-09-21, the user clarified that a baseline comparison is blocking only when the stable
source contains the same validated contract and produces a comparable result. A stable source
that predates the plugin, hook, or scenario inputs produces recorded `inconclusive` evidence and
does not block closure when the candidate checks pass.

The verified repository stack is Python 3.12+, PyYAML, jsonschema, pytest, Ruff, `uv`, and the
Codex CLI adapter with capability checks. Plugin hooks and App Server lifecycle behavior are current
official Codex interfaces. The existing skills snapshot remains skill-only; lifecycle evaluation
will freeze the selected source's manifest and hook inputs separately through the repository's
validation-input loader so historical snapshot identities do not change and stable/candidate
plugin sources cannot be mixed.

## Assumptions and deferred work

No implementation-blocking assumption remains.

Deliberately deferred non-goals remain: reducing compactation frequency, general memory,
transcript parsing, Context Mode integration, a database, a daemon, concurrent-agent state,
public publication, deployment, and CI. A GUI or custom Devquitect toggle is unnecessary because
Codex `/hooks` already owns individual hook activation.

Model-backed evaluation is authorized for the final lifecycle slice using the fixed
`gpt-5.6-luna`/high inventory below. The one/two/four-compaction behavior and comparison must
pass that inventory before the slice can be marked verified.

## Outcome and common constraints

An authorized long-running `project-plan-execution` delivery can survive repeated Codex context
compactations without repeating confirmed work, discarding partial work, or trusting stale
conversation over the checkpoint and repository. `09-delivery-status.md` remains the sole
durable delivery state and the working tree remains implementation reality.

All slices preserve unrelated working-tree changes and the single-writer revision protocol.
No slice installs dependencies into the user's environment, changes the plugin version, commits,
tags, pushes, publishes, deploys, or bypasses hook trust outside a fresh disposable evaluator.
Optional local tooling and its generated state are not part of this delivery.

The normative acceptance criteria are only in the `devquitect-verification` block below. Slice
prose explains implementation and evidence without maintaining a second criteria list.

## SLICE-001 — Versioned execution frontier and legacy-safe state guard

**Outcome:** new deliveries use checkpoint schema v3 with a validated execution frontier;
existing v1/v2 checkpoints remain readable, and active legacy mutation is rejected until the
documented recovery/migration sequence reconciles repository evidence. Dependencies: none.

**Existing files to modify:**

- `skills/project-plan-execution/references/delivery-state.md`: v3 fields, semantics, coherent
  refresh protocol, legacy read/migrate table, and unknown-data handling.
- `skills/project-plan-execution/references/execution.md`: milestone checkpoint cadence and
  frontier refresh before implementation/verification transitions.
- `skills/project-plan-execution/scripts/verify_slice.py`: strict v3 frontier validation,
  legacy mutation refusal, expected-revision preservation, and safe close behavior.
- `tests/unit/test_slice_verification.py`: v1/v2/v3, migration-required, preservation, invalid
  type/path/version, conflict, and atomic no-write cases.

**Implementation details:** the verifier accepts schema v3 only for active mutation. An active
v1/v2 `snapshot`, `check`, or `close` returns an unsupported result with a specific
`tracker.migration-required` issue and writes nothing. Status-only reading belongs to the skill
and remains read-only. Completed legacy checkpoints are not rewritten merely because they are
old. Unknown versions remain unsupported.

Version 3 requires the four approved `execution_frontier` members. Reject duplicate YAML keys,
wrong types, absolute/escaping/duplicate paths, and non-empty partial mappings without an action.
Preserve unknown fields during all supported writes. `close` may clear the completed slice's
`in_progress` and `pending_verification` state but must not fabricate free-text completion facts
or duplicate canonical slice status. Migration is a recovery workflow action, not a new CLI
operation and never derives facts from conversation.

**Verification and evidence:** run the slice-specific state tests and all common checks from the
inventory. Inspect rejected-operation bytes to prove no write, and a successful v3 close to
prove unrelated fields/body survive. If Graphify is available, run `graphify update .`, then repeat
the final checks over the updated tree. Delivery evidence belongs in `slices/SLICE-001.md` only
after this plan is approved and the slice is authorized.

**Rollback:** retain v3 reader support after any active migration. Reverting only new writes is
safe; reverting to a version unable to read v3 is not supported.

## SLICE-002 — Conservative recovery contract and deterministic hook handler

**Outcome:** every operational-context loss uses one documented recovery sequence, and the
standalone hook handler deterministically emits the correct bounded instruction for zero, one,
multiple, or malformed checkpoint candidates. Dependency: SLICE-001 verified and current.

**Files to create:**

- `skills/project-plan-execution/references/compaction-recovery.md`: shared resume/reconcile
  sequence, outcomes, ambiguity rules, activation limits, and operator messages.
- `hooks/hooks.json`: the single synchronous `SessionStart`/`^compact$` handler contract.
- `hooks/compaction_recovery.py`: standard-library event parser, bounded checkpoint discovery,
  and hook-specific JSON output.
- `tests/unit/test_compaction_recovery_hook.py`: subprocess-level input/output, discovery,
  path-safety, size, malformed-data, and failure tests.
- `evals/fixtures/compaction-recovery/`: approved-plan delivery fixture with completed, partial,
  pending, stale-conversation, and disagreement evidence but no prefabricated successful result.
- `evals/cases/compaction-recovery-resume-positive.yaml`: manual resume/reconciliation contract.
- `evals/cases/compaction-recovery-resume-negative.yaml`: stale-memory/repetition negative case.

**Existing files to modify:**

- `skills/project-plan-execution/SKILL.md`: concise routing to the recovery reference for
  compactation, startup/resume, handoff, clear/reset, and equivalent context loss.
- `authority-map.yaml`: add `project-plan-execution.compaction-recovery` with the hook script as
  owner, recovery reference as `explains`, entrypoint as `routes`, and external cases/tests as
  `tests`; preserve existing delivery-state/execution ownership.
- `src/devquitect_quality/validate.py`: admit repository-relative paths declared by the selected
  authority map into the frozen validation inputs while retaining source, regular-file, and path
  safety checks; this is the validation-boundary prerequisite for the slice.
- `tests/unit/test_validate.py`: cover external authority-map paths from the working tree and
  preserve the existing missing/unsafe authority-path records.
- `tests/unit/test_cases.py`: prove the new external cases load, retain fixed critical policy,
  and do not weaken existing cases.

**Implementation details:** the hook reads exactly one JSON object from stdin and uses only
`hook_event_name`, `source`, and `cwd`. It searches only immediate
`docs/software-design/*/09-delivery-status.md` paths below the detected repository root, parses
only the required top-level scalar frontmatter subset, and never reads transcripts, follows
escaping paths, accesses the network, executes checkpoint data, or writes files.

Wrong/non-compact events produce no recovery context. Zero candidates exit 0 silently. One
candidate emits the approved checkpoint path and recovery instruction. Multiple or malformed
plausible candidates emit a stop-and-resolve instruction without selecting one. Unexpected
runtime/input errors return non-zero with bounded stderr and no success context. JSON stdout is
at most 4096 UTF-8 bytes; candidate truncation reports the omitted count. The handler remains
independently executable and tested here but is not claimed to ship until SLICE-003.

The skill recovery sequence selects exactly one checkpoint, validates its approved plan,
reconciles named repository and verification evidence, reads only frontier-required context,
and then reports `resumed`, `reconciled`, `blocked`, or `ambiguous`. Conversation cannot prove
authorization, acceptance, deferral, completion, or verification.

**Verification and evidence:** run hook subprocess tests, case loading, structural validation,
the validator-boundary tests, and common checks. Do not execute the YAML behavioral cases with a
model without separate authorization. If Graphify is available, run `graphify update .` after code changes and before final
evidence capture.

**Rollback:** removing the runtime handler before it is packaged does not alter checkpoint
state. Preserve the manual recovery reference and v3 reader if any active delivery has migrated.

## SLICE-003 — Plugin integration, native activation, validation, and packaging

**Outcome:** Devquitect ships the exact trusted hook definition and handler, validates only the
approved executable inputs, builds them reproducibly, and documents native `/hooks`
enable/disable behavior. Dependency: SLICE-002 verified and current.

**Existing files to modify:**

- `.codex-plugin/plugin.json`: declare exactly `"hooks": "./hooks/hooks.json"` without a
  version bump in this local implementation task.
- `src/devquitect_quality/validate.py`: validate the exact manifest/config/command contract after
  the repository-relative authority paths and approved hook inputs are admitted by SLICE-002;
  reject undeclared/symlink hook inputs.
- `src/devquitect_quality/packaging.py`: admit the two exact hook files in `_safe_path` and
  `_tree_entries`, preserving regular-file checks, order, modes, timestamps, and digest behavior.
- `tests/unit/test_validate.py`: positive linkage plus missing, extra, escaping, symlink,
  asynchronous, wrong event/matcher/command/platform/bounds cases.
- `tests/unit/test_packaging.py`: exact ZIP contents, hook digest sensitivity, reproducibility,
  modes, undeclared inputs, and symlink/non-blob refusal in temporary repositories.
- `tests/integration/test_release_check.py`: prove exact source-commit binding still rejects stale
  evidence even when skill snapshot identity is unchanged by a hook-only commit.
- `tests/fixtures/valid-plugin/.codex-plugin/plugin.json`: declare the fixture hook.
- `docs/contributing-skills.md`: package allowlist, trust review, `/hooks` activation, Python
  prerequisite, and disabled/unavailable behavior.

**Files to create in the structural fixture:**

- `tests/fixtures/valid-plugin/hooks/hooks.json`
- `tests/fixtures/valid-plugin/hooks/compaction_recovery.py`

**Implementation details:** `load_validation_inputs` already admits the repository-relative
authority paths declared by the selected source. This slice additionally admits only the
manifest and two root hook paths. The validator requires the exact manifest pointer, one
synchronous `SessionStart` group, matcher `^compact$`, one command handler, POSIX and Windows
commands resolving only through `PLUGIN_ROOT`, timeout 10, context limit 1200, and no extra
handler. It rejects symlinks before reading content.

Packaging reads the same three plugin-level paths from the selected immutable commit. Hook-only
changes must alter the package digest. Release evidence remains safely bound by both
`snapshot_id` and exact `source_commit`; the integration test protects that invariant rather
than redefining historical skill snapshot identities.

Normal activation/deactivation uses Codex `/hooks`; global hook/plugin disablement is not the
recommended individual control. Trust bypass is absent from product guidance. Disabled,
untrusted, missing-Python, timeout, and process failure states never claim automatic recovery.

**Verification and evidence:** run hook, validation, packaging, release-check, and common checks.
Package tests use temporary Git repositories; do not create a release artifact from this working
tree, bump a version, install the plugin, or run release-check against a candidate commit. If
Graphify is available, run `graphify update .` before final checks.

**Rollback:** remove the manifest hook declaration and packaged hook inputs together. Leave v3
and manual recovery compatibility intact. A plugin cache already installed elsewhere is outside
this local task and requires separate authorization to change.

## SLICE-004 — Real App Server compactation evaluation and baseline refresh

**Outcome:** versioned lifecycle cases can cause and observe real compactations through Codex
App Server, and the required one/two/four, stale-memory, partial-work, and repository-conflict
scenarios produce reviewable evidence. Dependency: SLICE-003 verified and current.

**Files to create:**

- `src/devquitect_quality/app_server_adapter.py`: bounded stdio JSON-RPC lifecycle runner and
  isolated temporary plugin installation.
- `tests/integration/test_app_server_adapter.py`: fake CLI/plugin/App Server protocol covering
  ordering, wrong thread, timeout, hook failure, malformed messages, cleanup, and redaction.
- `evals/cases/compaction-recovery-compact-once.yaml`
- `evals/cases/compaction-recovery-compact-twice.yaml`
- `evals/cases/compaction-recovery-compact-four-times.yaml`
- `evals/cases/compaction-recovery-stale-conversation.yaml`
- `evals/cases/compaction-recovery-partial-work.yaml`
- `evals/cases/compaction-recovery-repository-disagreement.yaml`

**Existing files to modify:**

- `schemas/eval-case.schema.json`: backward-compatible `turns` xor versioned `scenario`, with
  exact `prompt` and empty `compact` step shapes.
- `src/devquitect_quality/evaluation.py`: route only scenario cases to the App Server runner;
  preserve the existing runner path and injection used by ordinary cases/tests.
- `src/devquitect_quality/cli.py`: load/freeze the selected source's validated manifest/hook
  inputs once and pass the matching stable/candidate inputs to lifecycle attempts.
- `src/devquitect_quality/observations.py`: normalize bounded `contextCompaction` lifecycle
  evidence and capture the declared checkpoint before/after subset.
- `src/devquitect_quality/assertions.py`: add the narrow exact-count assertion required to prove
  observed compactations; retain unknown-assertion failure behavior.
- `tests/unit/test_cases.py`, `tests/unit/test_observations.py`, and
  `tests/unit/test_assertions.py`: schema compatibility, lifecycle normalization/count, bounds,
  and old-case regression coverage.
- `tests/integration/test_eval_command.py`: old `turns` routing and new `scenario` routing with
  fake runners, no authentication or model call.
- `docs/contributing-skills.md`: lifecycle adapter isolation, local marketplace staging,
  authorization, failure classification, and diagnostic guidance.
- `docs/software-design/system-context.md`: after implementation and verification, refresh
  System boundaries, Current capabilities, Technical landscape, Development and verification,
  Preserved behavior, Known limitations, and Authoritative references.

**Implementation details:** the CLI freezes `ValidationInputs` from the same selected source as
the existing skill snapshot before any attempt. The adapter creates a temporary plugin root from
that frozen manifest/hooks plus the frozen skills, generates a one-plugin local marketplace,
and uses `codex plugin marketplace add` and `codex plugin add` inside the attempt's isolated
`CODEX_HOME`. It never changes the user's plugin configuration or cache. It starts the Codex
App Server over stdio with the existing sandbox/model policy and
`--dangerously-bypass-hook-trust` only after structural validation inside this disposable
boundary.

Each prompt waits for its same-thread terminal turn event. Each compact step sends
`thread/compact/start`, requires the immediate `{}` response, and waits for same-thread
`contextCompaction` `item/started` then `item/completed` before continuing. Bound messages,
events, stderr, timeouts, and secrets using existing observation/redaction policy. Do not call
`thread/shellCommand`; repository inspection remains model tool activity under the configured
sandbox.

The six lifecycle cases use the shared fixture and exact compact counts. Deterministic assertions
cover observed count, prohibited repetition commands/effects, allowed paths, checkpoint
transition or non-transition, runtime success, and contradiction stop. No synthetic prompt or
summary may satisfy a compact step.

**Verification and evidence:** first run the fake App Server/unit tests and all common checks.
The candidate model-backed inventory check is authorized by plan revision 3 and uses the
repository's fixed `gpt-5.6-luna`/high configuration. Attempt a comparison against the exact
current `stable-n` source ref when that ref contains the same validated plugin, hook, and scenario
inputs. If the ref predates that contract, record the comparison as `inconclusive` and continue;
it is non-blocking when the candidate checks pass. A comparable baseline regression remains
blocking. Infrastructure/auth/hook failures never pass and are not retried until their cause
changes. Update System Context only after the implemented baseline passes deterministic
verification, then rerun final checks and, when available, `graphify update .`.

**Rollback:** ordinary `turns` cases and `codex exec` remain unchanged. The scenario schema and
adapter may be removed together only if lifecycle cases are also removed; removing the evaluator
does not remove the shipped hook or alter delivery checkpoints. Preserve evidence already
recorded as historical, not current proof.

## Delivery order, cumulative review, and authorization

Implement in order. Each slice requires explicit authorization and a current verified dependency.
Shared-file changes in a later slice can invalidate prior evidence; rerun affected checks and
re-close the slice under the approved tracker protocol. Create `09-delivery-status.md` and each
`slices/SLICE-*.md` only when implementation is authorized through `$project-plan-execution`.

Before final acceptance, review the accumulated diff, confirm every criterion below has current
evidence, run the mandatory repository commands, and confirm no unresolved blocker, approval,
or acceptance remains. Model-backed commands are not implied by plan or slice approval; request
their authorization explicitly. No implementation authorization implies release, installation,
commit, push, publication, or deployment.

## Executable verification inventory

Every declared command must exit 0. `devquitect check` must report `result: pass`; Ruff must
report no violations; `git diff --check` must be silent. The candidate model-backed check in
SLICE-004 is mandatory for closure and authorized under plan revision 3. A comparable baseline
comparison is additional evidence; an `inconclusive` result caused by a stable source that lacks
the introduced contract does not block closure.

```devquitect-verification
schema_version: 1
slices:
  SLICE-001:
    depends_on: []
    criteria:
      AC-CR-001:
        text: "09-delivery-status.md remains the only durable execution-state file; no migration, verifier, or close operation creates parallel state."
        requirement: REQ-CR-001
      AC-CR-002:
        text: "Schema v3 records the reconstructable frontier with validated completed context, partial action and paths, do-not-repeat guidance, and pending verification while retaining canonical current-slice, next-action, and blockers fields."
        requirement: REQ-CR-002
      AC-CR-003:
        text: "Frontier fields do not duplicate or override slice status, evidence, acceptance, authorization, or completion authorities."
        requirement: REQ-CR-003
      AC-CR-004:
        text: "The execution contract refreshes one coherent revision only at approved meaningful progress boundaries and does not require writes after routine reads or commands."
        requirement: REQ-CR-004
      AC-CR-005:
        text: "Completed v1/v2 checkpoints remain unchanged and readable; active legacy mutation requires repository reconciliation and one v3 migration without fabricated facts."
        requirement: REQ-CR-020
      AC-CR-006:
        text: "All v3 and migration writes enforce expected revision, preserve unrelated fields/body and working-tree changes, and leave bytes unchanged on rejection or conflict."
        requirement: REQ-CR-024
    checks:
      CHECK-FAST:
        command: "uv run devquitect check --source working-tree --report .devquitect-reports/check.json"
        cwd: "."
      CHECK-RUFF:
        command: "uv run ruff check src tests"
        cwd: "."
      CHECK-DIFF:
        command: "git diff --check"
        cwd: "."
      CHECK-STATE:
        command: "uv run pytest tests/unit/test_slice_verification.py"
        cwd: "."
    inputs:
      - "skills/project-plan-execution"
      - "tests/unit/test_slice_verification.py"
      - "pyproject.toml"
      - "uv.lock"
      - "AGENTS.md"
      - "docs/software-design/compaction-recovery/02-requirements.md"
      - "docs/software-design/compaction-recovery/04-architecture.md"
      - "docs/software-design/compaction-recovery/05-data-model.md"
      - "docs/software-design/compaction-recovery/06-api-contracts.md"
  SLICE-002:
    depends_on: ["SLICE-001"]
    criteria:
      AC-CR-007:
        text: "Compactation, startup/resume, handoff, clear/reset, and equivalent context-loss signals route to one conservative recovery contract before implementation."
        requirement: REQ-CR-005
      AC-CR-008:
        text: "Recovery selects one checkpoint, validates its plan, reads its frontier, inspects named repository and verification evidence, loads only required context, and resumes or reports a discrepancy."
        requirement: REQ-CR-006
      AC-CR-009:
        text: "Conversation and compacted memory cannot establish verification, deferral, acceptance, authorization, or completion."
        requirement: REQ-CR-007
      AC-CR-010:
        text: "Confirmed completed work is not repeated without contradictory repository evidence, and partial paths are inspected and continued rather than overwritten or restarted."
        requirement: REQ-CR-008
      AC-CR-011:
        text: "Checkpoint/repository contradictions are classified and exposed before normal implementation continues; neither source is trusted blindly."
        requirement: REQ-CR-009
      AC-CR-012:
        text: "Several plausible or malformed active checkpoints produce bounded ambiguity and no silent selection."
        requirement: REQ-CR-010
      AC-CR-013:
        text: "Checkpoint discovery uses only validated hook input, plugin environment, and repository-local immediate session paths without transcripts, network, or escaping traversal."
        requirement: REQ-CR-022
      AC-CR-014:
        text: "The hook handler uses only Python standard library, reports unavailable runtime support, and never installs a dependency."
        requirement: REQ-CR-023
    checks:
      CHECK-FAST:
        command: "uv run devquitect check --source working-tree --report .devquitect-reports/check.json"
        cwd: "."
      CHECK-RUFF:
        command: "uv run ruff check src tests"
        cwd: "."
      CHECK-DIFF:
        command: "git diff --check"
        cwd: "."
      CHECK-HOOK:
        command: "uv run pytest tests/unit/test_compaction_recovery_hook.py"
        cwd: "."
      CHECK-CASES:
        command: "uv run pytest tests/unit/test_cases.py"
        cwd: "."
      CHECK-VALIDATE:
        command: "uv run devquitect validate --source working-tree --format json"
        cwd: "."
    inputs:
      - "skills/project-plan-execution"
      - "hooks"
      - "authority-map.yaml"
      - "evals/cases"
      - "evals/fixtures/compaction-recovery"
      - "schemas"
      - "src/devquitect_quality/validate.py"
      - "tests/unit/test_compaction_recovery_hook.py"
      - "tests/unit/test_cases.py"
      - "tests/unit/test_validate.py"
      - "pyproject.toml"
      - "uv.lock"
      - "AGENTS.md"
      - "docs/software-design/compaction-recovery/02-requirements.md"
      - "docs/software-design/compaction-recovery/04-architecture.md"
      - "docs/software-design/compaction-recovery/06-api-contracts.md"
      - "docs/software-design/compaction-recovery/07-decisions.md"
  SLICE-003:
    depends_on: ["SLICE-002"]
    criteria:
      AC-CR-015:
        text: "The plugin ships exactly one synchronous SessionStart handler matched to compact and its referenced standard-library script."
        requirement: REQ-CR-011
      AC-CR-016:
        text: "The handler runs synchronously before continuation and emits only bounded recovery context, never checkpoint/plan bodies, repository inventories, transcripts, or logs."
        requirement: REQ-CR-012
      AC-CR-017:
        text: "Zero active checkpoints is silent, one identifies its path, and several or malformed plausible candidates expose bounded ambiguity without selection."
        requirement: REQ-CR-013
      AC-CR-018:
        text: "The hook writes no marker, preference, task-state file, or competing execution log."
        requirement: REQ-CR-014
      AC-CR-019:
        text: "Missing, disabled, untrusted, timed-out, failed, or unsupported hooks never report successful automatic recovery; manual recovery remains available."
        requirement: REQ-CR-015
      AC-CR-020:
        text: "Contributor/operator guidance explains trust review after install or update and individual enable/disable through Codex /hooks."
        requirement: REQ-CR-016
      AC-CR-021:
        text: "Success, no-delivery, ambiguity, unavailable-hook, and repository-disagreement feedback is concise and action-oriented without custom UI."
        requirement: REQ-CR-017
      AC-CR-022:
        text: "Validation and packaging admit only the declared hook manifest and handler as regular in-root files and reject extra, escaping, symlink, or malformed executable inputs."
        requirement: REQ-CR-018
      AC-CR-023:
        text: "Identical immutable source produces byte-identical sorted package entries and digest; hook-only changes alter the digest while exact source-commit evidence binding remains enforced."
        requirement: REQ-CR-019
      AC-CR-024:
        text: "Hook JSON output is independently capped at 4096 UTF-8 bytes and configured with additionalContextLimit 1200 so normal operation cannot increase context pressure without a deterministic failure."
        requirement: REQ-CR-021
    checks:
      CHECK-FAST:
        command: "uv run devquitect check --source working-tree --report .devquitect-reports/check.json"
        cwd: "."
      CHECK-RUFF:
        command: "uv run ruff check src tests"
        cwd: "."
      CHECK-DIFF:
        command: "git diff --check"
        cwd: "."
      CHECK-HOOK:
        command: "uv run pytest tests/unit/test_compaction_recovery_hook.py"
        cwd: "."
      CHECK-PACKAGE:
        command: "uv run pytest tests/unit/test_validate.py tests/unit/test_packaging.py tests/integration/test_release_check.py"
        cwd: "."
    inputs:
      - ".codex-plugin"
      - "hooks"
      - "skills/project-plan-execution"
      - "src/devquitect_quality/packaging.py"
      - "src/devquitect_quality/validate.py"
      - "tests/fixtures/valid-plugin"
      - "tests/unit/test_compaction_recovery_hook.py"
      - "tests/unit/test_validate.py"
      - "tests/unit/test_packaging.py"
      - "tests/integration/test_release_check.py"
      - "docs/contributing-skills.md"
      - "schemas"
      - "authority-map.yaml"
      - "pyproject.toml"
      - "uv.lock"
      - "AGENTS.md"
      - "docs/software-design/compaction-recovery/04-architecture.md"
      - "docs/software-design/compaction-recovery/06-api-contracts.md"
  SLICE-004:
    depends_on: ["SLICE-003"]
    criteria:
      AC-CR-025:
        text: "A real single contextCompaction lifecycle event rehydrates the active checkpoint, inspects repository state, continues partial C, and does not repeat completed A/B or start D early."
        requirement: ACC-CR-001
      AC-CR-026:
        text: "The same continuation invariant is evidenced with exact observed compactation counts of one, two, and four in separate fresh attempts."
        requirement: ACC-CR-002
      AC-CR-027:
        text: "A stale conversational instruction loses to reconciled checkpoint and repository evidence."
        requirement: ACC-CR-003
      AC-CR-028:
        text: "Existing partial implementation paths are inspected and continued without overwrite or restart."
        requirement: ACC-CR-004
      AC-CR-029:
        text: "A deliberate checkpoint/repository contradiction is exposed and reconciled or blocks before normal implementation resumes."
        requirement: ACC-CR-005
      AC-CR-030:
        text: "A compactation with no active delivery produces no recovery context or delivery-state mutation."
        requirement: ACC-CR-006
      AC-CR-031:
        text: "Several active checkpoints stop silent selection and expose only the bounded choice required."
        requirement: ACC-CR-007
      AC-CR-032:
        text: "Disabled, untrusted, failed, or unsupported hook execution is classified as unavailable/inconclusive and never as recovered."
        requirement: ACC-CR-008
      AC-CR-033:
        text: "The evaluated plugin source contains exactly the validated hook inputs, stable/candidate attempts cannot mix plugin sources, and packaging remains reproducible."
        requirement: ACC-CR-009
    checks:
      CHECK-FAST:
        command: "uv run devquitect check --source working-tree --report .devquitect-reports/check.json"
        cwd: "."
      CHECK-RUFF:
        command: "uv run ruff check src tests"
        cwd: "."
      CHECK-DIFF:
        command: "git diff --check"
        cwd: "."
      CHECK-EVALUATOR:
        command: "uv run pytest tests/unit/test_cases.py tests/unit/test_observations.py tests/unit/test_assertions.py tests/integration/test_app_server_adapter.py tests/integration/test_eval_command.py"
        cwd: "."
      CHECK-BEHAVIOR:
        command: "uv run devquitect eval --source working-tree --suite compaction-recovery --model gpt-5.6-luna --reasoning-effort high --report .devquitect-reports/compaction-recovery-eval.json"
        cwd: "."
    inputs:
      - ".codex-plugin"
      - "hooks"
      - "skills"
      - "src"
      - "tests"
      - "evals"
      - "schemas"
      - "baselines/stable-n.json"
      - "authority-map.yaml"
      - "docs/contributing-skills.md"
      - "docs/software-design/system-context.md"
      - "pyproject.toml"
      - "uv.lock"
      - "AGENTS.md"
      - "docs/software-design/compaction-recovery/01-concept.md"
      - "docs/software-design/compaction-recovery/02-requirements.md"
      - "docs/software-design/compaction-recovery/04-architecture.md"
      - "docs/software-design/compaction-recovery/05-data-model.md"
      - "docs/software-design/compaction-recovery/06-api-contracts.md"
      - "docs/software-design/compaction-recovery/07-decisions.md"
```

## Handoff

This plan is Approved and software definition is complete. Implementation requires a separate
request naming `SLICE-001`, another concrete slice set, or the whole plan. Execution then hands
off to `$project-plan-execution`; model-backed checks still require their own explicit
authorization.
