# Skill Change Ledger

This versioned ledger records each named prompt rule group. Baselines use immutable Git references. Candidate snapshot IDs are SHA-256 hashes of the listed worktree files; the source text is reconstructed from those paths and checked against its hash. Append new records without rewriting prior entries.

## PC-DN-001-DEF — Definition workflow and authority boundary

- **Baseline:** `git:7f7030813b7995a9a93cbf4a43cbafb9c8dddeb5` — `skills/software-idea-to-project/SKILL.md`
- **Candidate:** `worktree-sha256:6912f485c5f900737b340d5c57a88f77b3021740c0419dcec62467082897ce27` — `skills/software-idea-to-project/SKILL.md`
- **Scope:** Lean definition entrypoint; explicit gates and implementation handoff remain intact.
- **Disposition:** move
- **Deterministic cases:** `software-idea-positive`, `software-idea-negative`, `gate-one-bypass` (unchanged representative cases)
- **Behavioral configuration:** Not run; comparison requires separate authorization.
- **Evidence:** Credential-free check and command results are recorded in [SLICE-DN-001 evidence](software-design/devquitect-next/slices/SLICE-DN-001.md).
- **Verdict:** inconclusive
- **Rationale:** Detailed discovery, session-state, and planning mechanics remain in their referenced owners. No behavior comparison was authorized.

## PC-DN-001-DEL — Delivery authorization and verified close

- **Baseline:** `git:7f7030813b7995a9a93cbf4a43cbafb9c8dddeb5` — `skills/project-plan-execution/SKILL.md`, `skills/project-plan-execution/references/execution.md`
- **Candidate:** `worktree-sha256:d9a87dd0cec6e7f7e8f1d08615890fc64eeb14fff502389728ea29deb237fdca` — `skills/project-plan-execution/SKILL.md`; `worktree-sha256:607ea8e3828fb782b057da6118af1a974bb4acbc895f377ca9f4fbd937d93ae4` — `skills/project-plan-execution/references/execution.md`
- **Scope:** Lean entrypoint; authorized handoff preflight, durable delivery state, slice execution, and evidence close have canonical owners.
- **Disposition:** move
- **Deterministic cases:** `plan-execution-positive`, `plan-execution-negative`, `delivery-authorization-matching-positive`, `delivery-authorization-conflict-negative` (unchanged representative cases)
- **Behavioral configuration:** Not run; comparison requires separate authorization.
- **Evidence:** Credential-free check and command results are recorded in [SLICE-DN-001 evidence](software-design/devquitect-next/slices/SLICE-DN-001.md).
- **Verdict:** inconclusive
- **Rationale:** Authorization boundaries remain in the entrypoint and detailed execution mechanics remain in their owners. No behavior comparison was authorized.

## PC-DN-001-REF — Behavior-preserving refactor workflow

- **Baseline:** `git:7f7030813b7995a9a93cbf4a43cbafb9c8dddeb5` — `skills/targeted-refactoring/SKILL.md`
- **Candidate:** `worktree-sha256:30738c7bae7b76579e66103586dcaed1b55a54ee79282cbedbb70018230397cf` — `skills/targeted-refactoring/SKILL.md`; `worktree-sha256:fb34f0c8fbfd5f79a3ce017c3e4df3c8cbab81b4bd8eb91eea9db11163947cf5` — `skills/targeted-refactoring/references/workflow.md`
- **Scope:** Lean refactoring entrypoint and its detailed workflow owner.
- **Disposition:** move
- **Deterministic cases:** `refactoring-positive`, `refactoring-negative` (unchanged representative cases)
- **Behavioral configuration:** Not run; comparison requires separate authorization.
- **Evidence:** Credential-free check and command results are recorded in [SLICE-DN-001 evidence](software-design/devquitect-next/slices/SLICE-DN-001.md).
- **Verdict:** inconclusive
- **Rationale:** Review, authorization, behavior-preservation, and verification mechanics remain in the new workflow reference. No behavior comparison was authorized.

## BC-DN-001-001 — SLICE-DN-001 authorized behavioral comparison

- **Authorization:** Explicit user authorization received 2026-09-24.
- **Stable:** `git:7f7030813b7995a9a93cbf4a43cbafb9c8dddeb5`, snapshot `sha256:d3ae013072604f67f6f72e85c709334367134e33bdffa98e28adc6927507e359`.
- **Candidate:** `working-tree`, snapshot `sha256:1174fe6026afbcc4ca05821371a365e15962133f81e1bc513ef45d1cd1ac0073` (diagnostic-only).
- **Configuration:** `gpt-5.6-luna`, reasoning effort `high`, Codex CLI 0.154.0, devquitect-quality 0.1.0, one repetition per case. Supervised `chatgpt-cache-local` authentication was allowed and cleaned in every report.
- **Case results:** `software-idea-positive`, `software-idea-negative`, `gate-one-bypass`, `plan-execution-positive`, `plan-execution-negative`, `delivery-authorization-matching-positive`, `delivery-authorization-conflict-negative`, `refactoring-positive`, and `refactoring-negative` all returned `pass` and `equivalent`, with zero critical assertion failures.
- **Evidence:** Per-case reports are `.devquitect-reports/slice-dn-001-<case-id>.json`; the structured summary is recorded in [SLICE-DN-001 evidence](software-design/devquitect-next/slices/SLICE-DN-001.md).
- **Runtime notes:** The stable `software-idea-positive` run logged a unified exec process creation error, and the stable `plan-execution-positive` run logged a model-list refresh timeout. Both records still classified as `pass`, and both paired comparisons returned `equivalent`; the messages remain in their reports.
- **Verdict:** equivalent for the tested cases; diagnostic-only because the candidate was a working tree.
- **Rationale:** The same baseline, candidate, model, reasoning effort, and nine representative positive/negative cases were used for both sides. This follow-up supplements, and does not rewrite, the original pre-authorization PC-DN-001 records.
