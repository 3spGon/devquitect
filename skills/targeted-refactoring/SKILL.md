---
name: targeted-refactoring
description: Assess, plan, implement, or review narrowly scoped, behavior-preserving refactors in an existing codebase. Use for explicit requests to refactor, simplify structure, remove confirmed dead code, reduce duplication, split oversized code, or modernize a specific area; do not use for general implementation, speculative cleanup, architecture redesign, framework migrations, dependency upgrades, or unrelated style changes.
---

# Targeted Refactoring

Improve code structure through the smallest justified change that preserves intended behavior. A valid outcome may be a completed refactor, a bounded proposal, or a recommendation not to refactor.

## Establish intent and evidence

Before changing files:

1. Locate and follow every applicable `AGENTS.md` from the workspace root to the files in scope.
2. Inspect the repository status, relevant source, tests, configuration, and established conventions. Preserve unrelated user changes.
3. Classify the request:
   - **Review** — determine whether a refactor is justified; do not edit.
   - **Plan** — produce an implementation-ready refactor plan; do not edit.
   - **Execute** — implement an explicitly requested refactor.
   - **Diff review** — assess an existing refactor without changing it unless the user also requests fixes.
4. Identify the concrete maintenance cost, structural defect, or delivery risk motivating the refactor. Do not treat subjective cleanliness alone as sufficient evidence.

Do not infer edit authorization from requests to inspect, review, assess, explain, or plan. An explicit request to refactor authorizes only the bounded repository changes needed for that refactor, not commits, pushes, deployments, dependency upgrades, or external mutations.

## Define the refactor contract

Before implementation, establish:

- the structural problem and evidence that it exists;
- the intended improvement;
- the observable behavior and contracts that must remain stable;
- the code reasonably in scope and the code explicitly out of scope;
- the checks that can demonstrate parity;
- the conditions that would invalidate or materially expand the work.

Keep this contract proportional to the change. It may be a concise working summary for a local refactor rather than a separate artifact.

Recommend no refactor when the problem is not evidenced, the benefit does not justify the diff, a smaller non-structural change resolves the issue, or behavior cannot be preserved with acceptable confidence.

## Choose the smallest safe workflow

Execute directly when the refactor is local, reversible, already authorized, does not change a public contract, and has a clear verification path.

Form a brief plan before editing when the work crosses modules, affects shared dependencies or public interfaces, touches sensitive behavior such as authentication, concurrency, or persistence, lacks adequate tests, presents materially different approaches, or begins to grow beyond the original request. If execution is already authorized and the plan exposes no material user decision, continue without requesting another approval.

Stop before implementation and separate the work when it requires a feature decision, behavior change, framework or dependency migration, data migration, public API redesign, new architecture, or a multi-session delivery program. Route persistent definition and architectural planning to `$software-idea-to-project`; route implementation to `$project-plan-execution` only after that workflow has produced and authorized an eligible persistent plan.

## Implement a minimal coherent refactor

- Preserve behavior unless the user separately authorizes a functional change.
- Keep every changed file and edit traceable to the refactor contract.
- Prefer established repository patterns over introducing a new abstraction or convention.
- Do not mix opportunistic cleanup, unrelated renaming, formatting churn, dependency changes, or adjacent fixes into the refactor.
- Keep public APIs, serialized formats, schemas, side effects, error behavior, and operational contracts stable unless separately authorized.
- Add an abstraction only when current evidence supports it; do not design for speculative reuse.
- Treat dead-code removal as an evidence task. Check direct and indirect references, configuration, registration, reflection, generated use, scripts, and runtime discovery as applicable before deleting.
- Preserve unrelated working-tree changes. If they overlap the target and cannot be safely isolated, stop and report the conflict.

When functional and structural changes are both requested, separate them into independently explainable and verifiable passes whenever practical. Never conceal a behavior change inside a refactor.

## Verify parity and scope

Use evidence proportional to the affected surface:

1. Run or inspect the narrowest meaningful baseline before editing when feasible. Distinguish pre-existing failures from regressions.
2. Run focused tests and static checks for the changed behavior.
3. Run broader tests, builds, or checks when shared code or public contracts are affected.
4. Review the final diff for accidental scope growth, behavior changes, formatting churn, and unrelated edits.
5. State any verification that could not be performed and the resulting residual risk.

Do not claim that behavior was preserved from code inspection or expectation alone when an executable verification path exists.

## Report the result

Lead with the outcome. State:

- whether the refactor was performed, proposed, or rejected as unnecessary;
- the concrete reason and bounded scope;
- the behavior or contracts preserved;
- the verification commands and observed results;
- any unresolved risk or separately deferred opportunity.

Do not turn deferred cleanup ideas into implied follow-up authorization.
