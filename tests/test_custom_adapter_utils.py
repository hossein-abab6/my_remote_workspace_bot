from app.agents.utils import extract_dot_path, substitute_args


def test_substitute_args() -> None:
    assert substitute_args(
        ["resume", "{session_id}", "{prompt}"], "hello", "abc"
    ) == ["resume", "abc", "hello"]


def test_extract_dot_path() -> None:
    value = {"result": {"messages": [{"text": "done"}]}}
    assert extract_dot_path(value, "result.messages.0.text") == "done"
