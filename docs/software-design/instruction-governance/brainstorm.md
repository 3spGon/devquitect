# Instruction Governance brainstorm

This file is the chronological, non-canonical decision trail for the initiative.

## 2026-09-09 — Seed and baseline

- The user chose to restart from the clean `v0.3.0` baseline rather than extend the
  multi-initiative lifecycle experiment.
- The problem is governance of instruction complexity: rules have accumulated across skill
  entrypoints, references, rubrics, cases, and contributor guidance.
- The intended outcome is a smaller, coherent authority model. Safety invariants such as scoped
  mutation, explicit authorization, durable-state integrity, and ownership remain strict.
- Conversational phrasing, judge variation, and infrastructure failures must be distinguished
  from material behavior regressions before they influence promotion decisions.
- No implementation behavior, approval gate, evaluation result, commit, or promotion is carried
  from the prior experimental branch into this initiative.

## 2026-09-10 — Evaluation and promotion boundary

- The user identified the central governance risk: treating every repeated model diagnostic as a
  mandatory pass (for example, 15/15) would recreate the prior cycle of modifying skill
  instructions to chase model variance rather than improve the product contract.
- Deterministic safety invariants remain strict and promotion-blocking: scoped mutation, explicit
  authorization, durable-state integrity, and ownership boundaries.
- Semantic model behavior is diagnostic evidence governed by predeclared, scenario-specific
  thresholds; it is not subject to a universal all-repetitions-pass rule.
- Judge, CLI, and environment failures are inconclusive evidence, distinct from an agent behavior
  regression. They must be investigated without being counted as functional failure.
- Promotion should run the complete credential-free suite and model-backed evaluation relevant to
  the changed behavior. A complete model sweep may be a separately governed periodic or major
  release activity, rather than an automatic condition of every promotion.

## 2026-09-09 — Authority map and policy proposal

- Mapped the current owners: `SKILL.md` owns entrypoint behavior; named references own detailed
  workflow contracts; cases plus assertion code own observable invariants; rubrics own semantic
  dimensions; grading owns deterministic/inconclusive precedence; comparison owns paired-result
  classification; promotion owns release-evidence eligibility; schemas own record shape; and
  contributor guidance explains rather than redefines those contracts.
- Confirmed that every current versioned case has `repetitions: 1`. There is no repository rule
  requiring 15/15 semantic passes.
- Confirmed that semantic grades currently do not affect `grade_observation` or promotion
  eligibility. The initiative therefore needs an explicit per-scenario threshold/promotion-effect
  contract rather than another global instruction rule.
- Drafted a policy that makes deterministic safety failures blocking, keeps infrastructure
  failures inconclusive, scopes semantic diagnostics to changed behavior, and reserves broad
  model sweeps for separately governed calibration or major-release work.

## 2026-09-09 — Clarified intended mechanisms

- The user confirmed this initiative must deliver two mechanisms, not merely an authority map:
  repository validation must reject normative rules added outside their designated owner, and
  promotion policy must avoid a universal 100% semantic-success requirement.
- The proposed validator will use an explicit ownership registry and allow secondary documents
  to link, explain, test, schema-encode, or present an owned rule without redefining it. It will
  not attempt to judge arbitrary prose equivalence.

## 2026-09-09 — Scope reduced to critical contracts

- The user chose the lightweight approach: preserve concise installed skills; validate only the
  small set of cross-file critical contracts; and rely on external deterministic tests for their
  observable behavior.
- Rejected a per-rule registry, mandatory metadata on every instruction, and a prose linter. They
  would burden routine authoring and cannot reliably prove semantic contradiction.
- Confirmed from package code that only `.codex-plugin/plugin.json` and `skills/**` ship in a
  plugin. Tests, fixtures, source tooling, and the authority map can enforce repository quality
  without adding agent-reading load.

## 2026-09-09 — Promotion-evaluation assessment

- The supplied example shows an agent reporting a partial implementation honestly after failing
  to complete the requested delivery. That is a failed delivery outcome, but it does not prove a
  skill regression or a model defect; the later explanation is not evidence that the model could
  have completed the earlier turn.
- Current evaluation records observable effects, not private interpretation. Its semantic rubric
  and `forbidden_effects` case fields are not consumed by the evaluation/promotion path; all
  current cases use one repetition; and comparison retains only one record per case ID when
  repetitions exist. Repeated semantic thresholds are therefore not yet implemented evidence.
- Recommended that promotion retain structural and enforceable-safety gates, while model
  end-to-end behavior is measured differentially against the same stable model/runtime for only
  changed cases. Equal baseline limitations and ordinary variance should be diagnostic, not a
  prompt-edit treadmill. Safety requiring certainty belongs in deterministic guardrails.

## 2026-09-09 — Repository guidance

- The user requested that repository guidance make the initiative's operating intent explicit:
  Devquitect skills and their quality tooling evolve as product contracts, not incidental prose;
  concise entrypoints, external deterministic tests, and baseline comparison guide that work.

## 2026-09-10 — Model runs removed from promotion eligibility

- The user confirmed that lightweight models can hallucinate, stop, or behave oddly for reasons
  unrelated to skill instructions. Model-backed runs must therefore not be required per feature
  or block a promotion.
- Model scenarios remain optional diagnostic calibration. Promotion relies on complete
  credential-free deterministic evidence, immutable identities, and maintainer approval.
- This resolves DEC-IG-01 and DEC-IG-02: no semantic promotion thresholds are needed.

## 2026-09-10 — Correction

- The assistant prematurely treated the user's concern about unreliable lightweight models as
  authorization to adopt a new promotion policy and request Gate 1 approval. That was not an
  approved decision.
- The policy and checkpoint were restored to the prior draft state. DEC-IG-01 and DEC-IG-02
  remain open; the preceding rejected direction remains historical context only.
