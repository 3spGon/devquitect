# Adaptive Implementation Planning

Read this reference only after Gate 2 has been explicitly approved, or when the user supplies an architecture that demonstrably satisfies the readiness criteria. Planning remains a definition activity and does not authorize implementation.

## Choose evidence-based precision

The plan must be executable without leaving implementation-blocking decisions to its reader, but its details must come from evidence:

- In an existing repository, inspect relevant source, tests, configuration, build commands, and conventions. Use only verified paths, symbols, and commands.
- In greenfield work, derive a proposed structure from the approved architecture. Mark proposed paths as proposed until implementation creates them.
- If an exact path, interface, dependency, or command cannot be established, resolve it before finalizing the plan or identify it as a blocker and stop at Gate 2.

Do not manufacture precision, paste production implementation code, or split work into arbitrary two-to-five-minute steps. A task boundary should represent a coherent, independently reviewable and testable result.

## Plan structure

Start with:

- document status, last-updated date, and a positive `Plan revision` beginning at `1`;
- goal and user-visible or system-visible outcome;
- approved design and architecture artifacts or chat decisions being implemented;
- relevant global constraints and non-goals;
- confirmed stack and repository context;
- non-blocking assumptions and deliberately deferred work.

Organize delivery into thin vertical slices that produce observable behavior. Give every slice a stable `SLICE-*` identifier that is unique within the plan. Each slice must state:

- outcome and observable acceptance criteria;
- dependencies and prerequisites;
- files to create or modify, distinguishing verified from proposed paths;
- interfaces consumed and produced, with names and shapes when established;
- domain rules, permissions, validation, errors, and failure behavior implemented;
- test cases and the verification command;
- documentation, telemetry, migration, rollout, rollback, or compatibility work;
- completion evidence.

Use the stable identifier in requirement, decision, test, and dependency mappings. Do not renumber existing identifiers merely because ordering changes. A material plan change returns the document to `Review`, increments `Plan revision`, and identifies the affected slices so an existing delivery tracker can invalidate only impacted work.

Fold setup, configuration, schema, and documentation into the slice that needs them unless they form an independently testable deliverable. Order tasks so foundations precede consumers while each completed slice leaves the project in a coherent state.

## Validation coverage

Map approved requirements and significant risks to tasks and tests. Include happy paths, important edge cases, authorization boundaries, invalid transitions, retries or duplicates, integration failures, migrations, and rollback only where they are relevant to the system.

Commands must be copied from repository evidence or derived from an explicitly approved greenfield toolchain. State the expected signal of success or failure. Do not write vague steps such as “add validation,” “handle errors,” or “write tests” without specifying the behavior involved.

## Final readiness review

Before presenting the plan:

1. Confirm every approved requirement maps to at least one slice and verification method.
2. Confirm task interfaces, names, and paths are internally consistent.
3. Remove placeholders and implementation decisions disguised as tasks.
4. Confirm the sequence handles migrations, compatibility, rollout, and rollback where required.
5. Separate deferred non-goals from missing work.
6. Summarize any residual risk that implementation must monitor but does not need to decide.

In persistent mode, save the result as `08-implementation-plan.md` with status `Review` and `Plan revision: 1`, then mark it `Approved` only after explicit user approval. End by stating that implementation requires separate authorization and a concrete authorized slice list. When granted, hand execution to `$project-plan-execution`; do not execute the plan from this skill.
