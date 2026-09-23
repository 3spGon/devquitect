# Durable Delivery State

Read this reference when initializing, reporting, resuming, handing off, repairing, or updating delivery. Store the single execution checkpoint at `docs/software-design/<slug>/09-delivery-status.md`.

## Initialization and schema

Create the checkpoint only after every authorization prerequisite in `SKILL.md` is satisfied. Copy only the `SLICE-*` identifiers covered by the user's explicit implementation authorization into `authorized_slices`, then initialize schema v3 at revision `1`:

```markdown
---
schema_version: 3
skill: project-plan-execution
project: Document Intake
session: document-intake
revision: 1
last_updated: "2026-08-27T10:00:00-06:00"
plan: 08-implementation-plan.md
plan_revision: 1
completion_scope: implementation-only
authorized_slices:
  - SLICE-01
  - SLICE-02
delivery_status: active
current_slice: SLICE-01
next_action: Implement SLICE-01 request correlation behavior
pending_user_action: null
required_context:
  - 02-requirements.md
  - 04-architecture.md
  - 08-implementation-plan.md
blockers: []
execution_frontier:
  last_completed: []
  in_progress:
    action: Implement SLICE-01 request correlation behavior
    paths: []
  do_not_repeat: []
  pending_verification: []
slices:
  SLICE-01:
    status: pending
    acceptance: not-required
  SLICE-02:
    status: pending
    acceptance: not-required
---

# Delivery checkpoint

## Current objective

## Last completed work

## Slice evidence

## Handoff notes
```

Use these exact values:

- `delivery_status`: `active`, `awaiting-input`, `awaiting-authorization`, `blocked`, or `complete`.
- Slice `status`: `pending`, `in-progress`, `implemented`, `verified`, `blocked`, `invalidated`, or `deferred`.
- Slice `acceptance`: `not-required`, `pending`, or `accepted`.

Required invariants:

- `schema_version` is `3` for new or migrated active checkpoints, `skill` is `project-plan-execution`, and `session` equals the containing slug.
- `revision` and `plan_revision` are positive integers. Increment `revision` exactly once per coherent checkpoint update.
- `last_updated` is ISO 8601 with an explicit UTC offset.
- `plan` and every `required_context` entry are relative paths inside the session directory.
- `authorized_slices` is a non-empty explicit list and every identifier exists in the approved plan and `slices` map.
- `authorized_slices` records authorized delivery scope; the tracker itself cannot grant or expand authorization.
- `completion_scope` is `implementation-only` unless the user explicitly authorizes a broader named scope.
- With `delivery_status: active`, `next_action` is concrete and agent-executable and `pending_user_action` is `null`.
- With `awaiting-input` or `awaiting-authorization`, `next_action` is `null` and `pending_user_action` states the minimum answer or authority needed.
- With `blocked`, `next_action` is `null`, `blockers` is non-empty, and `pending_user_action` is set only when the user can resolve it.
- With `complete`, `current_slice`, `next_action`, and `pending_user_action` are `null`; every authorized slice is `verified` or explicitly `deferred`, and no required acceptance is pending.
- `implemented` never implies verification. `verified` requires current evidence that every acceptance criterion and required command succeeded.
- `deferred` requires explicit authorization and a reason in the evidence body.
- `execution_frontier` is required in v3 and contains exactly these semantic members: `last_completed`, `in_progress`, `do_not_repeat`, and `pending_verification`. Unknown fields are preserved but do not acquire meaning.
- Frontier lists contain non-empty strings. `in_progress` is null or a mapping with a non-empty `action` and normalized repository-relative `paths`; paths cannot be absolute, escaping, duplicated, or backslash-separated.
- Frontier facts are reconstructive context only; they cannot establish slice status, evidence, acceptance, authorization, completion, or verification.

The Markdown body owns concise execution evidence and handoff context. Do not duplicate the full implementation plan or large command logs. A verified slice may link one `slices/<SLICE-ID>.md` detail; that file is the sole structured evidence record, while legacy status reads remain read-only.

## Link the definition checkpoint

After creating `09-delivery-status.md`, re-read `00-status.md` and apply its single-writer revision check. Add:

```yaml
delivery_checkpoint: 09-delivery-status.md
```

Increment the definition checkpoint revision once, but preserve `phase: complete`, `phase_status: complete`, approved gates, and null definition actions. This link is an index, not a second source of delivery truth. If `00-status.md` changed concurrently, stop and reconcile instead of writing the pointer blindly.

`00-status.md` establishes definition readiness through its phase and approved gates; it need not list authorized slices. An absent slice list there is neither a discrepancy nor a blocker. If its handoff notes explicitly limit delivery scope, treat that statement as authorization evidence, not as a second live tracker. A later explicit user authorization can supersede it. When the note and `authorized_slices` differ, reconcile them against the original and any later user authorization before executing affected slices or changing their scope. A tracker entry alone does not resolve the difference.

## Frontier refresh and legacy compatibility

Refresh the frontier, canonical fields, revision, and timestamp in one coherent write after a
functional change, consequential decision, completed migration, transition to verification, a
resolved verification failure, or a material recovery reconciliation. Routine reads and
individual commands do not force a checkpoint write.

Versions 1 and 2 remain readable. Completed legacy checkpoints stay byte-for-byte unchanged
unless an authorized operation already needs to update them. Active legacy checkpoints report
`tracker.migration-required` to verifier snapshot/check/close operations and are not rewritten;
the recovery workflow must reconcile repository evidence first and then perform one v3 migration.
Unknown versions are unsupported. Migration preserves existing fields, including `ownership`,
plan revision, slices, evidence, required context, and blockers. Unestablished frontier facts
remain empty or null and are never inferred from conversation.

## Discover and report

For status, resume, or handoff, search `docs/software-design/*/09-delivery-status.md`. Use the `delivery_checkpoint` from `00-status.md` when present.

- One matching session: read it directly.
- Several plausible sessions: report project, session, delivery status, current slice, last update, and current or pending action, then ask the user to choose.
- No tracker: report that durable execution has not started. Do not reconstruct one during status-only.

A status response reports authorized scope, plan revision, slice counts by state, current slice, last completed work, evidence summary, blockers, and active or pending action. It never writes files or executes the action.

## Update and resume

Only one agent writes a delivery session at a time. Other agents may report it read-only. Do not create locks, commits, or pushes.

Before every checkpoint write:

1. Remember the loaded `revision`.
2. Make and inspect the authorized repository changes or run the relevant verification.
3. Re-read `09-delivery-status.md` immediately before writing.
4. If its revision changed, discard the proposed checkpoint write, reload repository and session state, and reconcile with the other writer.
5. Record the coherent milestone and evidence, increment revision once, refresh `last_updated`, and set the next agent action or pending user action.
6. If the resulting status is `active`, continue immediately from `next_action`.

Resume according to durable state:

- `active`: execute `next_action` and continue through subsequent safe actions.
- Current slice `in-progress`: inspect existing changes and evidence before continuing; do not restart or assume correctness.
- Current slice `implemented`: execute its current verification before advancing.
- `awaiting-input` or `awaiting-authorization`: present only `pending_user_action` with minimum context.
- `blocked`: report the blocker and the condition needed to resolve it.
- `complete`: report the completed authorized scope and do not reopen it automatically.

A newly selected slice, changed revision, or new `next_action` is never a terminal condition.

## Plan changes and recovery

On every resume, compare the approved plan's `Plan revision` and status with the checkpoint:

- If the revision matches and the plan remains `Approved`, continue.
- If the plan is no longer approved, stop execution and request restoration of an approved plan through `$software-idea-to-project`.
- If the revision changed, perform an impact analysis before modifying code. Mark directly affected slices `invalidated`, then invalidate their transitive dependents. Preserve unaffected verified slices.
- If the change alters approved requirements, domain rules, architecture, interfaces, or ownership, stop implementation and return to `$software-idea-to-project` for the relevant gate invalidation and redesign.

If the tracker is missing or malformed during resume, recover conservatively from the approved plan, repository evidence, and recorded verification. Reconstruct `authorized_slices` only from explicit user authorization; the approved plan, repository changes, and previous tracker contents do not authorize additional slices. Never infer `verified`, `deferred`, acceptance, or authorization without evidence. Present actual discrepancies before writing a repaired tracker. If an explicit scope restriction in `00-status.md` conflicts with the proposed scope and no later authorization resolves it, leave the affected slices unexecuted and ask for the minimum clarification; continue unaffected authorized work when safe. Status-only remains read-only.

Recovery distinguishes plan or input invalidation, a recoverable verification failure, unavailable runtime
support, and a genuine blocker. Missing support is reported without installing dependencies; a manual
equivalent is not a supported close path. Legacy status reads remain read-only, and adopting the structured
evidence format requires an approved plan revision while preserving unaffected verified slices.
