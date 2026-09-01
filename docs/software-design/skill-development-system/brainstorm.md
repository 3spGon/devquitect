# Devquitect Skill Development System — decision trail

## 2026-08-30 — Initial problem framing

The repository was assessed as a collection of three declarative skills without independent behavioral tests or the surrounding engineering practices needed to change them confidently. The initial quality concerns were routing regressions, accidental authority expansion, invalid persistent-state transitions, and changes whose effects could not be established from repository evidence.

## 2026-08-30 — Development-system direction

The proposed change was broadened from adding tests alone to establishing a complete, proportional skill development system. The direction includes authoring conventions, static validation, isolated behavioral evaluation, reproducible packaging, quality evidence, CI integration, semantic versioning, and controlled releases.

The three related skills are proposed to remain independently authored while being distributed together as the `devquitect` plugin. Public marketplace publication, MCP integrations, and a graphical interface remain outside the initial scope.

## 2026-08-30 — Controlled self-hosting

Using `software-idea-to-project` to define improvements to itself was accepted as useful dogfooding, subject to a non-circular trust model:

- stable version N may help define candidate N+1;
- candidate N+1 cannot be its own sole evaluator or approver;
- author and candidate versions must be isolated and identified in evidence;
- deterministic checks, independent behavioral graders, and human approval remain required;
- only a verified candidate may be promoted and then help produce the next version.

Repository inspection established that the currently discovered local skill resolves to the same working-tree directory. This is useful during authoring but unsafe as the eventual evaluation boundary, so the proposed development system must execute immutable skill snapshots in isolated workspaces.

## 2026-08-30 — Persistent mode

The user explicitly moved the definition from chat-only to persistent mode. The prior design and self-hosting refinement were crystallized into `01-concept.md` and `02-requirements.md`, both in Review, with Gate 1 pending.

## 2026-08-30 — Gate 1 approved

The user explicitly approved the concept and requirements. Both canonical documents moved to Approved, Gate 1 was recorded as approved, and the workflow advanced to technical design.

## 2026-08-30 — Technical architecture defined

The technical design preserves controlled self-hosting through immutable, content-addressed stable and candidate snapshots. A Python quality runner uses fresh fixtures and ephemeral Codex executions, separates deterministic assertions from independent semantic grading, and records source/runtime provenance in versioned evidence.

The same provider-neutral command surface covers structural validation, behavioral evaluation, stable-candidate comparison, reproducible plugin packaging, and release eligibility. Infrastructure errors remain inconclusive, critical deterministic failures cannot be scored away, and promotion still requires a clean commit plus explicit human approval.

## 2026-08-30 — Gate 2 approved

The user explicitly approved the technical architecture after clarifying the bootstrap rule: Gate 2 may be approved before an immutable baseline exists, but no file under `skills/` may be changed for N+1 until stable N has been frozen, identified, and verified outside the candidate working tree. The workflow advanced to implementation planning with baseline creation as the first delivery slice.

## 2026-08-30 — Implementation plan ready for approval

The approved architecture was translated into seven ordered, independently verifiable delivery slices. `SLICE-001` freezes stable N from commit `264f4648ae1e699168347eb8e5945459bfbd0e27` and is a hard prerequisite; later slices add structural validation, isolated execution, critical behavioral contracts, stable-candidate comparison, reproducible release checks, and the integrated contributor workflow. Every approved requirement and acceptance scenario maps to a slice and verification method. The plan does not modify the three skills and does not authorize implementation.

## 2026-08-30 — Implementation plan approved

The user explicitly approved implementation plan revision 1. The software-definition workflow is complete with both gates and all canonical artifacts approved. No implementation slice was authorized by this approval; delivery requires a separate request naming the concrete `SLICE-*` scope and must begin with `SLICE-001`.
