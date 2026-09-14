# Graph Report - devquitect-instruction-governance  (2026-09-10)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 617 nodes · 1232 edges · 41 communities (40 shown, 1 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 77 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8f874f69`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- freeze_source
- cli.py
- build_package
- properties
- properties
- validate.py
- evaluation.py
- schemas/authority-map.schema.json
- valid-plugin/schemas/authority-map.schema.json
- codex_adapter.py
- type
- parse_jsonl_events
- test_validate.py
- properties
- compatibility
- fixtures.py
- redact_value
- properties
- type
- classify_results
- schemas/eval-case.schema.json
- items
- schemas/promotion-record.schema.json
- observation
- test_fake_codex_run.py
- valid-plugin/schemas/calibration-report.schema.json
- valid-plugin/schemas/eval-case.schema.json
- valid-plugin/schemas/promotion-record.schema.json
- valid-plugin/schemas/report.schema.json
- test_check_command.py
- fixture
- id
- repetitions
- tags
- target_skill
- approved_at
- package_digest
- run_ids
- snapshot_id
- version
- devquitect-quality

## God Nodes (most connected - your core abstractions)
1. `freeze_source()` - 32 edges
2. `SourceError` - 26 edges
3. `build_package()` - 25 edges
4. `_run_calibrate()` - 23 edges
5. `SkillSource` - 22 edges
6. `_run_compare()` - 19 edges
7. `_run_eval()` - 18 edges
8. `_run_validate()` - 18 edges
9. `release_check()` - 18 edges
10. `ValidationConfigurationError` - 16 edges

## Surprising Connections (you probably didn't know these)
- `observation()` --uses--> `NormalizedEvent`  [INFERRED]
  tests/unit/test_assertions.py → src/devquitect_quality/observations.py
- `test_unsupported_schema_is_an_invalid_configuration()` --uses--> `ValidationConfigurationError`  [INFERRED]
  tests/unit/test_validate.py → src/devquitect_quality/validate.py
- `observation()` --uses--> `Observation`  [INFERRED]
  tests/unit/test_assertions.py → src/devquitect_quality/observations.py
- `observation()` --uses--> `GitState`  [INFERRED]
  tests/unit/test_assertions.py → src/devquitect_quality/observations.py
- `test_critical_suite_has_fixed_repetitions_and_non_overridable_policy()` --uses--> `RuntimeStatus`  [INFERRED]
  tests/integration/test_eval_command.py → src/devquitect_quality/observations.py

## Import Cycles
- None detected.

## Communities (41 total, 1 thin omitted)

### Community 0 - "freeze_source"
Cohesion: 0.07
Nodes (61): skipif, freeze_pair(), FrozenPair, Path, Stable/candidate pairing and safety-dominant comparison classification., Freeze both identities before either can execute., Quality tooling for the Devquitect skill bundle., Path (+53 more)

### Community 1 - "cli.py"
Cohesion: 0.08
Nodes (58): ArgumentParser, CompletedProcess, Namespace, CaseError, EvalCase, load_cases(), Path, ValueError (+50 more)

### Community 2 - "build_package"
Cohesion: 0.09
Nodes (50): build_package(), _git(), _normalize_manifest(), PackageArtifact, PackageEntry, PackageError, Path, PurePosixPath (+42 more)

### Community 3 - "properties"
Cohesion: 0.04
Nodes (45): additionalProperties, type, maxItems, type, format, type, $id, minLength (+37 more)

### Community 4 - "properties"
Cohesion: 0.04
Nodes (44): additionalProperties, minLength, type, type, format, type, $id, type (+36 more)

### Community 5 - "validate.py"
Cohesion: 0.12
Nodes (37): normalize_relative_path(), Path, Return a portable repository-relative path or reject an unsafe one., Create one stable, machine-readable structural-validation record., validation_record(), _authority_path(), _git(), load_directory_inputs() (+29 more)

### Community 6 - "evaluation.py"
Cohesion: 0.16
Nodes (21): Runner, AssertionResult, evaluate_assertion(), evaluate_assertions(), _matches(), Any, Side-effect-free deterministic assertions over normalized observations., Evaluate one immutable specification without invoking tools or modifying… (+13 more)

### Community 7 - "schemas/authority-map.schema.json"
Cohesion: 0.09
Nodes (26): additionalProperties, items, type, $id, minLength, type, additionalProperties, properties (+18 more)

### Community 8 - "valid-plugin/schemas/authority-map.schema.json"
Cohesion: 0.09
Nodes (24): additionalProperties, items, type, minLength, type, additionalProperties, properties, required (+16 more)

### Community 9 - "codex_adapter.py"
Cohesion: 0.14
Nodes (20): build_command(), CodexPreflight, preflight_codex(), Path, Pinned Codex CLI adapter with explicit isolation and failure classification., Run one fresh attempt; adapter/auth/service failures remain inconclusive., Verify the exact runtime version and flags assumed by the approved adapter., run_codex() (+12 more)

### Community 10 - "type"
Cohesion: 0.22
Nodes (11): items, type, uniqueItems, minLength, type, forbidden_effects, turns, items (+3 more)

### Community 11 - "parse_jsonl_events"
Cohesion: 0.22
Nodes (10): _event_detail(), NormalizedEvent, parse_jsonl_events(), Any, Parse untrusted JSONL as data and return bounded normalized evidence., Path, test_filesystem_manifest_records_content_and_does_not_follow_symlinks(), test_success_stream_normalizes_commands_final_message_and_terminal_event() (+2 more)

### Community 12 - "test_validate.py"
Cohesion: 0.47
Nodes (10): _codes(), _copy_fixture(), _path_parts(), parametrize, Path, test_malformed_case_and_missing_fixture_are_reported(), test_quality_failures_have_specific_machine_records(), test_unsupported_schema_is_an_invalid_configuration() (+2 more)

### Community 13 - "properties"
Cohesion: 0.20
Nodes (10): type, type, properties, accepted_deltas, approved_by, schema_version, source_commit, const (+2 more)

### Community 14 - "compatibility"
Cohesion: 0.20
Nodes (10): additionalProperties, properties, required, type, enum, items, type, compatibility (+2 more)

### Community 15 - "fixtures.py"
Cohesion: 0.29
Nodes (6): FixtureAttempt, _initialize_git(), materialize_attempt(), Path, Fresh fixture, skill-discovery, configuration, and evidence namespaces., Create one isolated attempt. The caller owns cleanup unless used as a context…

### Community 16 - "redact_value"
Cohesion: 0.31
Nodes (9): Any, Bounded, deterministic secret redaction for retained evaluation evidence., Mask known values and common credential shapes without retaining the secret., Recursively redact a JSON-compatible evidence value., redact_text(), redact_value(), visit(), RedactionResult (+1 more)

### Community 17 - "properties"
Cohesion: 0.22
Nodes (9): enum, properties, activation, sandbox, schema_version, semantic_rubric, enum, const (+1 more)

### Community 18 - "type"
Cohesion: 0.22
Nodes (9): items, type, uniqueItems, type, comparison_ids, residual_risks, items, type (+1 more)

### Community 19 - "classify_results"
Cohesion: 0.39
Nodes (7): ComparisonClass, classify_results(), pair_records(), Any, record(), test_comparison_classifications_and_critical_precedence(), test_reviewed_declaration_requires_updated_cases()

### Community 20 - "schemas/eval-case.schema.json"
Cohesion: 0.25
Nodes (7): additionalProperties, $id, required, $schema, title, type, x-devquitect-schema-version

### Community 21 - "items"
Cohesion: 0.25
Nodes (8): items, type, properties, required, assertions, type, minLength, type

### Community 22 - "schemas/promotion-record.schema.json"
Cohesion: 0.25
Nodes (7): additionalProperties, $id, required, $schema, title, type, x-devquitect-schema-version

### Community 23 - "observation"
Cohesion: 0.67
Nodes (5): FileRecord, observation(), test_command_tool_artifact_and_final_json_assertions(), test_invalid_checkpoint_transition_fails_and_unknown_assertion_is_not_evaluated(), test_read_only_write_and_allowlist_violation_fail_deterministically()

### Community 24 - "test_fake_codex_run.py"
Cohesion: 0.73
Nodes (5): fake_codex(), git(), Path, snapshot(), test_fake_adapter_run_is_normalized_and_read_only_violation_fails()

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

### Community 29 - "test_check_command.py"
Cohesion: 0.67
Nodes (3): Path, test_check_invalid_source_returns_two_and_still_writes_report(), test_check_runs_fast_composed_definition_of_done_and_writes_atomic_report()

### Community 30 - "fixture"
Cohesion: 0.67
Nodes (3): minLength, type, fixture

### Community 31 - "id"
Cohesion: 0.67
Nodes (3): pattern, type, id

### Community 32 - "repetitions"
Cohesion: 0.67
Nodes (3): repetitions, minimum, type

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

## Knowledge Gaps
- **156 isolated node(s):** `type`, `uniqueItems`, `minItems`, `type`, `type` (+151 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 254 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `freeze_source()` connect `freeze_source` to `test_fake_codex_run.py`, `cli.py`, `build_package`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Why does `build_package()` connect `build_package` to `freeze_source`, `cli.py`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Why does `run_case()` connect `evaluation.py` to `freeze_source`, `cli.py`, `fixtures.py`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **Are the 8 inferred relationships involving `freeze_source()` (e.g. with `SkillSource` and `snapshot()`) actually correct?**
  _`freeze_source()` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `SourceError` (e.g. with `_configuration_failure()` and `_run_calibrate()`) actually correct?**
  _`SourceError` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `build_package()` (e.g. with `SkillSource` and `SourceError`) actually correct?**
  _`build_package()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `_run_calibrate()` (e.g. with `CaseError` and `SkillSource`) actually correct?**
  _`_run_calibrate()` has 4 INFERRED edges - model-reasoned connections that need verification._