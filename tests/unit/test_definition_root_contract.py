from pathlib import Path


def test_artifact_creation_uses_configured_root():
    reference = (
        Path(__file__).resolve().parents[2]
        / "skills/software-idea-to-project/references/artifacts.md"
    ).read_text()
    session_directory = reference.split("## Session directory\n", 1)[1].split("\n## ", 1)[0]
    assert "<definition_root>/<slug>/" in session_directory
    assert "[session-state.md](session-state.md)" in session_directory
    assert "docs/software-design/<slug>/" not in session_directory


def test_artifact_discovery_does_not_force_default_root():
    reference = (
        Path(__file__).resolve().parents[2]
        / "skills/software-idea-to-project/references/artifacts.md"
    ).read_text()
    session_directory = reference.split("## Session directory\n", 1)[1].split("\n## ", 1)[0]
    assert (
        "existing sessions keep their recorded root or current legacy location" in session_directory
    )
    assert "Never move or copy a session" in session_directory
    assert "wait for user selection" in session_directory
    assert "inspect `docs/software-design/`" not in session_directory
