from pathlib import Path

from app import database


def test_session_round_trip(tmp_path: Path, monkeypatch) -> None:
    db_path = tmp_path / "test.db"
    monkeypatch.setattr(database, "database_path", lambda: db_path)
    database.initialize_database()
    session_id = database.create_session(
        user_id=1,
        project_path=str(tmp_path),
        provider="claude",
        title="Test session",
        mode="plan",
    )
    database.add_message(session_id, "user", "hello")
    database.add_message(session_id, "assistant", "hi")
    session = database.get_session(session_id)
    messages = database.list_messages(session_id)
    assert session["title"] == "Test session"
    assert [item["role"] for item in messages] == ["user", "assistant"]
