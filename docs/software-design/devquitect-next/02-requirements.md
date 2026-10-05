# Devquitect Next requirements

Status: Approved
Last updated: 2026-10-03

## Confirmed

### R-01: Preserve authority boundaries

The three existing skills remain distinct: definition does not implement, plan execution does not invent architecture, and targeted refactoring does not disguise behavior changes as refactors.

### R-02: Lean entrypoints with cross-generation evidence

The 0.7.0 skill entrypoints state each policy once and preserve only outcome, constraints, authorization, readiness, escalation, and completion behavior that the agent needs at entry. Detailed state and artifact mechanics remain in their designated owners. Every material simplification is evaluated against the same representative cases before it is retained. GPT-5.6 remains a reproducible prior-generation baseline; the operating model is not tuned exclusively to that generation.

### R-03: QUICK route

0.7.0 adds an independently invocable skill that may activate implicitly when its precise description matches an authorized change that is localized, reversible, has no public-contract or material behavior decision, and has a direct verification path. It performs focused discovery, modifies only in-scope files, runs relevant validation, and reports the result concisely.

### R-04: QUICK escalation

QUICK must stop and route to the appropriate established workflow when evidence finds a feature decision, architecture decision, public contract, persistence or migration change, security-sensitive behavior, multi-module impact, or a need for durable continuity.

### R-05: Preserve delivered verification

The initiative does not modify `verify_slice.py`, its Python/PyYAML requirements, its YAML inventory, or the existing snapshot/check/close acceptance contract.

### R-06: Compatibility and stabilization

1.0.0 is eligible only after the new routes, escalation behavior, and retained verification boundaries have deterministic positive and negative coverage plus approved behavioral comparison evidence where authorized.

### R-07: Staged prompt-change protocol

Each material prompt simplification starts from an immutable baseline, changes one named rule group in one skill, reruns the same deterministic cases, and records a retain, move, or remove disposition. A behavioral comparison, when authorized, uses a declared model/host configuration and the same case set. Regression or inconclusive evidence retains the prior text.

### R-08: Prompt-change ledger

The repository maintains a versioned prompt-change ledger. Each entry identifies the immutable baseline and candidate snapshots, affected paths and rule groups, disposition, deterministic cases, model/host configuration when applicable, report references, and verdict. Source text is reconstructed from the referenced snapshots rather than duplicated in the ledger.

### R-09: Generalized workflow and persistence configuration

Workflow depth applies to every initiative according to impact and risk. Persistent definition work resolves a configured root when supplied and otherwise uses a detected repository default; existing sessions remain discoverable at their current paths.

### R-10: Invocation and evaluation policy

The invocation policy explicitly controls implicit activation for each skill. The initial evaluation matrix includes GPT-5.6 Sol, Terra, and Luna as baseline rows and GPT-6 Sol (`gpt-6-sol`) and GPT-6 Luna (`gpt-6-luna`) as separate new-generation rows. Each row declares model, host, runtime, reasoning effort where supported, suite revision, repetitions, and reports; results from different configurations are not pooled. Behavioral comparisons remain separately authorized.

## Approved DN-005 / DN-006 requirements

The user approved the following amendment at Gate 1 on 2026-10-03. It preserves R-01 through R-10 and adds CI and exact-candidate evidence requirements; it does not make planned behavior part of the implemented baseline or authorize implementation.

### R-11: Independent continuous verification

DN-005 shall run the credential-free definition of done from a clean GitHub runner on the checked-out commit using Python 3.12 and the locked `uv` environment. Validation, tests, Ruff, and introduced whitespace errors shall block technical eligibility. Installed quality tooling, checkout, and selected source shall identify the same candidate. Local working-tree checks remain the development default; CI shall use the exact checked-out Git source, not `working-tree`.

PR CI shall record tested integration SHA, PR head SHA, and base SHA. CI shall also run after integration to `main`; release evidence shall match the final candidate SHA exactly, with no implicit substitution of PR, merge, squash, or rebase identities. Every required platform job must succeed. Failed, missing, cancelled, or skipped mandatory jobs cannot count as completed verification. Runner or network failure prevents eligibility without being mislabeled as a product regression.

The normal workflow shall need no model, ChatGPT login, API key, publication token, or write permission. GitHub's read-only job token and dependency network access are infrastructure dependencies, not model credentials. Maintainers shall activate stable required checks on `main`, prohibit force pushes and deletion, and use PR integration. Documented but unapplied protection is an incomplete merge gate.

### R-12: Platform compatibility and reproducible package

DN-005 shall smoke-test compaction recovery, relevant CLI contracts, path-sensitive packaging, and applicable Windows behavior on Linux, macOS, and Windows, initially with Python 3.12 only. The canonical package shall be built twice from the same exact commit, version, and locked toolchain in separate clean output roots. Matching package SHA-256 and entry manifests are required; cross-OS byte equivalence is not claimed by this initial gate.

The package ZIP, deterministic manifest, check report, execution metadata, and digests are CI evidence, not a public release. Failed-run reports shall remain available for diagnosis while never qualifying as successful candidate evidence.

### R-13: Candidate identity and evidence provenance

DN-006 shall accept an explicit full candidate SHA and version and select one successful CI run attempt for that candidate in the expected repository and workflow. It shall verify provenance against GitHub run/job/artifact metadata, not trust self-declared JSON identities or artifact names alone. Quality, every required platform variant, and package evidence shall all belong to that candidate and selected attempt.

The release input, committed plugin manifest, package contents, and deterministic package manifest shall agree on version and identity. The downloaded ZIP and manifest shall match recorded file digests, and the ZIP shall match the reproducible package evaluated by `release-check`. Absent, incomplete, tampered, expired, cancelled, or unrelated evidence shall prevent eligibility; reruns shall be selected explicitly and never mixed with stale evidence from another attempt.

### R-14: Release readiness without publication authority

DN-006 shall run explicitly and produce structured eligibility and an unapproved promotion proposal containing candidate identity, version, source snapshot, workflow/run/attempt/artifact references, file digests, release-check result, and timestamp. `approved_by` and `approved_at` remain null. No workflow shall tag, push, publish, deploy, change `main`, or approve its own proposal.

Compatibility shall be evaluated against an explicitly selected immutable previous-release reference, with its version recorded, so commits after a version bump can remain eligible. Existing callers that omit that new option retain the current parent-based behavior; selecting a baseline does not weaken exact-candidate or version checks. Missing baseline or a non-increasing release version shall prevent eligibility.

Authorized behavioral evidence shall retain its own model ID, host/runtime, reasoning effort, suite revision, repetitions, report references, source snapshot, authorization, and `pass`, `fail`, `inconclusive`, or `not-run` verdict. No behavioral result substitutes for a deterministic gate; model infrastructure failure is inconclusive and is not a normal PR blocker. DN-004 remains the matrix authority. Readiness shall preserve those rows as supplementary evidence, without calling a model.

## Assumptions

- Existing GitHub and CLI surfaces cover the minimal maintainer interaction; observable input, failure, and eligibility states are specified here without a separate visual artifact.
- GitHub-hosted runners and artifact access are available for the target repository; implementation must verify effective permissions and branch protection rather than assume them from configuration files.

## Open decisions

- None at the behavior-definition level. R-11 through R-14 have Gate 1 approval and their technical treatment has Gate 2 approval; plan approval remains separate. The initial ledger and model matrix retain their previously approved R-08 / R-10 scope.
