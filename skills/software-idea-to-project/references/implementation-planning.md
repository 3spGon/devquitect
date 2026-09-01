# Adaptive Implementation Planning

Read this reference only after Gate 2 has been explicitly approved, or when the user supplies an architecture that demonstrably satisfies the readiness criteria. Planning remains a definition activity and does not authorize implementation.

## Choose evidence-based precision

The plan must be executable without leaving implementation-blocking decisions to its reader, but its details must come from evidence:

- In an existing repository, inspect relevant source, tests, configuration, build commands, and conventions. Use only verified paths, symbols, and commands.
- In greenfield work, derive a proposed structure from the approved architecture. Mark proposed paths as proposed until implementation creates them.
- Use the System Context as baseline orientation when present, but verify implementation-critical facts against repository evidence. Do not update the current baseline during planning.
- If an exact path, interface, dependency, or command cannot be established, resolve it before finalizing the plan or identify it as a blocker and stop at Gate 2.

Do not manufacture precision, paste production implementation code, or split work into arbitrary two-to-five-minute steps. A task boundary should represent a coherent, independently reviewable and testable result.

## Plan structure

Start with:

- document status, last-updated date, and a positive `Plan revision` beginning at `1`;
- goal and user-visible or system-visible outcome;
- approved design and architecture artifacts or chat decisions being implemented;
- approved experience decisions and referenced design evidence when applicable;
- relevant global constraints and non-goals;
- confirmed stack and repository context;
- non-blocking assumptions and deliberately deferred work.

For a `system-change` or `hybrid` initiative, also include the confirmed Change Profile or link to its canonical rationale. Preserve its affected surfaces, compatibility constraints, elevation reasons, and verification expectations in the slices that treat them; do not copy the full checkpoint mechanically.

Organize delivery into thin vertical slices that produce observable behavior. Give every slice a stable `SLICE-*` identifier that is unique within the plan. Each slice must state:

- outcome and observable acceptance criteria;
- dependencies and prerequisites;
- files to create or modify, distinguishing verified from proposed paths;
- interfaces consumed and produced, with names and shapes when established;
- domain rules, permissions, validation, errors, and failure behavior implemented;
- applicable interaction behavior, responsive rules, accessibility expectations, and design-system constraints implemented;
- test cases and the verification command;
- documentation, telemetry, migration, rollout, rollback, or compatibility work;
- a System Context refresh when the slice will materially change the implemented baseline;
- completion evidence.

Place a required System Context refresh inside the slice that changes the baseline, after its implementation and verification steps. Specify the affected sections and expected new baseline reference. Do not create a standalone speculative documentation slice or describe planned behavior as current before delivery succeeds.

Use the stable identifier in requirement, decision, test, and dependency mappings. Do not renumber existing identifiers merely because ordering changes. A material plan change returns the document to `Review`, increments `Plan revision`, and identifies the affected slices so an existing delivery tracker can invalidate only impacted work.

If planning exposes wider impact or a new disqualifier, stop treating the existing depth as authoritative. Elevate the Change Profile according to [change-profile.md](change-profile.md), invalidate the affected gates, and return to the earliest required phase before finalizing the plan.

Fold setup, configuration, schema, and documentation into the slice that needs them unless they form an independently testable deliverable. Order tasks so foundations precede consumers while each completed slice leaves the project in a coherent state.

## Validation coverage

Map approved requirements, applicable experience decisions, and significant risks to tasks and tests. Include happy paths, important edge cases, interaction states, responsive behavior, accessibility checks, authorization boundaries, invalid transitions, retries or duplicates, integration failures, migrations, rollback, and visual review only where they are relevant to the system. Do not require screenshot comparison, manual visual acceptance, or device-matrix testing unless the approved experience or repository evidence makes it necessary.

Commands must be copied from repository evidence or derived from an explicitly approved greenfield toolchain. State the expected signal of success or failure. Do not write vague steps such as “add validation,” “handle errors,” or “write tests” without specifying the behavior involved.

## Final readiness review

Before presenting the plan:

1. Confirm every approved requirement maps to at least one slice and verification method.
2. Confirm every applicable approved experience decision maps to at least one slice and verification method.
3. Confirm task interfaces, names, and paths are internally consistent.
4. Remove placeholders and implementation decisions disguised as tasks.
5. Confirm the sequence handles migrations, compatibility, rollout, and rollback where required.
6. Separate deferred non-goals from missing work.
7. Summarize any residual risk that implementation must monitor but does not need to decide.
8. Confirm every material baseline change schedules a proportional System Context refresh after verification, and that unchanged or merely planned behavior does not rewrite it.

In persistent mode, save the result as `08-implementation-plan.md` with status `Review` and `Plan revision: 1`, then mark it `Approved` only after explicit user approval. End by stating that implementation requires separate authorization and a concrete authorized slice list. When granted, hand execution to `$project-plan-execution`; do not execute the plan from this skill.
