---
name: project-plan-execution
description: Execute, resume, or report the status of an explicitly authorized implementation from an approved persistent technical plan, tracking verification evidence for each delivery slice. Use when code delivery must continue across chats; do not use for unapproved plans, ordinary ad hoc coding, design work, or automatic deployment.
---

# Project Plan Execution

Implement an approved plan without confusing code written with delivery verified. Preserve traceability from authorized slices to repository changes, acceptance behavior, commands, and observed evidence.

## Establish the execution context

Before changing files:

1. Locate and follow every applicable `AGENTS.md` from the workspace root to the files in scope.
2. Inspect `docs/software-design/*/00-status.md` and `09-delivery-status.md`, then identify the intended persistent session. If several sessions are plausible, summarize them and ask the user to choose; never select silently.
3. Inspect the relevant repository state, approved artifacts, source, tests, configuration, and verified commands. Preserve user changes and existing conventions.
4. Classify the request as **start**, **status**, **resume**, or **handoff**.

For status or resume, read [references/delivery-state.md](references/delivery-state.md). Read `09-delivery-status.md` first, followed only by its `required_context`. A status-only request is read-only and must not execute, repair, initialize, or advance delivery.

## Require an authorized handoff

Start delivery only when all of these conditions are evidenced:

- the definition uses a persistent session under `docs/software-design/<slug>/`;
- `00-status.md` records Gate 1 and Gate 2 as approved and the definition phase as complete;
- `08-implementation-plan.md` is `Approved`, has a positive `Plan revision`, and uses stable `SLICE-*` identifiers;
- the user explicitly authorized implementation;
- the authorized slice list is concrete.

Treat an explicit request to implement the entire approved plan as authorization for every slice in that plan and enumerate them in the tracker without asking again. For narrower authorization, include only the slices the user identified or whose requested outcome unambiguously selects them.

Default `completion_scope` to `implementation-only`. Authorization to implement does not authorize commits, pushes, deployments, provisioning, production mutations, or other external side effects. If any prerequisite is absent, do not modify application code or create a delivery checkpoint; report the missing condition or return design work to `$software-idea-to-project`.

When starting or updating durable delivery state, follow [references/delivery-state.md](references/delivery-state.md). `09-delivery-status.md` is the sole durable execution checkpoint; do not create parallel JSON state.

## Execute and verify

Read [references/execution.md](references/execution.md) before implementing or resuming slices. Work only within the authorized scope and carry forward the approved requirements, architecture, assumptions, deferred decisions, and repository instructions.

While `delivery_status` is `active`, execute `next_action` without asking for confirmation. Complete multiple safe, coherent actions in the same turn. Updating a slice, checkpoint revision, evidence entry, or `next_action` is bookkeeping, not a stopping condition.

A slice is complete only when it is `verified`. `implemented` means verification remains. Continue automatically to the next ready authorized slice after verification. Stop only for unavailable user-only information, required authorization, an unresolved blocker, required human acceptance, an invalidated plan or design, or completion of the authorized scope.

## Preserve boundaries

- Do not expand implementation beyond authorized slices or silently resolve a new architecture decision in code.
- Do not overwrite user changes, rewrite unrelated files, or discard conflicting work.
- Do not claim verification from an unexecuted command, an old result, or expectation alone.
- Do not record secrets or unnecessarily large logs in delivery artifacts.
- Do not mark a slice `deferred` without explicit user authorization and a recorded reason.
- Do not mark delivery `complete` while an authorized slice is pending, in progress, implemented, blocked, invalidated, or awaiting required acceptance.

Lead each response with the current delivery result. Before deliberately yielding, make the durable checkpoint accurately describe the next agent action, pending user action, blocker, or completed scope.
