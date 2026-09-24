---
name: project-plan-execution
description: Execute, resume, or report the status of an explicitly authorized implementation from an approved persistent technical plan, tracking verification evidence for each delivery slice. Use when code delivery must continue across chats; do not use for unapproved plans, ordinary ad hoc coding, design work, or automatic deployment.
---

# Project Plan Execution

Implement explicitly authorized slices from an approved persistent plan. Keep code written separate from delivery verified, and preserve traceability from each slice to its requirements, changes, checks, and evidence.

## Establish authority and session

Follow the authorized handoff preflight in [execution.md](references/execution.md) before starting delivery or changing files.

Follow applicable `AGENTS.md` files and preserve current user changes. For status, resume, or handoff, select the session from its durable checkpoints; if several remain plausible, ask the user to choose. Read [delivery-state.md](references/delivery-state.md) and, for recovery after lost context, [compaction-recovery.md](references/compaction-recovery.md). Status-only is read-only.

Use `09-delivery-status.md` as the sole execution checkpoint. Initialize and update it using [delivery-state.md](references/delivery-state.md); keep scope `implementation-only` unless broader authority is explicit. Implementation authorization does not include commits, pushes, deployments, provisioning, production mutations, or other external actions.

## Execute authorized slices

While delivery is active, execute its `next_action` and continue through safe, ready work without treating checkpoint updates as a stopping point. Work only within authorized slices and return new architecture or design decisions to `$software-idea-to-project`.

A slice is complete only when every applicable criterion and required check has current evidence and the supported close path records `verified`. Read [slice-verification.md](references/slice-verification.md) and use [`verify_slice.py`](scripts/verify_slice.py) for `snapshot`, `check`, and `close`. Before running it, confirm Python 3.12+ and PyYAML are available; report missing support without installing dependencies or using a manual equivalent.

Preserve unrelated changes, do not claim unrun verification, and do not mark work `deferred` without explicit authorization and a recorded reason. Keep the checkpoint accurate before yielding; `complete` means only the authorized scope is verified.
