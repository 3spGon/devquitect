# Repository instructions

These instructions apply to the entire repository.

## Verification after changes

- After changing any repository file, run the credential-free verification suite before declaring the work complete:
  1. `uv run devquitect check --source working-tree --report .devquitect-reports/check.json`
  2. `uv run ruff check src tests`
  3. `git diff --check`
- Run additional focused tests when the changed area has a more specific relevant suite.
- Do not claim that work is complete or verified when a required command was skipped or failed. Report failures and infrastructure limitations clearly.

## Behavioral tests and usage

- Do not run `devquitect eval`, `devquitect compare`, or `devquitect check --behavioral` unless the user explicitly authorizes model-backed testing for the current task.
- When behavioral testing is authorized and the user does not request another calibration, use `gpt-5.4-mini` with `--reasoning-effort low`.
- Credential-free checks are the default after changes.

## Repository boundaries

- Preserve existing user changes and leave unrelated files untouched.
- Do not create commits, tags, pushes, installations, publications, deployments, or promotion approvals unless the user explicitly authorizes them.
- Changes under `skills/` require relevant positive and negative cases. Run credential-free checks first, then obtain or confirm authorization before any behavioral comparison.
