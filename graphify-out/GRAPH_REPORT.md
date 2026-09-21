# Graph Report - devquitect-instruction-governance  (2026-09-21)

## Corpus Check
- 174 files · ~106,986 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1711 nodes · 2754 edges · 162 communities (130 shown, 27 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 117 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `882a0f8b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- freeze_source
- reporting.py
- build_package
- properties
- properties
- app_server_adapter.py
- SLICE-001.md
- schemas/authority-map.schema.json
- valid-plugin/schemas/authority-map.schema.json
- Evaluation Authentication Governance
- type
- slice-verification/README.md
- Evaluation Authentication Governance implementation plan
- properties
- compatibility
- observations.py
- Compaction Recovery decisions
- properties
- type
- Devquitect Skill Development System architecture
- schemas/eval-case.schema.json
- items
- schemas/promotion-record.schema.json
- Evaluation Authentication Governance architecture
- Compaction Recovery concept
- valid-plugin/schemas/calibration-report.schema.json
- valid-plugin/schemas/eval-case.schema.json
- valid-plugin/schemas/promotion-record.schema.json
- valid-plugin/schemas/report.schema.json
- What You Must Do When Invoked
- fixture
- id
- scenario
- tags
- target_skill
- approved_at
- package_digest
- run_ids
- snapshot_id
- version
- devquitect-quality
- verify_slice.py
- Devquitect Skill Development System implementation plan
- Devquitect Skill Development System contracts
- Devquitect Skill Development System data model
- Devquitect Skill Development System decisions
- Handoff notes
- Diseño técnico — Verificación de slices
- Requisitos y escenarios de aceptación
- Proportional Change Profile decisions
- Proportional Change Profile implementation plan
- Devquitect Skill Development System concept
- Confirmed
- Instruction Governance brainstorm
- Proportional Change Profile concept
- Devquitect Skill Development System requirements
- Devquitect Skill Development System — decision trail
- Instruction Governance Implementation Plan
- Proportional Change Profile architecture
- Plan de implementación — Slice verification
- Durable Session State
- test_slice_verification.py
- graphify reference: extra exports and benchmark
- Confirmed
- project-plan-execution/SKILL.md
- Verificación de entregas por slice
- Proportional Change Profile
- Proportional Change Profile data model
- Historial — Slice verification
- Persistent Artifacts
- Discovery and Crystallization
- Repository instructions
- Proportional Change Profile requirements
- Delivery checkpoint
- Proportional Change Profile brainstorm
- System Context and Baseline
- Technical Design
- Software Idea to Project
- graphify reference: query, path, explain
- Confirmed
- Delivery checkpoint
- Contributing skills
- Delivery checkpoint
- Durable Delivery State
- Authorized Slice Execution
- Experience Design
- Current checkpoint
- Instruction Governance Requirements
- Current checkpoint
- Compaction Recovery architecture
- Current checkpoint
- slice-verification/01-concept.md
- codex_adapter.py
- Adaptive Implementation Planning
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- Instruction Governance Interfaces
- Instruction Governance Decisions
- guide.md
- graphify reference: GitHub clone and cross-repo merge
- graphify reference: transcribe video and audio
- extraction-spec.md
- basic/README.md
- runtime-workspace/README.md
- Functional requirements
- Compaction Recovery brainstorm
- Devquitect system context
- SLICE-002.md
- test_fake_codex_run.py
- fixtures/slice-verification/00-status.md
- fixtures/slice-verification/08-implementation-plan.md
- fixtures/slice-verification/09-delivery-status.md
- fixtures/slice-verification/slices/SLICE-001.md
- Compaction Recovery interface contracts
- Plan de implementación — Compaction Recovery
- Evaluation Authentication Governance domain
- compaction-recovery/08-implementation-plan.md
- Evaluation Authentication Governance brainstorm
- Evaluation Authentication Governance contracts
- Compaction Recovery requirements
- Compaction Recovery data model
- Functional requirements
- Delivery checkpoint
- evaluation.py
- Q: How does Devquitect recover delivery execution after Codex context compaction?
- compaction_recovery.py
- Evaluation Authentication Governance decisions
- test_compaction_recovery_hook.py
- Commands
- validate.py
- Compaction recovery contract
- Delivery checkpoint
- compaction-recovery/slices/SLICE-002.md
- fixtures/compaction-recovery/00-status.md
- fixtures/compaction-recovery/08-implementation-plan.md
- pending-d.md
- repository-disagreement.md
- stale-conversation.md
- compaction-recovery/README.md
- Evaluation Authentication Governance requirements
- SLICE-003.md
- valid-plugin/hooks/compaction_recovery.py
- software-design/system-context.md
- _run_calibrate
- SLICE-004.md
- Proposed architecture
- cli.py
- Current checkpoint
- parse_jsonl_events
- test_validate.py
- resolve_auth
- Delivery checkpoint
- test_auth_lifecycle.py
- Proposed architecture
- SLICE-EAG-001.md
- SLICE-EAG-002.md

## God Nodes (most connected - your core abstractions)
1. `freeze_source()` - 37 edges
2. `build_package()` - 30 edges
3. `SkillSource` - 29 edges
4. `SourceError` - 28 edges
5. `release_check()` - 27 edges
6. `_run_calibrate()` - 24 edges
7. `run_app_server()` - 22 edges
8. `load_validation_inputs()` - 22 edges
9. `_run_eval()` - 21 edges
10. `_run_compare()` - 21 edges

## Surprising Connections (you probably didn't know these)
- `_run()` --uses--> `SkillSource`  [INFERRED]
  tests/integration/test_app_server_adapter.py → src/devquitect_quality/models.py
- `test_app_server_cleans_staged_auth_after_protocol_failure()` --uses--> `SkillSource`  [INFERRED]
  tests/integration/test_app_server_adapter.py → src/devquitect_quality/models.py
- `test_plugin_setup_failure_is_redacted()` --uses--> `SkillSource`  [INFERRED]
  tests/integration/test_app_server_adapter.py → src/devquitect_quality/models.py
- `test_pair_freezes_both_sources_before_candidate_edits_and_uses_distinct_roots()` --uses--> `SkillSource`  [INFERRED]
  tests/integration/test_compare_command.py → src/devquitect_quality/models.py
- `test_run_case_routes_turns_and_scenarios_to_their_separate_runners()` --uses--> `SkillSource`  [INFERRED]
  tests/integration/test_eval_command.py → src/devquitect_quality/models.py

## Import Cycles
- None detected.

## Communities (162 total, 27 thin omitted)

### Community 0 - "freeze_source"
Cohesion: 0.05
Nodes (80): ComparisonClass, skipif, classify_results(), freeze_pair(), FrozenPair, pair_records(), Any, Path (+72 more)

### Community 1 - "reporting.py"
Cohesion: 0.10
Nodes (32): _emit(), main(), Run the repository-owned command surface., _run_check(), _run_package(), _run_release_check(), build_artifact_report(), build_calibration_report() (+24 more)

### Community 2 - "build_package"
Cohesion: 0.08
Nodes (60): build_package(), _git(), _normalize_manifest(), PackageArtifact, PackageEntry, PackageError, Path, PurePosixPath (+52 more)

### Community 3 - "properties"
Cohesion: 0.04
Nodes (45): additionalProperties, type, maxItems, type, format, type, $id, minLength (+37 more)

### Community 4 - "properties"
Cohesion: 0.04
Nodes (44): additionalProperties, minLength, type, type, format, type, $id, type (+36 more)

### Community 5 - "app_server_adapter.py"
Cohesion: 0.19
Nodes (25): Popen, AppServerError, _command_environment(), _drive(), compact(), record(), request(), wait_for_turn() (+17 more)

### Community 7 - "schemas/authority-map.schema.json"
Cohesion: 0.09
Nodes (26): additionalProperties, items, type, $id, minLength, type, additionalProperties, properties (+18 more)

### Community 8 - "valid-plugin/schemas/authority-map.schema.json"
Cohesion: 0.09
Nodes (24): additionalProperties, items, type, minLength, type, additionalProperties, properties, required (+16 more)

### Community 9 - "Evaluation Authentication Governance"
Cohesion: 0.15
Nodes (13): Actors and external systems, Assumptions, Change Profile, Conceptual direction, Confirmed, Desired outcome, Evaluation Authentication Governance, Gate 1 proposal (+5 more)

### Community 10 - "type"
Cohesion: 0.22
Nodes (11): items, type, uniqueItems, minLength, type, forbidden_effects, turns, items (+3 more)

### Community 12 - "Evaluation Authentication Governance implementation plan"
Cohesion: 0.17
Nodes (12): Approved design inputs, Delivery slices, Evaluation Authentication Governance implementation plan, Global constraints and non-goals, Goal, Machine-readable verification inventory, Repository context, Residual risk and deferred work (+4 more)

### Community 13 - "properties"
Cohesion: 0.20
Nodes (10): type, type, properties, accepted_deltas, approved_by, schema_version, source_commit, const (+2 more)

### Community 14 - "compatibility"
Cohesion: 0.20
Nodes (10): additionalProperties, properties, required, type, enum, items, type, compatibility (+2 more)

### Community 15 - "observations.py"
Cohesion: 0.22
Nodes (17): FileRecord, GitState, NormalizedEvent, Observation, Normalize process, runtime, filesystem, Git, and checkpoint evidence., RuntimeStatus, Path, test_run_case_routes_turns_and_scenarios_to_their_separate_runners() (+9 more)

### Community 16 - "Compaction Recovery decisions"
Cohesion: 0.13
Nodes (14): Assumptions, Compaction Recovery decisions, Confirmed, DEC-CR-001 — Recover at the native compactation continuation boundary, DEC-CR-002 — Adopt delivery checkpoint schema version 3, DEC-CR-003 — Keep hook state transient, DEC-CR-004 — Fail safe on ambiguity, not on ordinary absence, DEC-CR-005 — Use one standard-library discovery hook (+6 more)

### Community 17 - "properties"
Cohesion: 0.17
Nodes (12): enum, properties, activation, repetitions, sandbox, schema_version, semantic_rubric, minimum (+4 more)

### Community 18 - "type"
Cohesion: 0.22
Nodes (9): items, type, uniqueItems, type, comparison_ids, residual_risks, items, type (+1 more)

### Community 19 - "Devquitect Skill Development System architecture"
Cohesion: 0.07
Nodes (29): 10. Reporting and CI adapter, 1. Source registry and snapshot manager, 2. Structural validator, 3. Fixture materializer, 4. Codex execution adapter, 5. Observation collector, 6. Deterministic assertion engine, 7. Independent semantic grader (+21 more)

### Community 20 - "schemas/eval-case.schema.json"
Cohesion: 0.22
Nodes (8): additionalProperties, $id, oneOf, required, $schema, title, type, x-devquitect-schema-version

### Community 21 - "items"
Cohesion: 0.25
Nodes (8): items, type, properties, required, assertions, type, minLength, type

### Community 22 - "schemas/promotion-record.schema.json"
Cohesion: 0.25
Nodes (7): additionalProperties, $id, required, $schema, title, type, x-devquitect-schema-version

### Community 23 - "Evaluation Authentication Governance architecture"
Cohesion: 0.18
Nodes (11): Alternatives considered, Assumptions, Build a general authentication-provider framework, Confirmed, Current architecture, Evaluation Authentication Governance architecture, Keep implicit cache discovery, Open decisions (+3 more)

### Community 24 - "Compaction Recovery concept"
Cohesion: 0.14
Nodes (13): Actors and external systems, Assumptions, Change Profile, Compaction Recovery concept, Conceptual direction, Confirmed, Desired outcome, Gate 1 proposal (+5 more)

### Community 25 - "valid-plugin/schemas/calibration-report.schema.json"
Cohesion: 0.50
Nodes (3): $schema, type, x-devquitect-schema-version

### Community 26 - "valid-plugin/schemas/eval-case.schema.json"
Cohesion: 0.50
Nodes (3): $schema, type, x-devquitect-schema-version

### Community 27 - "valid-plugin/schemas/promotion-record.schema.json"
Cohesion: 0.50
Nodes (3): $schema, type, x-devquitect-schema-version

### Community 28 - "valid-plugin/schemas/report.schema.json"
Cohesion: 0.50
Nodes (3): $schema, type, x-devquitect-schema-version

### Community 29 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 30 - "fixture"
Cohesion: 0.67
Nodes (3): minLength, type, fixture

### Community 31 - "id"
Cohesion: 0.67
Nodes (3): pattern, type, id

### Community 32 - "scenario"
Cohesion: 0.17
Nodes (12): oneOf, scenario, steps, version, additionalProperties, properties, required, type (+4 more)

### Community 33 - "tags"
Cohesion: 0.67
Nodes (3): tags, type, uniqueItems

### Community 34 - "target_skill"
Cohesion: 0.67
Nodes (3): target_skill, pattern, type

### Community 35 - "approved_at"
Cohesion: 0.67
Nodes (3): format, type, approved_at

### Community 36 - "package_digest"
Cohesion: 0.67
Nodes (3): pattern, type, package_digest

### Community 37 - "run_ids"
Cohesion: 0.67
Nodes (3): run_ids, type, uniqueItems

### Community 38 - "snapshot_id"
Cohesion: 0.67
Nodes (3): snapshot_id, pattern, type

### Community 39 - "version"
Cohesion: 0.67
Nodes (3): version, pattern, type

### Community 41 - "verify_slice.py"
Cohesion: 0.18
Nodes (36): datetime, MappingNode, _check(), _close(), ConcurrentChangeError, _definition(), _detail(), _digest() (+28 more)

### Community 42 - "Devquitect Skill Development System implementation plan"
Cohesion: 0.10
Nodes (20): Approved acceptance-scenario coverage, Approved inputs, Assumptions, Confirmed, Delivery ordering and authorization boundary, Delivery slices, Devquitect Skill Development System implementation plan, Global constraints and non-goals (+12 more)

### Community 43 - "Devquitect Skill Development System contracts"
Cohesion: 0.17
Nodes (12): Assertion plug-in contract, Assumptions, Common options, Compatibility contract, Confirmed, Devquitect Skill Development System contracts, Eval case YAML contract, Exit codes (+4 more)

### Community 44 - "Devquitect Skill Development System data model"
Cohesion: 0.12
Nodes (16): Aggregate relationships, Assumptions, Candidate lifecycle, Comparison, Compatibility and migration, Confirmed, Devquitect Skill Development System data model, EvalCase (+8 more)

### Community 45 - "Devquitect Skill Development System decisions"
Cohesion: 0.12
Nodes (16): ADR-001 — Controlled self-hosting, not circular self-validation, ADR-002 — Behavioral contracts assert observations, not exact prose, ADR-003 — Deterministic invariants dominate semantic grading, ADR-004 — Python orchestrator with a Codex CLI adapter, ADR-005 — Immutable content-addressed snapshots, ADR-006 — Fresh isolation per case and attempt, ADR-007 — YAML cases, JSON Schema validation, JSON evidence, ADR-008 — Separate fast checks from credentialed behavioral evals (+8 more)

### Community 46 - "Handoff notes"
Cohesion: 0.12
Nodes (15): Authorized-scope completion review, Current objective, Delivery checkpoint, Final authorized-scope completion, Handoff notes, Last completed work, SLICE-001, SLICE-002 (+7 more)

### Community 47 - "Diseño técnico — Verificación de slices"
Cohesion: 0.13
Nodes (15): Assumptions, Compatibilidad, adopción y reversión, Componentes y autoridad, Confirmed, Contrato del detalle por slice, Contrato del plan, Decisiones y alternativas, Diseño técnico — Verificación de slices (+7 more)

### Community 48 - "Requisitos y escenarios de aceptación"
Cohesion: 0.15
Nodes (13): Assumptions, Confirmed, Contrato propuesto de verificación, Evaluación futura de la mejora, Open decisions, REQ-SV-01 — Verificar antes de cerrar y avanzar, REQ-SV-02 — Evidencia atómica y trazable, REQ-SV-03 — Estados inequívocos (+5 more)

### Community 49 - "Proportional Change Profile decisions"
Cohesion: 0.17
Nodes (12): Assumptions, Confirmed, DEC-001 — Use a routing profile, not a generated artifact, DEC-002 — Default provisional work to standard, DEC-003 — Permit combined approval only for confirmed expedited work, DEC-004 — Retain checkpoint schema version 2, DEC-005 — Centralize normative rules, DEC-006 — Elevate automatically and visibly (+4 more)

### Community 50 - "Proportional Change Profile implementation plan"
Cohesion: 0.17
Nodes (12): Approved inputs, Assumptions, Confirmed, Delivery slices, Final readiness review, Global constraints and non-goals, Goal and observable outcome, Open decisions (+4 more)

### Community 51 - "Devquitect Skill Development System concept"
Cohesion: 0.17
Nodes (12): Actors, Assumptions, Confirmed, Controlled self-hosting rule, Core workflow, Desired outcome, Devquitect Skill Development System concept, First-release scope (+4 more)

### Community 52 - "Confirmed"
Cohesion: 0.18
Nodes (10): Assumptions, Behavior calibration, Confirmed, Current authority map, Instruction Governance, Open decisions, Preserved behavior, Proposed authority and validation model (+2 more)

### Community 53 - "Instruction Governance brainstorm"
Cohesion: 0.18
Nodes (10): 2026-09-09 — Authority map and policy proposal, 2026-09-09 — Clarified intended mechanisms, 2026-09-09 — Promotion-evaluation assessment, 2026-09-09 — Repository guidance, 2026-09-09 — Scope reduced to critical contracts, 2026-09-09 — Seed and baseline, 2026-09-10 — Correction, 2026-09-10 — Evaluation and promotion boundary (+2 more)

### Community 54 - "Proportional Change Profile concept"
Cohesion: 0.18
Nodes (11): Assumptions, Baseline and requested delta, Confirmed, Desired outcome, Interaction surface, Non-goals, Open decisions, Preserved behavior (+3 more)

### Community 55 - "Devquitect Skill Development System requirements"
Cohesion: 0.18
Nodes (11): Acceptance scenarios, Assumptions, Authoring and discovery, Behavioral isolation and evidence, Confirmed, Controlled self-hosting, Critical workflow protection, Devquitect Skill Development System requirements (+3 more)

### Community 56 - "Devquitect Skill Development System — decision trail"
Cohesion: 0.18
Nodes (10): 2026-08-30 — Controlled self-hosting, 2026-08-30 — Development-system direction, 2026-08-30 — Gate 1 approved, 2026-08-30 — Gate 2 approved, 2026-08-30 — Implementation plan approved, 2026-08-30 — Implementation plan ready for approval, 2026-08-30 — Initial problem framing, 2026-08-30 — Persistent mode (+2 more)

### Community 57 - "Instruction Governance Implementation Plan"
Cohesion: 0.20
Nodes (9): Constraints, Deferred, Goal, Instruction Governance Implementation Plan, SLICE-001 — Authority map validation, SLICE-002 — Calibration report contract, SLICE-003 — Promotion separation and documentation, Slices (+1 more)

### Community 58 - "Proportional Change Profile architecture"
Cohesion: 0.20
Nodes (10): Assumptions, Compatibility and boundaries, Confirmed, Current architecture, Data and control flow, Failure and recovery behavior, Gate transition contract, Open decisions (+2 more)

### Community 59 - "Plan de implementación — Slice verification"
Cohesion: 0.20
Nodes (10): Arranque y revisión acumulada de esta entrega, Assumptions, Confirmed, Handoff, Inventario ejecutable del plan, Open decisions, Plan de implementación — Slice verification, Resultado y restricciones comunes (+2 more)

### Community 60 - "Durable Session State"
Cohesion: 0.20
Nodes (10): Autonomy and terminal conditions, Discover and report sessions, Durable Session State, Gates and invalidation, Migrate schema v1 to v2, Portability boundary, Recover missing, corrupt, or stale state, Resume by state (+2 more)

### Community 61 - "test_slice_verification.py"
Cohesion: 0.31
Nodes (22): make_session(), CompletedProcess, Path, run(), set_tracker_version(), test_active_legacy_operations_require_migration_without_writing(), test_check_rejects_stale_inputs_and_fail_evidence(), test_check_requires_complete_criterion_and_check_evidence() (+14 more)

### Community 62 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 63 - "Confirmed"
Cohesion: 0.22
Nodes (8): Assumptions, Boundaries and flow, Components, Confirmed, Data and lifecycle, Instruction Governance Architecture, Interfaces, Open decisions

### Community 64 - "project-plan-execution/SKILL.md"
Cohesion: 0.20
Nodes (6): Slice verification, Establish the execution context, Execute and verify, Preserve boundaries, Project Plan Execution, Require an authorized handoff

### Community 65 - "Verificación de entregas por slice"
Cohesion: 0.22
Nodes (9): Assumptions, Confirmed, Contraste con OpenSpec, Dónde guardar la evidencia, Objetivo y límites, Open decisions, Opinión: funcionará con estas condiciones, Perfil y experiencia (+1 more)

### Community 67 - "Proportional Change Profile"
Cohesion: 0.22
Nodes (9): Apply approval gates, Elevate and invalidate safely, Establish and confirm the profile, Present the profile, Preserve cross-skill boundaries, Profile model, Proportional Change Profile, Purpose and ownership (+1 more)

### Community 68 - "Proportional Change Profile data model"
Cohesion: 0.25
Nodes (8): Assumptions, Checkpoint extension, Compatibility, Confirmed, Invariants, Lifecycle, Open decisions, Proportional Change Profile data model

### Community 69 - "Historial — Slice verification"
Cohesion: 0.25
Nodes (7): 2026-09-14 — Arquitectura presentada a Gate 2, 2026-09-14 — Gate 1 aprobado, 2026-09-14 — Gate 2 aprobado, 2026-09-14 — Plan aprobado; implementación no autorizada, 2026-09-14 — Plan preparado para aprobación, 2026-09-14 — Semilla, investigación y dirección propuesta, Historial — Slice verification

### Community 70 - "Persistent Artifacts"
Cohesion: 0.25
Nodes (8): Artifact set, Authority and evolution, Canonical document header, Change Profile ownership, Chat-only mode, Persistent Artifacts, Session directory, Shared system context

### Community 71 - "Discovery and Crystallization"
Cohesion: 0.25
Nodes (8): Crystallize and apply Gate 1, Discovery and Crystallization, Establish initiative context and baseline, Expand, Explore technical alternatives, Frame, Refine, Research only when it changes a decision

### Community 72 - "Repository instructions"
Cohesion: 0.29
Nodes (6): Behavioral tests and usage, Evolving Devquitect skills, graphify, Repository boundaries, Repository instructions, Verification after changes

### Community 73 - "Proportional Change Profile requirements"
Cohesion: 0.29
Nodes (7): Acceptance scenarios, Assumptions, Confirmed, Functional requirements, Interaction requirements, Open decisions, Proportional Change Profile requirements

### Community 74 - "Delivery checkpoint"
Cohesion: 0.29
Nodes (6): Current objective, Delivery checkpoint, Handoff notes, Last completed work, SLICE-001, Slice evidence

### Community 75 - "Proportional Change Profile brainstorm"
Cohesion: 0.29
Nodes (6): 2026-08-31 — Architecture and Gate 2, 2026-08-31 — Design crystallization and Gate 1, 2026-08-31 — Persistent transition, 2026-08-31 — Plan approval, 2026-08-31 — Seed and baseline, Proportional Change Profile brainstorm

### Community 77 - "System Context and Baseline"
Cohesion: 0.29
Nodes (7): Authority and current versus proposed state, Content, Document contract, Establish the baseline proportionally, Purpose and location, System Context and Baseline, Update discipline

### Community 78 - "Technical Design"
Cohesion: 0.29
Nodes (7): Apply Gate 2 — Architecture readiness, Assess an expedited no-change path, Define interfaces and contracts, Derive the architecture, Model the domain and data, Preserve traceability, Technical Design

### Community 79 - "Software Idea to Project"
Cohesion: 0.29
Nodes (7): Enforce the boundary, Establish context and mode, Finish at the correct boundary, Maintain artifacts deliberately, Report or resume durable work, Run the workflow progressively, Software Idea to Project

### Community 80 - "graphify reference: query, path, explain"
Cohesion: 0.33
Nodes (5): For /graphify explain, For /graphify path, graphify reference: query, path, explain, Step 0 — Constrained query expansion (REQUIRED before traversal), Step 1 — Traversal

### Community 81 - "Confirmed"
Cohesion: 0.33
Nodes (5): Authority map, Calibration report, Confirmed, Instruction Governance Data Model, Open decisions

### Community 82 - "Delivery checkpoint"
Cohesion: 0.33
Nodes (5): Current objective, Delivery checkpoint, Handoff notes, Last completed work, Slice evidence

### Community 83 - "Contributing skills"
Cohesion: 0.20
Nodes (10): Author behavioral cases, Command and evidence matrix, Compare stable N with candidate N+1, Contributing skills, Contributor walkthrough, Package an exact candidate, Propose promotion and recover, Required structure (+2 more)

### Community 84 - "Delivery checkpoint"
Cohesion: 0.11
Nodes (17): 2026-09-14T21:38:22.550643Z/slice-verification, Correction attempt, Current objective, Current objective, Delivery checkpoint, Delivery checkpoint, Delivery history, Final contract audit (+9 more)

### Community 85 - "Durable Delivery State"
Cohesion: 0.29
Nodes (7): Discover and report, Durable Delivery State, Frontier refresh and legacy compatibility, Initialization and schema, Link the definition checkpoint, Plan changes and recovery, Update and resume

### Community 86 - "Authorized Slice Execution"
Cohesion: 0.33
Nodes (6): Authorized Slice Execution, Completion review, Execution loop, External actions, Failures and blockers, Preflight

### Community 87 - "Experience Design"
Cohesion: 0.33
Nodes (6): Apply experience readiness at Gate 1, Classify the interaction surface, Define the consequential experience, Experience Design, Persist only when useful, Use specialized design capabilities conditionally

### Community 88 - "Current checkpoint"
Cohesion: 0.40
Nodes (4): Current checkpoint, Current objective, Handoff notes, Last completed work

### Community 89 - "Instruction Governance Requirements"
Cohesion: 0.40
Nodes (4): Assumptions, Confirmed, Instruction Governance Requirements, Open decisions

### Community 90 - "Current checkpoint"
Cohesion: 0.40
Nodes (4): Current checkpoint, Current objective, Handoff notes, Last completed work

### Community 91 - "Compaction Recovery architecture"
Cohesion: 0.14
Nodes (14): Assumptions, Behavioral evaluation architecture, Compaction Recovery architecture, Compatibility, rollout, and rollback, Components and ownership, Confirmed basis, Failure boundaries, Gate 2 proposal (+6 more)

### Community 92 - "Current checkpoint"
Cohesion: 0.40
Nodes (4): Current checkpoint, Current objective, Handoff notes, Last completed work

### Community 93 - "slice-verification/01-concept.md"
Cohesion: 0.25
Nodes (4): Checkpoint actual, Notas de continuidad, Objetivo actual, Último trabajo completado

### Community 94 - "codex_adapter.py"
Cohesion: 0.11
Nodes (23): build_command(), CodexPreflight, preflight_codex(), Path, Codex CLI adapter with explicit isolation and failure classification., Run one fresh attempt; adapter/auth/service failures remain inconclusive., Verify the runtime and capabilities assumed by the approved adapter., run_codex() (+15 more)

### Community 95 - "Adaptive Implementation Planning"
Cohesion: 0.40
Nodes (5): Adaptive Implementation Planning, Choose evidence-based precision, Final readiness review, Plan structure, Validation coverage

### Community 96 - "graphify reference: add a URL and watch a folder"
Cohesion: 0.50
Nodes (3): For /graphify add, For --watch, graphify reference: add a URL and watch a folder

### Community 97 - "graphify reference: commit hook and native CLAUDE.md integration"
Cohesion: 0.50
Nodes (3): For git commit hook, For native CLAUDE.md integration, graphify reference: commit hook and native CLAUDE.md integration

### Community 98 - "graphify reference: incremental update and cluster-only"
Cohesion: 0.50
Nodes (3): For --cluster-only, For --update (incremental re-extraction), graphify reference: incremental update and cluster-only

### Community 99 - "Instruction Governance Interfaces"
Cohesion: 0.50
Nodes (3): Confirmed, Instruction Governance Interfaces, Open decisions

### Community 100 - "Instruction Governance Decisions"
Cohesion: 0.50
Nodes (3): Confirmed, Instruction Governance Decisions, Open decisions

### Community 107 - "Functional requirements"
Cohesion: 0.20
Nodes (10): Functional requirements, REQ-EAG-001 — Preserve the credential-free path, REQ-EAG-002 — Make behavioral authentication explicit, REQ-EAG-003 — Gate unattended execution, REQ-EAG-004 — Isolate credentials per attempt, REQ-EAG-005 — Establish restrictive permissions at creation, REQ-EAG-006 — Define cleanup guarantees honestly, REQ-EAG-007 — Recover stale material without exposing it (+2 more)

### Community 108 - "Compaction Recovery brainstorm"
Cohesion: 0.17
Nodes (11): 2026-09-19 — Direction refined, 2026-09-19 — External evidence, 2026-09-19 — Gate 1 approved, 2026-09-19 — Gate 1 prepared, 2026-09-19 — Gate 2 approved and plan revision 1 prepared, 2026-09-19 — Gate 2 prepared, 2026-09-19 — Implementation plan revision 1 approved, 2026-09-19 — Native hook activation clarified (+3 more)

### Community 109 - "Devquitect system context"
Cohesion: 0.17
Nodes (12): Actors and external systems, Authoritative references, Current capabilities, Current lifecycle, Development and verification, Devquitect system context, Known limitations and context gaps, Preserved behavior (+4 more)

### Community 111 - "test_fake_codex_run.py"
Cohesion: 0.71
Nodes (6): fake_codex(), git(), Path, snapshot(), test_fake_adapter_cleans_auth_after_child_failure_timeout_and_malformed_output(), test_fake_adapter_run_is_normalized_and_read_only_violation_fails()

### Community 116 - "Compaction Recovery interface contracts"
Cohesion: 0.18
Nodes (11): Acceptance mapping, Activation contract, Behavioral case extension, Checkpoint discovery contract, Compaction Recovery interface contracts, Compatibility and security, Hook configuration, Hook input and output (+3 more)

### Community 117 - "Plan de implementación — Compaction Recovery"
Cohesion: 0.18
Nodes (11): Assumptions and deferred work, Confirmed, Delivery order, cumulative review, and authorization, Executable verification inventory, Handoff, Outcome and common constraints, Plan de implementación — Compaction Recovery, SLICE-001 — Versioned execution frontier and legacy-safe state guard (+3 more)

### Community 118 - "Evaluation Authentication Governance domain"
Cohesion: 0.22
Nodes (8): Assumptions, Concepts and ownership, Confirmed, Data sensitivity, Evaluation Authentication Governance domain, Open decisions, Rules, State transitions

### Community 119 - "compaction-recovery/08-implementation-plan.md"
Cohesion: 0.20
Nodes (4): Current checkpoint, Current objective, Handoff notes, Last completed work

### Community 120 - "Evaluation Authentication Governance brainstorm"
Cohesion: 0.22
Nodes (8): 2026-09-21 — Gate 1 approval and technical design, 2026-09-21 — Gate 1 proposal, 2026-09-21 — Gate 2 approval and implementation planning, 2026-09-21 — Initial direction, 2026-09-21 — Plan approval, 2026-09-21 — Risk and policy research, 2026-09-21 — Seed and baseline, Evaluation Authentication Governance brainstorm

### Community 121 - "Evaluation Authentication Governance contracts"
Cohesion: 0.25
Nodes (8): Assumptions, Compatibility and migration, Confirmed, Evaluation Authentication Governance contracts, Internal adapter contract, Open decisions, Proposed CLI contract, Proposed report metadata

### Community 122 - "Compaction Recovery requirements"
Cohesion: 0.25
Nodes (8): Acceptance scenarios, Assumptions, Compaction Recovery requirements, Confirmed, Non-goals, Open decisions, Quality requirements, Verification requirements

### Community 123 - "Compaction Recovery data model"
Cohesion: 0.25
Nodes (8): Canonical checkpoint shape, Compaction Recovery data model, Decision, Field contract, Freshness transitions, Invariants, Legacy transition, Verification obligations

### Community 124 - "Functional requirements"
Cohesion: 0.33
Nodes (6): Delivery state, Functional requirements, Operator interaction, Packaging and compatibility, Recovery behavior, Runtime trigger

### Community 125 - "Delivery checkpoint"
Cohesion: 0.33
Nodes (5): Current objective, Delivery checkpoint, Handoff notes, Last completed work, Slice evidence

### Community 126 - "evaluation.py"
Cohesion: 0.20
Nodes (16): AssertionResult, evaluate_assertion(), evaluate_assertions(), _matches(), Any, Side-effect-free deterministic assertions over normalized observations., Evaluate one immutable specification without invoking tools or modifying…, Behavioral case orchestration over immutable skill snapshots. (+8 more)

### Community 127 - "Q: How does Devquitect recover delivery execution after Codex context compaction?"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: How does Devquitect recover delivery execution after Codex context compaction?, Source Nodes

### Community 129 - "compaction_recovery.py"
Cohesion: 0.25
Nodes (15): _bounded_output(), _candidate_paths(), _classify(), _context(), _frontmatter(), HookError, _load_event(), main() (+7 more)

### Community 130 - "Evaluation Authentication Governance decisions"
Cohesion: 0.25
Nodes (8): Assumptions, Confirmed, DEC-EAG-001 — Retain local subscription mode only as explicit opt-in, DEC-EAG-002 — Use one explicit auth-mode boundary, DEC-EAG-003 — Best-effort stale cleanup with no SIGKILL claim, DEC-EAG-004 — Prohibit unattended subscription-cache execution, Evaluation Authentication Governance decisions, Open decisions

### Community 131 - "test_compaction_recovery_hook.py"
Cohesion: 0.41
Nodes (15): add_checkpoint(), event(), make_repo(), CompletedProcess, parametrize, Path, run_hook(), test_discovery_does_not_follow_escaping_session_symlink() (+7 more)

### Community 132 - "Commands"
Cohesion: 0.29
Nodes (7): Commands, `devquitect check`, `devquitect compare`, `devquitect eval`, `devquitect package`, `devquitect release-check`, `devquitect validate`

### Community 133 - "validate.py"
Cohesion: 0.14
Nodes (34): Create one stable, machine-readable structural-validation record., validation_record(), _authority_map_paths(), _authority_path(), _git(), load_directory_inputs(), load_validation_inputs(), _local_references() (+26 more)

### Community 134 - "Compaction recovery contract"
Cohesion: 0.40
Nodes (4): Compaction recovery contract, Hook limits, Outcomes and operator messages, Recovery sequence

### Community 143 - "Evaluation Authentication Governance requirements"
Cohesion: 0.29
Nodes (7): Acceptance scenarios, Assumptions, Confirmed, Evaluation Authentication Governance requirements, Non-functional requirements, Open decisions, Preserved behavior

### Community 146 - "software-design/system-context.md"
Cohesion: 0.17
Nodes (9): Devquitect, Local definition of done, Choose the smallest safe workflow, Define the refactor contract, Establish intent and evidence, Implement a minimal coherent refactor, Report the result, Targeted Refactoring (+1 more)

### Community 147 - "_run_calibrate"
Cohesion: 0.12
Nodes (28): Namespace, Runner, AuthPolicyError, ValueError, The requested authentication mode is missing or not allowed., CaseError, EvalCase, load_cases() (+20 more)

### Community 150 - "Proposed architecture"
Cohesion: 0.33
Nodes (6): Components and responsibilities, Credential lifecycle, Failure and compatibility behavior, Proposed architecture, Stale cleanup, Trust boundaries

### Community 151 - "cli.py"
Cohesion: 0.15
Nodes (21): ArgumentParser, _add_auth_options(), _calibration_dimensions(), _calibration_evidence(), _check_record(), _configuration_failure(), _nested_command(), _parser() (+13 more)

### Community 152 - "Current checkpoint"
Cohesion: 0.40
Nodes (4): Current checkpoint, Current objective, Handoff notes, Last completed work

### Community 153 - "parse_jsonl_events"
Cohesion: 0.16
Nodes (17): _event_detail(), parse_jsonl_events(), Any, Parse untrusted JSONL as data and return bounded normalized evidence., Any, Bounded, deterministic secret redaction for retained evaluation evidence., Mask known values and common credential shapes without retaining the secret., Recursively redact a JSON-compatible evidence value. (+9 more)

### Community 154 - "test_validate.py"
Cohesion: 0.45
Nodes (13): _codes(), _copy_fixture(), _path_parts(), parametrize, Path, test_hook_contract_rejects_unsafe_variants(), test_malformed_case_and_missing_fixture_are_reported(), test_missing_hook_config_is_reported() (+5 more)

### Community 155 - "resolve_auth"
Cohesion: 0.24
Nodes (11): AuthSelection, Path, Explicit authentication policy for behavioral commands., Validate explicit auth without reading credential contents., resolve_auth(), test_api_key_requires_only_the_supported_environment_boundary(), test_behavioral_auth_must_be_explicit(), test_local_cache_is_refused_for_unattended_behavior() (+3 more)

### Community 156 - "Delivery checkpoint"
Cohesion: 0.33
Nodes (5): Current objective, Delivery checkpoint, Handoff notes, Last completed work, Slice evidence

### Community 158 - "test_auth_lifecycle.py"
Cohesion: 0.47
Nodes (4): Path, test_staging_is_owner_only_from_creation_and_cleans_partial_copy(), test_staging_rejects_symlink_and_group_accessible_sources(), test_stale_cleanup_requires_marker_age_ownership_and_dead_process()

### Community 159 - "Proposed architecture"
Cohesion: 0.40
Nodes (5): Contextual integrations, Normative Change Profile reference, Proposed architecture, Quality evidence, Workflow orchestrator

## Knowledge Gaps
- **835 isolated node(s):** `devquitect-quality`, `$schema`, `$id`, `x-devquitect-schema-version`, `title` (+830 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1016 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **27 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `resolve_auth()` connect `resolve_auth` to `_run_calibrate`, `cli.py`?**
  _High betweenness centrality (0.007) - this node is a cross-community bridge._
- **Why does `build_package()` connect `build_package` to `freeze_source`, `reporting.py`, `cli.py`?**
  _High betweenness centrality (0.005) - this node is a cross-community bridge._
- **Why does `Diseño técnico — Verificación de slices` connect `Diseño técnico — Verificación de slices` to `slice-verification/01-concept.md`?**
  _High betweenness centrality (0.004) - this node is a cross-community bridge._
- **Are the 8 inferred relationships involving `freeze_source()` (e.g. with `SkillSource` and `snapshot()`) actually correct?**
  _`freeze_source()` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `build_package()` (e.g. with `SkillSource` and `SourceError`) actually correct?**
  _`build_package()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `SkillSource` (e.g. with `_configuration_failure()` and `_run_calibrate()`) actually correct?**
  _`SkillSource` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `SourceError` (e.g. with `_configuration_failure()` and `_run_calibrate()`) actually correct?**
  _`SourceError` has 9 INFERRED edges - model-reasoned connections that need verification._