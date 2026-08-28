# Durable Session State

Read this reference when starting persistent mode, reporting workflow status, resuming or handing off a session, updating a checkpoint, migrating schema v1, or recovering inconsistent state. `00-status.md` is the single durable representation of workflow state; do not create a parallel JSON state file.

Checkpointing records continuity. It does not control ordinary turn boundaries. While a session is active, saving a new `next_action` must be followed by executing it when that work is safe and in scope.

## State location and schema

Store the checkpoint at `docs/software-design/<slug>/00-status.md`. Initialize new persistent sessions with schema version `2` and revision `1`:

```markdown
---
schema_version: 2
skill: software-idea-to-project
project: Document Intake
session: document-intake
workflow_mode: persistent
revision: 1
phase: frame
phase_status: active
gate_1: not-ready
gate_2: not-ready
last_updated: "2026-08-27T10:00:00-06:00"
next_action: Map how incoming email correlates to a request using current evidence
pending_user_action: null
required_context: []
blockers: []
open_decisions: []
artifacts:
  brainstorm.md: active
---

# Current checkpoint

## Current objective

State the immediate outcome of the current phase.

## Last completed work

Summarize the last coherent milestone, decision, or artifact update.

## Handoff notes

Record only context another agent needs before taking the next action.
```

Use these exact values:

- `phase`: `frame`, `expand`, `explore`, `research`, `refine`, `crystallize`, `technical-design`, `implementation-planning`, or `complete`.
- `phase_status`: `active`, `awaiting-input`, `awaiting-approval`, `blocked`, or `complete`.
- `gate_1` and `gate_2`: `not-ready`, `pending`, `approved`, or `invalidated`.
- Existing artifact status: `active`, `draft`, `review`, or `approved`.

Required invariants:

- `schema_version` is `2`, `skill` is `software-idea-to-project`, and `workflow_mode` is `persistent`.
- `session` equals the containing directory slug.
- `revision` is a positive integer and increases by one for every completed checkpoint update.
- `last_updated` is an ISO 8601 timestamp with an explicit UTC offset.
- When `phase_status: active`, `next_action` is a concrete action executable by the agent and `pending_user_action` is `null`.
- When `phase_status` is `awaiting-input` or `awaiting-approval`, `next_action` is `null` and `pending_user_action` states exactly what the user must answer or approve.
- When `phase_status: blocked`, `next_action` is `null`, `blockers` is not empty, and `pending_user_action` is populated only if the user can resolve the blocker.
- When `phase_status: complete`, `phase` is `complete` and both `next_action` and `pending_user_action` are `null`.
- `required_context` contains only relative paths within the session directory and only the minimum files needed for the active action or pending user action.
- `blockers` and `open_decisions` are arrays, empty when none exist. Prefer stable decision identifiers when the project already uses them.
- `artifacts` lists existing session artifacts only. Do not list hypothetical or uncreated files.
- `delivery_checkpoint` is optional and absent until authorized execution initializes `09-delivery-status.md`. When present, its value is exactly `09-delivery-status.md`.
- The Markdown body summarizes process context; it does not duplicate requirements, architecture, or contracts owned by canonical documents.

## Autonomy and terminal conditions

`phase_status`, not `next_action`, determines whether execution continues.

While `phase_status: active`:

1. Execute `next_action` without asking for confirmation.
2. Inspect repository evidence, canonical artifacts, constraints, and authoritative technical sources before asking the user.
3. Use an explicit, reversible assumption when uncertainty is non-blocking.
4. After a material milestone, save the resulting checkpoint and immediately continue with its new `next_action` when safe and in scope.
5. Complete multiple coherent actions before yielding; do not expose every internal checkpoint as a conversational stop.

Changing `next_action`, incrementing `revision`, updating an artifact, or completing one decision is never by itself a reason to end the turn.

Change to `awaiting-input` only when the missing information cannot be discovered and a wrong assumption would materially alter scope, architecture, safety, cost, permissions, or irreversible work. The two approval gates remain mandatory terminal conditions. Use `blocked` for required authority, unavailable external state, contradictions, or other conditions the agent cannot resolve within scope.

If a turn ends at a natural boundary while still `active`, preserve an agent-executable `next_action` and report it as status, not as a question or request for permission.

## Discover and report sessions

For status, resume, or handoff requests, search `docs/software-design/*/00-status.md` before relying on conversation context.

- When the user names a project or slug, match that session first.
- With exactly one relevant checkpoint, use it without making the user identify it again.
- With multiple plausible checkpoints, list `project`, `session`, `phase`, `phase_status`, `last_updated`, and either `next_action` or `pending_user_action`, then wait for selection.
- With no checkpoint, look for existing `docs/software-design/<slug>/` artifacts only to offer recovery. Do not reconstruct or write state during a read-only status request.

A status response reports the current phase, phase status, both gates, last completed work, blockers, open decisions, the active next action, and any pending user action. When `delivery_checkpoint` is present, also read it and report delivery status, authorized scope, slice counts, current slice, evidence summary, delivery blockers, and its active or pending action as a separate section. It does not mutate documents, execute either action, advance a phase, resolve a blocker, migrate schema, or repair inconsistencies.

When status-only reads a schema v1 checkpoint, interpret it in memory, report that migration is pending, and leave the file unchanged.

## Resume by state

Read the selected `00-status.md`, migrate schema v1 when necessary, then read only `required_context`. Verify the schema and compare the checkpoint with declared artifact statuses before continuing.

- `active` — execute `next_action` without confirmation, then continue through additional safe actions until a genuine terminal condition.
- `awaiting-input` — present only `pending_user_action` with the minimum context needed to answer it.
- `awaiting-approval` — present the gate recorded in `pending_user_action` and do not advance without explicit approval.
- `blocked` — explain the blocker and the recorded condition or authority needed to resolve it.
- `complete` — report definition completion and do not reopen it automatically. If `delivery_checkpoint` exists, include its separate state; use `$project-plan-execution` for delivery resume or repair.
- Any gate marked `invalidated` — return to the earliest affected phase and update dependent artifacts before advancing again.

Lead a resume response with a compact handoff summary so the user can detect a wrong session or stale state. That summary does not require confirmation when the selected session is unambiguous and active.

## Update ordering and cadence

Update durable state after a meaningful milestone, phase change, genuinely blocking question, gate transition, new or resolved blocker, artifact status change, gate invalidation, implementation-plan completion, or deliberate handoff. Do not rewrite it after messages that change nothing, and do not treat an update as a reason to yield.

For every coherent transition:

1. Read and remember the current `revision`.
2. Update the affected canonical documents.
3. Append the meaningful milestone to `brainstorm.md` when history changed.
4. Re-read `00-status.md` immediately before writing it. If `revision` differs from the remembered value, stop, reload the session, and reconcile with the other writer; do not merge blindly.
5. Update the checkpoint last, increment `revision` exactly once, refresh `last_updated`, and set either the next agent action or pending user action according to `phase_status`.
6. If the new state is `active`, continue working immediately from `next_action`.

Only one agent writes a session at a time. Other agents may read and report status. Do not create lock files, automatically commit, or automatically push checkpoint changes.

Before deliberately yielding for input or approval, becoming blocked, completing the workflow, or handing off, make the checkpoint describe that terminal state. An unexpected interruption may leave it behind, so recovery must remain conservative.

## Gates and invalidation

Before requesting Gate 1 approval, set `phase: crystallize`, `phase_status: awaiting-approval`, `gate_1: pending`, `next_action: null`, and make `pending_user_action` request approval or revision of the design. After explicit approval, mark the relevant canonical documents `Approved`, set `gate_1: approved`, move to `technical-design`, set `phase_status: active`, clear `pending_user_action`, record an agent-executable `next_action`, and continue technical design in the same turn.

Before requesting Gate 2 approval, set `phase: technical-design`, `phase_status: awaiting-approval`, `gate_2: pending`, `next_action: null`, and make `pending_user_action` request architecture approval. After explicit approval, mark the relevant technical documents `Approved`, set `gate_2: approved`, move to `implementation-planning`, set `phase_status: active`, clear `pending_user_action`, record an agent-executable `next_action`, and continue planning in the same turn.

If an approved canonical document returns to `Draft` or `Review`, invalidate every dependent gate. Gate 1 invalidation also invalidates Gate 2. Return to the earliest phase needed to restore consistency.

When the implementation plan is approved, set `phase: complete`, `phase_status: complete`, both gates to `approved`, `next_action: null`, and `pending_user_action: null`, then summarize the final handoff. This records completion of the definition workflow, not authorization to implement.

After separate implementation authorization, `$project-plan-execution` may create `09-delivery-status.md` and add `delivery_checkpoint: 09-delivery-status.md` using this checkpoint's revision check. Increment the definition revision once while preserving its complete phase, approved gates, and null actions. The pointer is only an index; `09-delivery-status.md` remains authoritative for delivery and subsequent delivery updates do not rewrite `00-status.md`.

## Migrate schema v1 to v2

Migrate a valid schema v1 checkpoint only when the user resumes, repairs, or otherwise updates the session. A status-only request never writes the migration.

Before migration, apply the single-writer revision check. Preserve all unaffected fields, set `schema_version: 2`, increment `revision` once, refresh `last_updated`, add `pending_user_action`, and record the migration in `brainstorm.md`.

Convert execution fields by the existing `phase_status`:

- `active` — reformulate the old `next_action` as an agent-executable action, keep it in `next_action`, and set `pending_user_action: null`. If the old value clearly requires a material decision that only the user can make, change to `awaiting-input`, move that request to `pending_user_action`, and set `next_action: null`.
- `awaiting-input` or `awaiting-approval` — move the old `next_action` to `pending_user_action` and set `next_action: null`.
- `blocked` — set `next_action: null`; move the old value to `pending_user_action` only when it describes an action the user can take. Ensure `blockers` is not empty.
- `complete` — set both fields to `null`.

Classify an old value as user-only only when it requests a preference, approval, authority, inaccessible fact, or consequential choice that cannot be derived or assumed safely. Wording such as “clarify,” “decide,” or “choose” alone is not sufficient; first determine whether the agent can resolve it using evidence or a reversible assumption.

After migrating an `active` session, continue autonomously from the migrated `next_action` in the same turn.

## Recover missing, corrupt, or stale state

Canonical numbered documents through `08` remain authoritative for requirements, technical design, and the approved plan. `00-status.md` is authoritative for definition workflow state. `09-delivery-status.md`, when present, is authoritative for delivery. `brainstorm.md` is historical evidence.

When resuming and the checkpoint is missing, malformed, or inconsistent:

1. Inspect canonical document statuses and their latest coherent content.
2. Read only the relevant milestones and explicit approvals from `brainstorm.md`.
3. Choose the earliest phase consistent with the available evidence.
4. Treat uncertain approvals as `pending`; never infer approval merely because a document looks complete.
5. If a checkpoint claims an approved gate while a dependent document is `Draft` or `Review`, mark the gate `invalidated`.
6. Reconstruct schema v2 using the phase-status invariants above.
7. Present the reconstructed state and discrepancies to the user.
8. Write the repaired checkpoint only when the user asked to resume or repair, not when they requested status only.

Preserve a valid existing revision by incrementing it during repair. For a missing or unreadable checkpoint, initialize the repaired file at revision `1` and note the recovery in `brainstorm.md`.

## Portability boundary

Durable continuity requires access to the same session files. Another chat using the same checkout can resume them. Another worktree, host, or machine can resume only after the files are synchronized through Git or shared storage. State this limitation when a handoff target cannot see the current checkout.
