from __future__ import annotations

import json
import os
import stat
from pathlib import Path

import pytest

from devquitect_quality.codex_adapter import _stage_auth_cache
from devquitect_quality.fixtures import ATTEMPT_MARKER, cleanup_stale_attempts


def test_staging_is_owner_only_from_creation_and_cleans_partial_copy(
    tmp_path: Path, monkeypatch
) -> None:
    source = tmp_path / "auth.json"
    source.write_text('{"token":"secret"}', encoding="utf-8")
    source.chmod(0o600)
    codex_home = tmp_path / "codex-home"
    codex_home.mkdir(mode=0o700)
    observed: dict[str, int] = {}

    def copyfileobj(source_handle, target_handle) -> None:
        observed["mode"] = stat.S_IMODE(os.fstat(target_handle.fileno()).st_mode)
        raise OSError("simulated copy failure")

    monkeypatch.setattr("devquitect_quality.codex_adapter.shutil.copyfileobj", copyfileobj)
    with pytest.raises(OSError, match="simulated copy failure"):
        _stage_auth_cache(source, codex_home)

    assert observed["mode"] == 0o600
    assert not (codex_home / "auth.json").exists()


def test_staging_rejects_symlink_and_group_accessible_sources(tmp_path: Path) -> None:
    codex_home = tmp_path / "codex-home"
    codex_home.mkdir(mode=0o700)
    source = tmp_path / "auth.json"
    source.write_text("secret", encoding="utf-8")
    source.chmod(0o640)
    with pytest.raises(ValueError, match="group or others"):
        _stage_auth_cache(source, codex_home)

    source.chmod(0o600)
    symlink = tmp_path / "auth-link.json"
    symlink.symlink_to(source)
    with pytest.raises((OSError, ValueError)):
        _stage_auth_cache(symlink, codex_home)


def test_stale_cleanup_requires_marker_age_ownership_and_dead_process(tmp_path: Path) -> None:
    parent = tmp_path / "attempts"
    parent.mkdir(mode=0o700)
    now = 10_000.0

    stale = parent / "attempt-stale"
    stale.mkdir(mode=0o700)
    (stale / ATTEMPT_MARKER).write_text(
        json.dumps(
            {
                "schema_version": 1,
                "attempt_id": stale.name,
                "pid": 2**30,
                "created_at": now - 100,
            }
        ),
        encoding="utf-8",
    )
    (stale / ATTEMPT_MARKER).chmod(0o600)

    active = parent / "attempt-active"
    active.mkdir(mode=0o700)
    (active / ATTEMPT_MARKER).write_text(
        json.dumps(
            {
                "schema_version": 1,
                "attempt_id": active.name,
                "pid": os.getpid(),
                "created_at": now - 100,
            }
        ),
        encoding="utf-8",
    )
    (active / ATTEMPT_MARKER).chmod(0o600)

    ambiguous = parent / "attempt-ambiguous"
    ambiguous.mkdir(mode=0o700)
    (ambiguous / ATTEMPT_MARKER).write_text("not json", encoding="utf-8")
    (ambiguous / ATTEMPT_MARKER).chmod(0o600)
    source_cache = parent / "auth.json"
    source_cache.write_text("must remain", encoding="utf-8")

    removed = cleanup_stale_attempts(parent, max_age_seconds=10, now=now)

    assert removed == (stale,)
    assert not stale.exists()
    assert active.exists()
    assert ambiguous.exists()
    assert source_cache.exists()
