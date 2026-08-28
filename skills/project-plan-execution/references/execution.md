# Authorized Slice Execution

Read this reference before implementing, resuming, verifying, or completing delivery slices.

## Preflight

Before the first code mutation and on resume:

1. Verify the authorization prerequisites and the tracker invariants.
2. Re-read applicable `AGENTS.md` and inspect the current repository status without discarding user work.
3. Confirm that the plan is still `Approved` at the recorded `plan_revision`.
4. Read only the current slice and its required canonical context.
5. Confirm its dependencies are `verified`, or explicitly `deferred` when the plan permits that dependency to be skipped.
6. Confirm its paths and commands against current repository evidence. Treat a mismatch as plan impact, not permission to invent a replacement architecture.

## Execution loop

For each ready authorized slice:

1. Record it as `in-progress` with an agent-executable `next_action`.
2. Implement only its approved behavior, tests, and necessary supporting changes. Preserve unrelated edits.
3. Inspect the resulting diff and map changes back to the slice's acceptance criteria.
4. Run the slice-specific commands from the plan plus any narrowly relevant repository checks required by the changed surface.
5. If all criteria and commands succeed, record concise evidence, set the slice to `verified`, select the next ready authorized slice, and continue without asking the user.
6. Use `implemented` only when code is present but verification must resume later. Never deliberately stop merely to expose that intermediate state.

Evidence for a verified slice includes:

- acceptance criteria evaluated and their observed outcomes;
- files materially changed;
- exact commands executed, exit result, and concise success signal;
- relevant manual or external checks and their provenance;
- timestamp and any residual risk that does not prevent acceptance.

Do not paste secrets or full logs. A command not run in the current relevant repository state is not evidence.

## Failures and blockers

When verification fails, keep the slice `in-progress` or `implemented`, diagnose the failure, correct it within the authorized design, and rerun the affected checks. Do not advance to dependent slices.

Use `blocked` only when progress requires inaccessible state, new authority, a material user-only decision, an unresolved conflict with user changes, or a plan/design correction outside the authorized scope. Record the concrete condition that clears the blocker. A difficult bug or an initial failed test is not by itself a blocker.

Required human or external acceptance uses `acceptance: pending` and `delivery_status: awaiting-input` only when the approved plan explicitly requires it. Ordinary slice completion never creates a user approval gate.

## Completion review

Before setting delivery to `complete`:

1. Confirm every authorized slice is `verified` or explicitly `deferred` with a reason and authorization.
2. Confirm every approved requirement in the authorized scope maps to a verified slice and current evidence.
3. Run the repository-supported regression, build, lint, typecheck, migration, compatibility, or packaging checks relevant to the cumulative changes.
4. Inspect the cumulative diff for unintended or out-of-scope changes.
5. Confirm no blockers, invalidated slices, required acceptance, or unresolved failures remain.
6. Record the final commands, results, deferred items, residual risks, and the exact completed scope.

`complete` means the authorized scope is verified. It does not imply deployment, release, commit, push, or completion of unauthorized plan slices. Report remaining unauthorized slices separately.

## External actions

Implementation authorization defaults to local code and tests only. Obtain specific authorization before installing dependencies when that changes the project, running migrations against shared data, provisioning services, committing, pushing, opening or merging changes, deploying, or mutating external systems. Record approved external actions and their evidence without broadening future permission.
