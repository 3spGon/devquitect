---
name: quick-change
description: Use for explicitly authorized, localized, reversible changes with a direct verification path and no material product or behavior decision. Do not use for new features, architecture or public-contract changes, persistence, security-sensitive behavior, migrations, multi-module work, or durable continuity; route those to the established workflow. Explicit invocation selects this skill but does not broaden its scope.
---

# QUICK

Make one authorized, bounded change in an existing codebase.

- Confirm the exact requested outcome and inspect the relevant files, callers, and repository instructions.
- Proceed only when the change is localized, reversible, and has a direct way to verify it without a material product or behavior decision.
- Stop before editing if it involves a feature or architecture decision, a public contract, persistence, security-sensitive behavior, a migration, multiple modules, or work that needs durable continuity. Route product, architecture, contract, security, persistence, migration, and multi-module work to `$software-idea-to-project`; use `$project-plan-execution` for an existing approved slice; use `$targeted-refactoring` for behavior-preserving structural refactors.
- An explicit `$quick-change` invocation selects this workflow, but does not grant implementation authority or suppress escalation.
- Change only the in-scope files, run the direct check and relevant focused validation, inspect the diff, and report the result briefly. Do not create a universal router or take external actions without authorization.
