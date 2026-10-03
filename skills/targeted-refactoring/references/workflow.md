# Targeted Refactoring Workflow

Use this reference for review, planning, implementation, or diff review under [the skill entrypoint](../SKILL.md). It owns the detailed evidence, scope, behavior-preservation, and verification rules.

## Establish intent and evidence

Before changing files:

1. Locate and follow every applicable `AGENTS.md` from the workspace root to the files in scope.
2. Inspect repository status, relevant source, tests, configuration, and conventions. Preserve unrelated user changes.
3. Classify the request as **Review** (assess without editing), **Plan** (produce an implementation-ready plan without editing), **Execute** (perform an explicitly requested refactor), or **Diff review** (assess an existing refactor; change it only when fixes are also requested).
4. Identify the concrete maintenance cost, structural defect, or delivery risk. Subjective cleanliness alone is not sufficient evidence.

Do not infer edit authorization from inspection, review, assessment, explanation, or planning requests. An explicit refactor request authorizes only the bounded repository changes needed for that refactor, not commits, pushes, deployments, dependency upgrades, or external mutations.

## Define the refactor contract

Before implementation, establish:

- the structural problem and evidence that it exists;
- the intended improvement;
- observable behavior and contracts that must remain stable;
- code in scope and explicitly out of scope;
- checks that can demonstrate parity; and
- conditions that would invalidate or materially expand the work.

Keep the contract proportional; a local refactor may need only a concise working summary. Recommend no refactor when the problem is not evidenced, the benefit does not justify the diff, a smaller non-structural change resolves it, or behavior cannot be preserved with acceptable confidence.

## Choose the smallest safe workflow

Execute directly when the refactor is local, reversible, authorized, does not change a public contract, and has a clear verification path.

Form a brief plan before editing when work crosses modules, affects shared dependencies or public interfaces, touches authentication, concurrency, or persistence, lacks adequate tests, presents materially different approaches, or grows beyond the request. Continue without another approval when execution is already authorized and the plan exposes no material user decision.

Stop before implementation when work requires a feature decision, behavior change, framework or dependency migration, data migration, public API redesign, new architecture, or a multi-session delivery program. Route persistent design and architecture to `$software-idea-to-project`; use `$project-plan-execution` only after an approved persistent plan names the authorized slices.

## Implement a minimal coherent refactor

- Preserve behavior unless the user separately authorizes a functional change.
- Keep every changed file traceable to the refactor contract and prefer established repository patterns.
- Exclude opportunistic cleanup, unrelated renaming, formatting churn, dependency changes, and adjacent fixes.
- Keep public APIs, serialized formats, schemas, side effects, errors, and operational contracts stable unless separately authorized.
- Add abstractions only when current evidence supports them; do not design for speculative reuse.
- Before deleting dead code, check direct and indirect references, configuration, registration, reflection, generated use, scripts, and runtime discovery as applicable.
- Preserve unrelated working-tree changes. If they overlap the target and cannot be safely isolated, stop and report the conflict.

When functional and structural changes are both requested, separate them into independently explainable and verifiable passes when practical. Never conceal a behavior change inside a refactor.

## Verify parity and scope

Use evidence proportional to the affected surface:

1. Run or inspect the narrowest meaningful baseline before editing when feasible; distinguish existing failures from regressions.
2. Run focused tests and static checks for changed behavior.
3. Run broader checks when shared code or public contracts are affected.
4. Review the final diff for scope growth, behavior changes, formatting churn, and unrelated edits.
5. Report checks that could not run and the resulting residual risk.

When an executable verification path exists, code inspection or expectation alone does not establish behavior preservation.

## Report the result

Lead with whether the refactor was performed, proposed, or rejected; its evidence-based reason and bounded scope; preserved behavior; observed verification; and unresolved risk or deferred work. Do not turn deferred cleanup into implied authorization.
