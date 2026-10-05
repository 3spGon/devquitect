# Devquitect Next concept

Status: Approved
Last updated: 2026-10-03

## Confirmed

Devquitect Next evolves the existing skill set without collapsing its authority boundaries. It has three staged outcomes:

1. **0.7.0 — operating model:** keep skill entrypoints concise around outcomes, hard constraints, approval boundaries, readiness, and stopping conditions; add QUICK as an independent route for authorized, local, reversible changes. GPT-5.6 remains the generation baseline for prompt evidence, not the only intended model generation.
2. **0.8.0 — follow-on scope:** reserve the release for work selected after 0.7.0 evidence; it does not modify distributed slice verification.
3. **1.0.0 — continuous verification and release readiness:** stabilize the skill, escalation, and existing verification contracts using credential-free CI from a clean runner, then establish exact-candidate release eligibility for a separate human publication decision.

The expanded initiative also generalizes proportional workflow depth beyond system changes, permits a durable definition root to be detected or configured rather than fixed to one path, defines the invocation policy for each skill, and measures the evolved workflows across a declared multi-generation model/host matrix. Its initial comparison includes GPT-5.6 Sol, Terra, and Luna as the prior-generation baseline, plus GPT-6 Sol and Luna as separate rows.

Actors are a user requesting repository work, a Codex agent selecting and applying a Devquitect workflow, and maintainers who publish the skill and verification contracts.

### DN-005 / DN-006 amendment for review

The user approved amended Gate 1 on 2026-10-03 after reviewing the Continuous Verification and Release Readiness changes. This approves the expanded behavior and boundaries, not Gate 2, plan revision 3, implementation, or release actions. DN-001 through DN-004 retain their existing scope and delivered evidence. DN-005 and DN-006 are the affected future slices.

The current checkout has local structural checks, tests, Ruff, deterministic packaging, and `release-check`, but no `.github/workflows/` implementation. The packager already rejects a requested version that differs from the committed plugin manifest. `release-check` reconstructs packages twice and requires a credential-free check for the same commit and snapshot; it does not consume a CI ZIP directly and currently compares version compatibility against the candidate's immediate parent.

DN-005 answers whether a candidate is technically valid: GitHub Actions repeats the deterministic checks from a clean, locked environment, exercises Linux/macOS/Windows surfaces, produces a reproducible canonical package, and records the tested source and execution identity. Local checks remain necessary. Required checks and effective branch protection establish merge eligibility; merely documenting protection does not activate it.

DN-006 answers whether release evidence belongs to the exact candidate: it selects successful CI for that SHA, verifies the downloaded package and manifest, checks version consistency, and uses `release-check` to produce an unapproved eligibility proposal. The source of truth is the full candidate SHA, not a mutable branch, artifact name, or a passing report from another commit.

PR evidence identifies the proposed integration; CI on `main` verifies the final integrated SHA again. Release readiness consumes evidence for the exact candidate, without treating squash, rebase, or equal trees as implicit commit equivalence. Authorized behavioral evidence remains supplementary, independent per model/runtime configuration, and cannot repair a deterministic failure.

The affected Change Profile remains full / rigorous and cross-cutting: this adds an external CI boundary, evidence provenance, merge gates, and release-eligibility behavior. Existing source identities and tooling should be reused rather than introducing a general release-management system.

QUICK is bounded to direct, localized implementation work. It is eligible for implicit activation through its precise skill description and remains explicitly invocable by a user. It escalates rather than proceeds when the task introduces a feature or product decision, crosses important module or public-interface boundaries, changes persistence or security behavior, requires a migration, or becomes a multi-session effort.

## Assumptions

- The 0.x release line remains the public development line; "v2" is an internal initiative label, not a proposed 2.0.0 release.
- `verify_slice.py`, its Python/PyYAML dependency, YAML inventory, and acceptance contract remain unchanged.

## Open decisions

- None. Gate 1, Gate 2, and plan revision 3 have explicit approval; the existing ledger and model matrix are not reopened. Implementation still requires concrete slice authorization.

## Interaction scope

The interaction surface is minimal: maintainers inspect PR gates, manually select a candidate SHA and version for readiness, and review its report. Missing evidence, denied access, expired artifacts, cancelled runs, and version/digest mismatches must be visible and must not look eligible. A successful report still requires a separate human release decision. Existing GitHub and CLI surfaces suffice; no new visual experience artifact is needed.

## Non-goals

- Rewriting the internal `devquitect_quality` Python tooling merely to remove PyYAML from consumers.
- Changing `verify_slice.py`, its runtime dependencies, its YAML inventory, or its acceptance semantics.
- Turning QUICK into a catch-all path for architectural work.
- Authorizing code or packaging changes through this definition.
- Automatic deployment, publishing, tagging, installation, or promotion approval.
- Behavioral runs on every PR, model-backed required checks, a new CI provider, new skills, or a generic release-management platform.
