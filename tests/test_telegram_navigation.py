from pathlib import Path


def test_main_menu_has_only_top_level_project_actions() -> None:
    source = (Path(__file__).parents[1] / "app" / "telegram" / "service.py").read_text(
        encoding="utf-8"
    )
    start = source.index("    def main_menu")
    end = source.index("    async def show_main", start)
    block = source[start:end]

    # Button labels moved behind i18n keys, so assert on the keys and callbacks.
    assert '"menu_choose_project"' in block
    assert '"menu_create_folder"' in block
    assert '"menu_status"' in block
    assert '"btn_new_session"' not in block
    assert '"btn_agent_mode"' not in block
    assert 'callback_data="menu:mode"' not in block
