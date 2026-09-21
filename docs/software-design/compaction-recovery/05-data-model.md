# Compaction Recovery data model

Status: Approved
Last updated: 2026-09-19

## Decision

Active delivery checkpoints move to `schema_version: 3`. Versions 1 and 2 remain readable.
Version 3 is explicit because version 2 already has deployed meaning (`ownership`); an optional
unversioned frontier would make capability and migration state ambiguous.

## Canonical checkpoint shape

The existing top-level fields remain authoritative. Version 3 adds only
`execution_frontier`; it does not duplicate `current_slice`, `next_action`, `blockers`, slice
status, acceptance, or evidence.

```yaml
schema_version: 3
skill: project-plan-execution
revision: 12
phase: delivery
phase_status: active
current_slice: SLICE-003
next_action: Continue request validation in src/example.py
blockers: []
execution_frontier:
  last_completed:
    - Added failing validation case and confirmed the expected failure
  in_progress:
    action: Implement request validation
    paths:
      - src/example.py
      - tests/test_example.py
  do_not_repeat:
    - Do not recreate the failing validation case unless repository evidence contradicts it
  pending_verification:
    - uv run pytest tests/test_example.py
```

## Field contract

| Field | Type | Rules |
| --- | --- | --- |
| `last_completed` | list of strings | Non-empty concise facts relevant to resumption; may be empty |
| `in_progress` | null or mapping | Null when no partial action is known |
| `in_progress.action` | string | Required and non-empty when the mapping exists |
| `in_progress.paths` | list of strings | Normalized repository-relative paths; no escapes, absolute paths, or duplicates |
| `do_not_repeat` | list of strings | Non-empty concise items; advisory until checked against repository evidence; may be empty |
| `pending_verification` | list of strings | Exact pending command or manual verification descriptions; may be empty |

All four frontier members are required in v3, including empty lists/null. Unknown fields are
preserved by coherent writes but do not acquire semantics. Duplicate YAML keys, invalid types,
unsupported versions, or escaped paths are format errors.

The frontier is reconstructive context, not proof. `last_completed` and `do_not_repeat` cannot
create a verified slice, acceptance, authorization, or completion state. Existing slice
records and evidence remain the owners of those facts.

## Freshness transitions

A coherent checkpoint revision refreshes the frontier after:

- a functional change is completed;
- a consequential decision is resolved;
- a migration completes;
- work moves from implementation to verification;
- a verification failure is understood or resolved;
- recovery reconciles a material checkpoint/repository discrepancy.

Routine reads and individual commands do not require writes. A refresh updates the frontier,
existing canonical fields, `revision`, and timestamp in one write under the current single-
writer/expected-revision protocol.

## Legacy transition

| Input | Read behavior | Write behavior |
| --- | --- | --- |
| Completed v1/v2 | Read unchanged | No migration solely for compatibility |
| Active v1/v2 status inspection | Read, report frontier unknown | No write |
| Active v1/v2 resume/update | Reconcile plan and repository first | One coherent migration to v3 |
| New delivery | Not applicable | Initialize v3 |
| Unknown version | Reject as unsupported | No write |

Migration preserves all existing fields, including `ownership`, plan revision, slices,
evidence, required context, and blockers. It populates only facts directly established from
the checkpoint and inspected repository. Unknown `last_completed`, `do_not_repeat`, or
verification facts use empty lists; unknown partial action uses null. Empty means unrecorded,
not proof that no such work exists, so recovery remains conservative.

The current verifier's field-preserving rewrite behavior is retained, but v3 validation is
added. Closing or mutating an active legacy checkpoint is rejected with a migration-required
issue until the recovery sequence has produced v3. Read/check operations may still explain
legacy state without mutating it.

## Invariants

1. Exactly one durable delivery checkpoint exists per session.
2. `revision` increases once per coherent write.
3. Repository evidence may contradict checkpoint claims; recovery must inspect before acting.
4. Frontier facts never override canonical slice/evidence/approval fields.
5. A path never leaves the repository root.
6. Migration never derives facts from conversation alone.
7. Writes preserve unrelated fields and working-tree changes.

## Verification obligations

Deterministic cases must cover v1/v2 reads, completed legacy no-migration, active migration,
unknown-to-empty behavior, ownership preservation, field-preserving v3 round trips, malformed
types, duplicate/escaping paths, unsupported versions, stale expected revision, and refusal to
close active legacy state before recovery.
