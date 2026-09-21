# Evaluation Authentication Governance brainstorm

This file is the chronological, non-canonical decision trail for the initiative.

## 2026-09-21 — Seed and baseline

- The user asked to turn the review of temporary ChatGPT login-cache handling into a new persistent initiative.
- The initiative is a `system-change` to the existing Devquitect evaluation toolchain, not a new product.
- Current behavior automatically discovers `~/.codex/auth.json` for trusted behavioral commands, copies it into an isolated `CODEX_HOME`, uses it for the subprocess, and removes the copied file in `finally` when the parent process continues normally.
- Credential-free structural checks remain separate and do not require model authentication.

## 2026-09-21 — Risk and policy research

- The cleanup design handles ordinary completion, timeout, and child-process failure, but cannot guarantee cleanup after `SIGKILL`, an unhandled terminating signal, OOM, or a crash of the parent runner.
- The current staging sequence copies the cache before applying `0600`, and the staging call occurs before the cleanup `try/finally`; both need explicit treatment in technical design.
- No dedicated tests currently prove auth-cache permissions, partial-staging cleanup, stale-cache recovery, or abrupt termination behavior.
- OpenAI's Codex guidance says ChatGPT-authenticated Codex usage is governed by the applicable ChatGPT terms or business/API agreement and consumes the associated usage allowance. The individual Terms of Use prohibit automatic or programmatic extraction of data or Output and bypassing rate limits or restrictions. This creates a policy gate for automated evaluation loops, not merely an implementation detail.

## 2026-09-21 — Initial direction

- Recommended direction: make authentication explicit and policy-governed; do not autodiscover a personal ChatGPT login cache for automated evaluation.
- Keep the structural check credential-free and default behavioral tooling to a non-subscription authentication path suitable for the approved environment.
- If local ChatGPT-cache execution remains supported, make it an explicit local-only mode with warnings, bounded lifetime, best-effort stale cleanup, and no claim of SIGKILL-proof deletion.
- The profile is confirmed as bounded impact but full workflow depth because it is trust-sensitive and has external policy and recovery consequences.

## 2026-09-21 — Gate 1 proposal

- `01-concept.md` and `02-requirements.md` are in `Review`.
- Gate 1 is pending explicit user approval. Detailed architecture and implementation planning remain deferred.

## 2026-09-21 — Gate 1 approval and technical design

- The user explicitly approved Gate 1.
- `01-concept.md` and `02-requirements.md` moved to `Approved`.
- Technical design now proposes explicit auth modes, no implicit login-cache discovery, and a
  best-effort stale-attempt cleanup mechanism. The external account/plan policy owner remains the
  only implementation-blocking decision before Gate 2.

## 2026-09-21 — Gate 2 approval and implementation planning

- The user confirmed the recommended boundary: no unattended use of ChatGPT subscription
  authentication; local cache use is explicit, local, and supervised only.
- `DEC-EAG-004` is resolved and the domain, architecture, contract, and decision artifacts are
  approved.
- The implementation plan is now in `Review`. Its approval would still not authorize implementation;
  execution requires a separate concrete slice authorization through `project-plan-execution`.

## 2026-09-21 — Plan approval

- The user approved implementation plan revision 1 only.
- The definition workflow is complete. No implementation slice is authorized, and no behavioral
  evaluation using a ChatGPT subscription was run.
