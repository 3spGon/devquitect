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
- When behavioral testing is authorized and the user does not request another calibration, use `gpt-5.6-luna` with `--reasoning-effort high`.
- Credential-free checks are the default after changes.

## Evolving Devquitect skills

- This repository develops and refines Devquitect's skills and their quality tooling. Treat a
  change under `skills/` as a product-contract change, not as incidental documentation cleanup.
- Keep skill entrypoints concise, place detailed workflow rules with their designated reference,
  and use external deterministic cases to protect critical observable contracts.
- Do not optimize a skill from one end-to-end model miss alone. Compare changed behavior against
  the same stable model/runtime baseline; distinguish a reproducible candidate regression from
  shared model limitations, ordinary variance, and infrastructure failure.
- A safety property that needs certainty must be enforced by a deterministic guardrail, not only
  by an instruction to the model.

For a change to a critical skill rule:

1. Identify the affected contract in `authority-map.yaml` and edit the file at its `owner_path`.
2. Update that map when the owner or secondary paths change.
3. Add relevant positive and negative deterministic cases.
4. Run `uv run devquitect check --source working-tree`.
5. Before release eligibility, run the check against the candidate commit and use that report for
   `release-check`.

See `docs/contributing-skills.md` for the complete evidence and promotion workflow.

## Repository boundaries

- Preserve existing user changes and leave unrelated files untouched.
- Do not create commits, tags, pushes, installations, publications, deployments, or promotion approvals unless the user explicitly authorizes them.
- Changes under `skills/` require relevant positive and negative cases. Run credential-free checks first, then obtain or confirm authorization before any behavioral comparison.

## Optional local knowledge graph

When Graphify is installed and a local graph exists, it may accelerate codebase navigation.
Otherwise use normal repository navigation. Graphify output is local generated state and must not
be committed; update it after code changes only when the tool is available.
