# Devquitect Skill Development System decisions

Status: Approved
Last updated: 2026-08-30

## Confirmed

- These decisions refine the approved concept and requirements without authorizing implementation.
- Reversals that materially alter trust, authorization, persistence, or release behavior require renewed architecture review.

## Assumptions

- Tool-specific details may evolve behind the documented contracts when evidence and compatibility remain intact.

## Open decisions

- Baseline measurement will determine model matrices, repetitions, and semantic thresholds.
- CI provider selection is deferred.

## ADR-001 — Controlled self-hosting, not circular self-validation

**Decision:** Stable N may help author candidate N+1. Both are frozen as different snapshots. Candidate N+1 is never its sole grader, policy engine, approver, or release authority.

**Why:** Dogfooding exercises the real workflow and improves the skill, while immutable separation and independent evidence prevent a candidate from redefining its own success criteria during evaluation.

**Rejected:** Avoid all self-use. This loses a valuable representative scenario. Use the live working tree as both author and candidate. This makes provenance and isolation unverifiable.

## ADR-002 — Behavioral contracts assert observations, not exact prose

**Decision:** Cases primarily assert commands, tools, file/Git effects, persistent transitions, forbidden actions, structured output, and meaning-level rubric results.

**Why:** Natural-language responses vary while authorization and state-integrity requirements do not. Exact strings remain valid only for formal serialized contracts.

**Rejected:** Golden full-response snapshots. They are brittle and reward wording stability over behavioral correctness.

## ADR-003 — Deterministic invariants dominate semantic grading

**Decision:** Critical mutation, authorization, schema, and state assertions are deterministic and non-overridable. Semantic graders address only irreducibly qualitative criteria.

**Why:** A persuasive answer cannot make an unauthorized write safe or turn missing execution evidence into verification.

**Rejected:** One aggregate model score. It obscures hard failures and allows the evaluated behavior to influence its own acceptance.

## ADR-004 — Python orchestrator with a pinned Codex CLI adapter

**Decision:** Implement repository tooling in Python 3.12 and initially execute behavioral cases through the documented JSONL interface of `codex exec --ephemeral --json`.

**Why:** Python is locally available and suitable for portable validation, subprocess orchestration, schemas, temporary Git fixtures, and tests. The CLI explicitly exposes event evidence and isolation controls required by this design.

**Rejected:** Shell-only orchestration, which becomes fragile for schemas and evidence. Direct Python SDK as the first adapter, because the CLI's event and flag contract currently maps more explicitly to the required observations. The SDK remains a replaceable future adapter.

## ADR-005 — Immutable content-addressed snapshots

**Decision:** Every evaluation freezes source contents before running and assigns a manifest digest. Stable release evidence requires a clean Git commit; working-tree snapshots are diagnostic candidate inputs only.

**Why:** In-progress edits must not alter stable authorship, repeat attempts, or the source associated with a verdict.

**Rejected:** Executing directly from repository paths or symlinked installed skills.

## ADR-006 — Fresh isolation per case and attempt

**Decision:** Each attempt gets a new conversation, temporary workspace, installed-skill root, configuration boundary, and evidence namespace.

**Why:** This makes cases independent and prevents history, files, rules, or previously active skills from contaminating routing and effects.

**Rejected:** Reusing a conversation or fixture directory for speed. Performance optimization cannot precede valid independence.

## ADR-007 — YAML cases, JSON Schema validation, JSON evidence

**Decision:** Humans author YAML cases; JSON Schemas define their contracts; canonical reports and promotion records are JSON with explicit schema versions.

**Why:** YAML is reviewable for scenarios, while JSON Schemas and canonical JSON give deterministic validation and automation.

**Rejected:** Markdown-only cases, which are hard to validate, and Python-only case definitions, which mix test intent with execution code.

## ADR-008 — Separate fast checks from credentialed behavioral evals

**Decision:** Structural validation and development-system tests are deterministic, offline, and credential-free. Real behavioral evals are an explicit suite requiring model access.

**Why:** Contributors need fast feedback, and trusted credentials must not be required or exposed for ordinary structural changes.

**Rejected:** Running model evals as an implicit prerequisite for every local command.

## ADR-009 — Infrastructure errors are inconclusive

**Decision:** Authentication, service, adapter, and missing-event failures use a distinct inconclusive status and exit code. Fixed repetitions measure variability; no retry-until-pass behavior is allowed.

**Why:** Availability failure proves neither behavioral success nor regression. Broad retries would bias evidence toward passing samples.

**Rejected:** Counting infrastructure failure as pass, fail, or silently retrying until a favorable answer appears.

## ADR-010 — Reproducible plugin package from a verified commit

**Decision:** Package the three skills as the `devquitect` plugin from an exact clean commit, with a required `.codex-plugin/plugin.json`, allowlisted inputs, normalized archive metadata, and a second-build digest comparison.

**Why:** Review and evaluation evidence must identify the same contents users install.

**Rejected:** Publishing from a dirty working tree or maintaining manually assembled archives such as `skills.zip` as release truth.

## ADR-011 — Provider-neutral core and thin CI adapters

**Decision:** Local commands and report schemas own all quality policy. A future CI workflow only selects commands, credentials, and artifact retention.

**Why:** The project has no remote or selected CI provider, and quality behavior should not diverge between local and hosted runs.

**Rejected:** Encoding assertions or promotion rules directly in one provider's workflow format.

## ADR-012 — Promotion is human-authorized and rollback is immutable

**Decision:** The system computes release eligibility and proposes a promotion record; a maintainer supplies explicit approval. Rollback selects a prior immutable package rather than rewriting history.

**Why:** Automated evidence supports but does not replace ownership of behavioral and compatibility decisions.

**Rejected:** Automatic promotion on aggregate score or altering an existing tag/package after release.
