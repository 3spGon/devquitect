"""Immutable source and snapshot records."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

SourceKind = Literal["git-ref", "working-tree"]
AuthMode = Literal["credential-free", "api-key", "chatgpt-cache-local", "unknown"]
ExecutionContext = Literal[
    "structural", "interactive-behavioral", "unattended-behavioral", "unknown"
]
AuthPolicy = Literal["allowed", "refused", "missing", "invalid", "unknown"]
CredentialState = Literal[
    "not-needed", "injected", "staged", "cleaned", "stale", "cleanup-failed", "unknown"
]
CleanupClass = Literal["not_applicable", "handled", "stale_recovered", "failed", "unknown"]


@dataclass(frozen=True, slots=True)
class AuthenticationEvidence:
    """Non-secret authentication and credential-lifecycle report metadata."""

    mode: AuthMode
    execution_context: ExecutionContext
    policy: AuthPolicy
    credential_state: CredentialState
    cleanup: CleanupClass

    @classmethod
    def unknown(cls) -> AuthenticationEvidence:
        return cls("unknown", "unknown", "unknown", "unknown", "unknown")

    @classmethod
    def from_mapping(cls, value: Mapping[str, object] | None) -> AuthenticationEvidence:
        if value is None:
            return cls.unknown()
        expected = cls.unknown().as_dict()
        if any(value.get(key) not in allowed for key, allowed in {
            "mode": {"credential-free", "api-key", "chatgpt-cache-local", "unknown"},
            "execution_context": {
                "structural", "interactive-behavioral", "unattended-behavioral", "unknown"
            },
            "policy": {"allowed", "refused", "missing", "invalid", "unknown"},
            "credential_state": {
                "not-needed", "injected", "staged", "cleaned", "stale", "cleanup-failed", "unknown"
            },
            "cleanup": {"not_applicable", "handled", "stale_recovered", "failed", "unknown"},
        }.items()):
            return cls.unknown()
        return cls(**{key: value[key] for key in expected})  # type: ignore[arg-type]

    def as_dict(self) -> dict[str, str]:
        return {
            "mode": self.mode,
            "execution_context": self.execution_context,
            "policy": self.policy,
            "credential_state": self.credential_state,
            "cleanup": self.cleanup,
        }


@dataclass(frozen=True, slots=True)
class SkillSource:
    """A source selector before its skill contents are frozen."""

    kind: SourceKind
    selector: str
    repository_root: Path

    @classmethod
    def from_selector(cls, selector: str, repository_root: Path | str) -> SkillSource:
        kind: SourceKind = "working-tree" if selector == "working-tree" else "git-ref"
        return cls(kind=kind, selector=selector, repository_root=Path(repository_root).resolve())


@dataclass(frozen=True, slots=True)
class SnapshotFile:
    """One normalized file in a frozen source snapshot."""

    path: str
    mode: str
    size: int
    sha256: str

    def as_dict(self) -> dict[str, str | int]:
        return {
            "path": self.path,
            "mode": self.mode,
            "size": self.size,
            "sha256": self.sha256,
        }


@dataclass(frozen=True, slots=True)
class SnapshotSkill:
    """Content identity for one discovered skill."""

    name: str
    path: str
    content_digest: str
    files: tuple[str, ...]

    def as_dict(self) -> dict[str, str | list[str]]:
        return {
            "name": self.name,
            "path": self.path,
            "content_digest": self.content_digest,
            "files": list(self.files),
        }


@dataclass(frozen=True, slots=True)
class SkillSnapshot:
    """Immutable materialized skill source and its provenance manifest."""

    snapshot_root: Path
    source_kind: SourceKind
    source_selector: str
    resolved_commit: str
    dirty: bool
    release_eligible_source: bool
    content_digest: str
    snapshot_id: str
    working_tree_fingerprint: str | None
    files: tuple[SnapshotFile, ...]
    skills: tuple[SnapshotSkill, ...]

    def as_manifest(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "source_kind": self.source_kind,
            "source_selector": self.source_selector,
            "resolved_commit": self.resolved_commit,
            "dirty": self.dirty,
            "release_eligible_source": self.release_eligible_source,
            "content_digest": self.content_digest,
            "snapshot_id": self.snapshot_id,
            "working_tree_fingerprint": self.working_tree_fingerprint,
            "skills": [skill.as_dict() for skill in self.skills],
            "files": [file.as_dict() for file in self.files],
        }
