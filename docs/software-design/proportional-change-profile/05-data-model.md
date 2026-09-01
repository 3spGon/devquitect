# Proportional Change Profile data model

Status: Approved
Last updated: 2026-08-31

## Confirmed

- The profile is operational workflow state, not a separate project document.
- Existing schema-v2 checkpoints remain valid without the field.

## Assumptions

- YAML null is used for impact while a profile is provisional and evidence is insufficient.

## Open decisions

No implementation-blocking data decisions remain.

## Checkpoint extension

For `system-change` and `hybrid` sessions, new or materially updated checkpoints may include:

```yaml
change_profile:
  status: provisional | confirmed
  kinds:
    - bug-fix | behavior-change | new-capability | technical-change | migration | deprecation
  impact: localized | bounded | cross-cutting | null
  workflow_depth: expedited | standard | full
  affected_surfaces:
    - behavior
    - experience
    - domain
    - data
    - interfaces
    - security-privacy
    - operations
    - quality-attributes
    - migration-compatibility
  elevation_reasons: []
```

The field is omitted for `new-system` sessions and may be absent in older schema-v2 sessions.

## Invariants

- `provisional` uses `workflow_depth: standard` unless confirmed evidence already requires `full`; it may have empty kinds and surfaces and null impact.
- `confirmed` requires non-empty `kinds`, non-null `impact`, and non-empty `affected_surfaces`.
- `expedited` requires `status: confirmed`, `impact: localized`, no elevation reason, no material open decision, and satisfaction of every expedited eligibility rule.
- `cross-cutting` requires `workflow_depth: full`.
- `elevation_reasons` records current evidence that makes a lower depth unsafe; it is not a historical log. Historical transitions belong in `brainstorm.md`.
- Values are unique within `kinds`, `affected_surfaces`, and `elevation_reasons`.
- Profile changes are written atomically with the enclosing checkpoint revision update.

## Lifecycle

```text
absent -> provisional -> confirmed
                         |       |
                         v       v
                    elevated  invalidated evidence
                         |       |
                         +-> reconfirmed
```

Absence is valid for legacy checkpoints and new-system initiatives. A material evidence change may return a confirmed profile to provisional while the workflow re-evaluates depth; affected gates follow the invalidation rules in [04-architecture.md](04-architecture.md).

## Compatibility

- Session `schema_version` remains `2`.
- No bulk migration or rewrite of historical checkpoints is permitted.
- A normal state-changing resume may populate the field when the initiative is `system-change` or `hybrid` and the profile is relevant.
- A status-only read reports the absence without mutating the session.
