---
schema_version: 2
skill: software-idea-to-project
project: Instruction Governance
session: instruction-governance
workflow_mode: persistent
initiative_context: system-change
system_context: ../system-context.md
revision: 15
phase: complete
phase_status: complete
gate_1: approved
gate_2: approved
last_updated: "2026-09-10T00:12:03-06:00"
next_action: null
pending_user_action: null
required_context:
  - brainstorm.md
  - 01-concept.md
  - 02-requirements.md
  - 04-architecture.md
  - 05-data-model.md
  - 06-api-contracts.md
  - 07-decisions.md
blockers: []
open_decisions: []
artifacts:
  brainstorm.md: active
  01-concept.md: approved
  02-requirements.md: approved
  04-architecture.md: review
  05-data-model.md: review
  06-api-contracts.md: review
  07-decisions.md: review
  08-implementation-plan.md: approved
delivery_checkpoint: 09-delivery-status.md
change_profile:
  status: provisional
  kinds:
    - technical-change
  impact: null
  workflow_depth: standard
  affected_surfaces:
    - operations
    - quality-attributes
  elevation_reasons: []
---

# Current checkpoint

## Current objective

Define two lightweight governance mechanisms: validate the ownership of cross-file critical
contracts without adding metadata to every instruction, and keep evaluation strict for safety
without treating normal model variation as a contract regression or requiring repeated 15/15 model
passes as a universal promotion condition.

## Last completed work

Mapped current instruction and evidence authorities and drafted both mechanism proposals.
Confirmed that no existing repository rule encodes universal repeated semantic passes: every
current case has one repetition, and semantic grades do not currently affect verdict or promotion
eligibility. The user selected an authority map for critical contracts plus external tests and
objective checks, rather than per-rule registration or prose linting. An evaluation audit found
that model-execution evidence needs a policy decision before a semantic threshold is meaningful.
Repository guidance now makes this product-contract and evidence approach explicit for future
skill changes. A prematurely applied promotion-policy change was reverted; both evaluation
decisions remain open.

## Handoff notes

The design is framed with a standard-depth provisional Change Profile (technical change affecting
operations and quality attributes). The role of end-to-end model evidence (DEC-IG-02) must be
settled before choosing a semantic scenario threshold (DEC-IG-01). No repository implementation
has changed.
