from __future__ import annotations

import asyncio
import logging
import re
import secrets
from datetime import datetime
from pathlib import Path
from typing import Any

from telegram import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ChatAction
from telegram.error import BadRequest
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from app.agents import create_adapter, get_agent_by_provider, get_default_agent
from app.database import (
    add_message,
    create_session,
    find_session_by_external,
    get_session,
    get_state,
    list_messages,
    list_sessions,
    session_message_count,
    set_external_session_id,
    update_session_title,
    update_state,
)
from app.i18n import LANGUAGES, t
from app.models import AgentSettings, AppSettings
from app.paths import telegram_proxy
from app.validation import allowed_modes

logger = logging.getLogger(__name__)
TELEGRAM_CHUNK_SIZE = 3800
WINDOWS_RESERVED_NAMES = {
    "CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))
}


def shorten(text: str, limit: int = 45) -> str:
    text = " ".join((text or "").split())
    return text if len(text) <= limit else text[: limit - 1] + "…"


def split_text(text: str, limit: int = TELEGRAM_CHUNK_SIZE) -> list[str]:
    text = (text or "").strip() or "(no textual response)"
    chunks: list[str] = []
    while len(text) > limit:
        point = text.rfind("\n", 0, limit)
        if point < limit // 2:
            point = text.rfind(" ", 0, limit)
        if point < limit // 2:
            point = limit
        chunks.append(text[:point].strip())
        text = text[point:].strip()
    if text:
        chunks.append(text)
    return chunks


def extract_message_text(raw: Any) -> str:
    if raw is None:
        return ""
    if isinstance(raw, str):
        return raw.strip()
    if isinstance(raw, (int, float, bool)):
        return str(raw)
    if isinstance(raw, dict):
        if raw.get("type") in {"tool_use", "tool_result", "thinking", "redacted_thinking"}:
            return ""
        if raw.get("type") == "text" and isinstance(raw.get("text"), str):
            return raw["text"].strip()
        for key in ("content", "message", "text"):
            if key in raw:
                result = extract_message_text(raw[key])
                if result:
                    return result
        return ""
    if isinstance(raw, (list, tuple)):
        return "\n".join(filter(None, (extract_message_text(item) for item in raw))).strip()
    for attr in ("text", "content", "message"):
        if hasattr(raw, attr):
            result = extract_message_text(getattr(raw, attr))
            if result:
                return result
    return ""


class TelegramService:
    def __init__(self, settings: AppSettings) -> None:
        self.settings = settings
        self.projects_root = Path(settings.projects_root).expanduser().resolve()
        self.allowed_users = set(settings.telegram.allowed_user_ids)
        self.run_locks: dict[int, asyncio.Lock] = {}
        builder = Application.builder().token(settings.telegram.bot_token)
        proxy = telegram_proxy()
        if proxy:
            logger.info("Using proxy for Telegram API requests: %s", proxy)
            builder = builder.proxy(proxy).get_updates_proxy(proxy)
        self.application = builder.build()
        self._register_handlers()

        # Fallback agent used when a user has not picked one yet.
        self.default_agent = get_default_agent(settings)

    def agent_for(self, user_id: int) -> AgentSettings:
        """Resolve the agent a specific user selected, falling back to the default one."""
        provider = get_state(user_id).get("selected_agent_provider")
        if provider:
            agent = get_agent_by_provider(self.settings, str(provider))
            if agent:
                return agent
        return self.default_agent

    def _register_handlers(self) -> None:
        app = self.application
        app.add_handler(CommandHandler("start", self.start_command))
        app.add_handler(CommandHandler("project", self.project_command))
        app.add_handler(CommandHandler("status", self.status_command))
        app.add_handler(CommandHandler("cancel", self.cancel_command))
        app.add_handler(CommandHandler("id", self.id_command))
        app.add_handler(CommandHandler("language", self.language_command))
        app.add_handler(CommandHandler("agent", self.agent_command))
        app.add_handler(CallbackQueryHandler(self.handle_callback))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text))
        app.add_handler(MessageHandler(filters.COMMAND, self.handle_command))
        app.add_error_handler(self.error_handler)

    async def agent_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self.is_allowed(update):
            await self.reject(update)
            return
        await self.show_agent_selection(update)

    async def show_agent_selection(self, update: Update) -> None:
        user_id = update.effective_user.id
        lang = self.lang(user_id)
        active = self.agent_for(user_id)
        keyboard = [
            [
                InlineKeyboardButton(
                    ("✅ " if agent.provider == active.provider else "") + agent.display_name,
                    callback_data=f"agent:{agent.provider}"
                )
            ]
            for agent in self.settings.agents
        ]
        keyboard.append([InlineKeyboardButton(t(lang, "btn_main_menu"), callback_data="menu:main")])
        await self.safe_edit(
            update,
            t(
                lang,
                "agent_selection_prompt",
                current_agent=active.display_name
            ),
            InlineKeyboardMarkup(keyboard)
        )

    async def handle_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self.is_allowed(update):
            await self.reject(update)
            return

        command = update.message.text.lower()
        if command == "/agent":
            await self.show_agent_selection(update)
        else:
            await update.message.reply_text(t(self.lang(update.effective_user.id), "unknown_command"))

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not update.callback_query:
            return
        if not self.is_allowed(update):
            await self.reject(update)
            return
        await update.callback_query.answer()
        data = update.callback_query.data or ""
        user_id = update.effective_user.id
        lang = self.lang(user_id)

        if data == "menu:main":
            await self.show_main(update)
        elif data == "menu:projects":
            context.user_data["path_tokens"] = {}
            await self.show_folder_browser(update, context, self.projects_root, 0, "select")
        elif data == "menu:create":
            context.user_data["path_tokens"] = {}
            await self.show_folder_browser(update, context, self.projects_root, 0, "create")
        elif data == "menu:mode":
            await self.show_modes(update)
        elif data == "menu:status":
            await self.show_status(update)
        elif data == "menu:language":
            await self.show_language_picker(update)
        elif data == "menu:agent":
            await self.show_agent_selection(update)
        elif data.startswith("lang:"):
            new_lang = data.split(":", 1)[1]
            if new_lang not in LANGUAGES:
                await update.callback_query.answer("Unsupported language.", show_alert=True)
                return
            update_state(user_id, language=new_lang)
            await update.callback_query.answer(t(new_lang, "language_set"))
            await self.show_language_picker(update)
        elif data.startswith("browse:"):
            _, purpose, token, page_text = data.split(":", 3)
            path = self.resolve_path_token(context, token)
            if not path:
                await update.callback_query.answer(t(lang, "folder_expired"), show_alert=True)
                return
            await self.show_folder_browser(update, context, path, int(page_text), purpose)
        elif data.startswith("folderaction:"):
            _, purpose, token = data.split(":", 2)
            path = self.resolve_path_token(context, token)
            if not path:
                await update.callback_query.answer(t(lang, "folder_expired_short"), show_alert=True)
                return
            if purpose == "select":
                await self.select_project(update, path)
            else:
                update_state(user_id, pending_action="folder_name", pending_path=str(path))
                await self.safe_edit(
                    update,
                    t(lang, "send_new_folder_name", path=path),
                    InlineKeyboardMarkup([[InlineKeyboardButton(t(lang, "btn_main_menu"), callback_data="menu:main")]]),
                )
        elif data.startswith("sessions:"):
            await self.show_sessions(update, context, int(data.split(":", 1)[1]))
        elif data == "session:new":
            await self.create_new_session(update)
        elif data.startswith("session:open:"):
            await self.open_session(update, int(data.rsplit(":", 1)[1]))
        elif data.startswith("history:"):
            _, session_id, page = data.split(":", 2)
            await self.show_history(update, int(session_id), page)
        elif data.startswith("mode:"):
            mode = data.split(":", 1)[1]
            agent = self.agent_for(user_id)
            if mode not in allowed_modes(agent.provider):
                await update.callback_query.answer(t(lang, "unsupported_mode"), show_alert=True)
                return
            update_state(user_id, selected_mode=mode)
            state = get_state(user_id)
            if state.get("active_session_id"):
                # The selected mode applies immediately, while the session's original mode remains in history.
                pass
            await self.show_modes(update)
        elif data.startswith("agent:"):
            provider = data.split(":", 1)[1]
            agent = get_agent_by_provider(self.settings, provider)
            if not agent:
                await update.callback_query.answer(t(lang, "agent_not_found"), show_alert=True)
                return
            update_state(user_id, selected_agent_provider=provider, selected_mode=None)
            await self.show_agent_selection(update)

    async def show_status(self, update: Update) -> None:
        user_id = update.effective_user.id
        lang = self.lang(user_id)
        state = get_state(user_id)
        project = self.active_project(user_id)
        session = get_session(int(state["active_session_id"])) if state.get("active_session_id") else None
        agent = self.agent_for(user_id)
        candidate_mode = state.get("selected_mode")
        mode = candidate_mode if candidate_mode in allowed_modes(agent.provider) else agent.default_mode
        lock = self.run_locks.get(user_id)
        if lock and lock.locked():
            execution_status = t(lang, "status_running")
        elif session:
            execution_status = t(lang, "status_ready")
        elif project:
            execution_status = t(lang, "status_project_selected")
        else:
            execution_status = t(lang, "status_waiting_project")
        last_activity = (session or {}).get("updated_at") or state.get("updated_at")
        status_label = t(lang, "status_agent_status_label", agent=agent.display_name)
        text = "\n".join(
            [
                t(lang, "status_title"),
                "",
                t(lang, "status_selected_project", value=project or t(lang, "status_not_selected")),
                t(lang, "status_active_session", value=(session or {}).get("title", t(lang, "status_not_selected"))),
                t(lang, "status_last_activity", value=self.format_activity_time(last_activity, lang)),
                f"{status_label}: {execution_status}",
                "",
                t(lang, "status_agent_line", agent=agent.display_name, provider=agent.provider),
                t(lang, "status_mode_line", mode=mode),
            ]
        )
        keyboard: list[list[InlineKeyboardButton]] = []
        if project:
            keyboard.append([InlineKeyboardButton(t(lang, "btn_project_sessions"), callback_data="sessions:0")])
        else:
            keyboard.append([InlineKeyboardButton(t(lang, "menu_choose_project"), callback_data="menu:projects")])
        keyboard.append([InlineKeyboardButton(t(lang, "btn_main_menu"), callback_data="menu:main")])
        keyboard.append([InlineKeyboardButton(t(lang, "btn_agent_selection"), callback_data="menu:agent")])
        await self.safe_edit(update, text, InlineKeyboardMarkup(keyboard))

    async def start(self) -> None:
        await self.application.initialize()
        for lang in LANGUAGES:
            await self.application.bot.set_my_commands(
                [
                    BotCommand("start", t(lang, "cmd_start")),
                    BotCommand("project", t(lang, "cmd_project")),
                    BotCommand("status", t(lang, "cmd_status")),
                    BotCommand("cancel", t(lang, "cmd_cancel")),
                    BotCommand("language", t(lang, "cmd_language")),
                    BotCommand("agent", t(lang, "cmd_agent")),
                    BotCommand("id", t(lang, "cmd_id")),
                ],
                language_code=lang,
            )
        await self.application.start()
        if self.application.updater is None:
            raise RuntimeError("Telegram updater is unavailable.")
        await self.application.updater.start_polling(drop_pending_updates=True)

    async def stop(self) -> None:
        if self.application.updater and self.application.updater.running:
            await self.application.updater.stop()
        if self.application.running:
            await self.application.stop()
        await self.application.shutdown()

    def is_allowed(self, update: Update) -> bool:
        return bool(update.effective_user and update.effective_user.id in self.allowed_users)

    def lang(self, user_id: int) -> str:
        value = get_state(user_id).get("language")
        return value if value in LANGUAGES else "en"

    async def reject(self, update: Update) -> None:
        lang = self.lang(update.effective_user.id) if update.effective_user else "en"
        if update.callback_query:
            await update.callback_query.answer(t(lang, "access_denied_alert"), show_alert=True)
        elif update.effective_message:
            await update.effective_message.reply_text(t(lang, "access_denied_message"))

    def inside_root(self, path: Path) -> bool:
        try:
            resolved = path.expanduser().resolve()
        except OSError:
            return False
        return resolved == self.projects_root or self.projects_root in resolved.parents

    def active_project(self, user_id: int) -> Path | None:
        value = get_state(user_id).get("active_project_path")
        if not value:
            return None
        path = Path(str(value)).expanduser().resolve()
        if not path.is_dir() or not self.inside_root(path):
            return None
        return path

    def create_path_token(self, context: ContextTypes.DEFAULT_TYPE, path: Path) -> str:
        tokens = context.user_data.setdefault("path_tokens", {})
        if len(tokens) > 300:
            tokens.clear()
        token = secrets.token_urlsafe(6)
        tokens[token] = str(path.resolve())
        return token

    def resolve_path_token(self, context: ContextTypes.DEFAULT_TYPE, token: str) -> Path | None:
        value = context.user_data.get("path_tokens", {}).get(token)
        if not value:
            return None
        path = Path(value).expanduser().resolve()
        if not path.is_dir() or not self.inside_root(path):
            return None
        return path

    async def safe_edit(
        self,
        update: Update,
        text: str,
        markup: InlineKeyboardMarkup | None = None,
    ) -> None:
        if update.callback_query:
            try:
                await update.callback_query.edit_message_text(text=text, reply_markup=markup)
                return
            except BadRequest as exc:
                if "Message is not modified" in str(exc):
                    return
        if update.effective_message:
            await update.effective_message.reply_text(text=text, reply_markup=markup)

    async def send_long(self, chat_id: int, text: str) -> None:
        for chunk in split_text(text):
            await self.application.bot.send_message(chat_id=chat_id, text=chunk)

    def main_menu(self, lang: str) -> InlineKeyboardMarkup:
        """Return the exact top-level navigation flow.

        Session creation and mode selection deliberately live inside the selected
        project's session page, not in the main menu.
        """
        return InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(t(lang, "menu_choose_project"), callback_data="menu:projects")],
                [InlineKeyboardButton(t(lang, "menu_create_folder"), callback_data="menu:create")],
                [InlineKeyboardButton(t(lang, "menu_status"), callback_data="menu:status")],
                [InlineKeyboardButton(t(lang, "menu_language"), callback_data="menu:language")],
            ]
        )

    async def show_main(self, update: Update) -> None:
        lang = self.lang(update.effective_user.id)
        await self.safe_edit(update, t(lang, "main_text"), self.main_menu(lang))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self.is_allowed(update):
            await self.reject(update)
            return
        await self.show_main(update)

    async def id_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.effective_message and update.effective_user:
            lang = self.lang(update.effective_user.id)
            await update.effective_message.reply_text(t(lang, "your_user_id", id=update.effective_user.id))

    async def project_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self.is_allowed(update):
            await self.reject(update)
            return
        await self.show_folder_browser(update, context, self.projects_root, 0, "select")

    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self.is_allowed(update):
            await self.reject(update)
            return
        await self.show_status(update)

    async def cancel_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self.is_allowed(update):
            await self.reject(update)
            return
        lang = self.lang(update.effective_user.id)
        update_state(update.effective_user.id, pending_action=None, pending_path=None)
        await update.effective_message.reply_text(t(lang, "input_cancelled"), reply_markup=self.main_menu(lang))

    async def language_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self.is_allowed(update):
            await self.reject(update)
            return
        await self.show_language_picker(update)

    async def show_language_picker(self, update: Update) -> None:
        lang = self.lang(update.effective_user.id)
        keyboard = [
            [
                InlineKeyboardButton(("✅ " if lang == "en" else "") + t(lang, "btn_lang_en"), callback_data="lang:en"),
                InlineKeyboardButton(("✅ " if lang == "fa" else "") + t(lang, "btn_lang_fa"), callback_data="lang:fa"),
            ],
            [InlineKeyboardButton(t(lang, "btn_main_menu"), callback_data="menu:main")],
        ]
        await self.safe_edit(update, t(lang, "language_prompt"), InlineKeyboardMarkup(keyboard))

    async def show_folder_browser(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        current: Path,
        page: int,
        purpose: str,
    ) -> None:
        lang = self.lang(update.effective_user.id)
        current = current.resolve()
        if not self.inside_root(current):
            current = self.projects_root
        try:
            folders = sorted(
                [item.resolve() for item in current.iterdir() if item.is_dir() and not item.name.startswith(".")],
                key=lambda item: item.name.casefold(),
            )
        except (OSError, PermissionError):
            folders = []
        size = self.settings.folder_page_size
        pages = max(1, (len(folders) + size - 1) // size)
        page = max(0, min(page, pages - 1))
        visible = folders[page * size : (page + 1) * size]
        keyboard: list[list[InlineKeyboardButton]] = []
        for folder in visible:
            token = self.create_path_token(context, folder)
            keyboard.append(
                [InlineKeyboardButton(f"📁 {shorten(folder.name)}", callback_data=f"browse:{purpose}:{token}:0")]
            )
        current_token = self.create_path_token(context, current)
        nav: list[InlineKeyboardButton] = []
        if page > 0:
            nav.append(InlineKeyboardButton(t(lang, "btn_previous"), callback_data=f"browse:{purpose}:{current_token}:{page-1}"))
        if page < pages - 1:
            nav.append(InlineKeyboardButton(t(lang, "btn_next"), callback_data=f"browse:{purpose}:{current_token}:{page+1}"))
        if nav:
            keyboard.append(nav)
        action_text = t(lang, "btn_select_folder") if purpose == "select" else t(lang, "btn_create_folder_here")
        keyboard.append([InlineKeyboardButton(action_text, callback_data=f"folderaction:{purpose}:{current_token}")])
        if current != self.projects_root:
            parent_token = self.create_path_token(context, current.parent)
            keyboard.append([InlineKeyboardButton(t(lang, "btn_parent_folder"), callback_data=f"browse:{purpose}:{parent_token}:0")])
        keyboard.append([InlineKeyboardButton(t(lang, "btn_main_menu"), callback_data="menu:main")])
        try:
            label = str(current.relative_to(self.projects_root))
            label = self.projects_root.name if label == "." else f"{self.projects_root.name} / {label}"
        except ValueError:
            label = str(current)
        await self.safe_edit(
            update,
            t(lang, "folder_browser_text", label=label, count=len(folders), page=page + 1, pages=pages),
            InlineKeyboardMarkup(keyboard),
        )

    async def select_project(self, update: Update, path: Path) -> None:
        user_id = update.effective_user.id
        update_state(user_id, active_project_path=str(path), active_session_id=None, pending_action=None, pending_path=None)
        await self.show_sessions(update, None, 0)

    async def sync_claude_sessions(self, user_id: int, project: Path) -> None:
        agent = self.agent_for(user_id)
        if agent.provider != "claude":
            return
        try:
            from claude_agent_sdk import list_sessions as sdk_list_sessions

            external_sessions = await asyncio.to_thread(
                sdk_list_sessions,
                directory=str(project),
                limit=None,
                include_worktrees=False,
            )
        except Exception as exc:
            logger.info("Could not discover external Claude sessions: %s", exc)
            return
        for item in external_sessions:
            external_id = str(getattr(item, "session_id", "") or "")
            if not external_id or find_session_by_external(user_id, "claude", external_id):
                continue
            title = shorten(
                str(
                    getattr(item, "custom_title", None)
                    or getattr(item, "summary", None)
                    or getattr(item, "first_prompt", None)
                    or external_id
                ),
                80,
            )
            create_session(
                user_id,
                str(project),
                "claude",
                title,
                agent.default_mode,
                external_id,
            )

    async def show_sessions(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE | None,
        page: int,
    ) -> None:
        user_id = update.effective_user.id
        lang = self.lang(user_id)
        project = self.active_project(user_id)
        if not project:
            await self.safe_edit(update, t(lang, "choose_project_first"), self.main_menu(lang))
            return
        await self.sync_claude_sessions(user_id, project)
        agent = self.agent_for(user_id)
        sessions = list_sessions(user_id, str(project), agent.provider)
        size = self.settings.session_page_size
        pages = max(1, (len(sessions) + size - 1) // size)
        page = max(0, min(page, pages - 1))
        visible = sessions[page * size : (page + 1) * size]
        keyboard: list[list[InlineKeyboardButton]] = [
            [InlineKeyboardButton(t(lang, "btn_new_session"), callback_data="session:new")]
        ]
        lines = [
            t(lang, "sessions_project_line", name=project.name),
            str(project),
            "",
            t(lang, "sessions_agent_line", agent=agent.display_name),
        ]
        if not visible:
            lines.extend(["", t(lang, "sessions_none")])
        for index, session in enumerate(visible, start=page * size + 1):
            lines.append(f"\n{index}. {session['title']}")
            keyboard.append(
                [InlineKeyboardButton(f"💬 {shorten(session['title'])}", callback_data=f"session:open:{session['id']}")]
            )
        nav: list[InlineKeyboardButton] = []
        if page > 0:
            nav.append(InlineKeyboardButton(t(lang, "btn_previous"), callback_data=f"sessions:{page-1}"))
        if page < pages - 1:
            nav.append(InlineKeyboardButton(t(lang, "btn_next"), callback_data=f"sessions:{page+1}"))
        if nav:
            keyboard.append(nav)
        keyboard.extend(
            [
                [InlineKeyboardButton(t(lang, "btn_agent_mode"), callback_data="menu:mode")],
                [InlineKeyboardButton(t(lang, "btn_change_project"), callback_data="menu:projects")],
                [InlineKeyboardButton(t(lang, "btn_main_menu"), callback_data="menu:main")],
            ]
        )
        await self.safe_edit(update, "\n".join(lines), InlineKeyboardMarkup(keyboard))

    async def create_new_session(self, update: Update) -> None:
        user_id = update.effective_user.id
        lang = self.lang(user_id)
        project = self.active_project(user_id)
        if not project:
            await self.safe_edit(update, t(lang, "choose_project_first"), self.main_menu(lang))
            return
        state = get_state(user_id)
        agent = self.agent_for(user_id)
        candidate_mode = state.get("selected_mode")
        mode = candidate_mode if candidate_mode in allowed_modes(agent.provider) else agent.default_mode
        session_id = create_session(
            user_id,
            str(project),
            agent.provider,
            "New session",
            str(mode),
        )
        update_state(user_id, active_session_id=session_id)
        await self.safe_edit(
            update,
            t(lang, "new_session_created", project=project.name, mode=mode),
            InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(t(lang, "btn_change_mode"), callback_data="menu:mode")],
                    [InlineKeyboardButton(t(lang, "btn_project_sessions"), callback_data="sessions:0")],
                ]
            ),
        )

    async def import_claude_history(self, local_session_id: int, external_id: str, project: Path) -> None:
        if session_message_count(local_session_id) > 0:
            return
        try:
            from claude_agent_sdk import get_session_messages

            rows = await asyncio.to_thread(
                get_session_messages,
                external_id,
                directory=str(project),
                limit=None,
                offset=0,
            )
        except Exception as exc:
            logger.info("Could not import Claude history: %s", exc)
            return
        for item in rows:
            role = str(getattr(item, "type", ""))
            if role not in {"user", "assistant"}:
                continue
            text = extract_message_text(getattr(item, "message", None))
            if text:
                add_message(local_session_id, role, text)

    async def open_session(self, update: Update, local_session_id: int) -> None:
        session = get_session(local_session_id)
        if not session or session["user_id"] != update.effective_user.id:
            lang = self.lang(update.effective_user.id)
            await update.callback_query.answer(t(lang, "session_not_found"), show_alert=True)
            return
        project = Path(session["project_path"]).resolve()
        update_state(
            update.effective_user.id,
            active_project_path=str(project),
            active_session_id=local_session_id,
            selected_mode=session["mode"],
        )
        if session["provider"] == "claude" and session.get("external_session_id"):
            await self.import_claude_history(local_session_id, session["external_session_id"], project)
        await self.show_history(update, local_session_id, "latest")

    async def show_history(self, update: Update, local_session_id: int, page_value: str) -> None:
        lang = self.lang(update.effective_user.id)
        agent = self.agent_for(update.effective_user.id)
        session = get_session(local_session_id)
        if not session:
            await self.safe_edit(update, t(lang, "session_not_found"), self.main_menu(lang))
            return
        messages = list_messages(local_session_id)
        size = self.settings.history_page_size
        pages = max(1, (len(messages) + size - 1) // size)
        page = pages - 1 if page_value == "latest" else max(0, min(int(page_value), pages - 1))
        visible = messages[page * size : (page + 1) * size]
        lines = [t(lang, "history_session_line", title=session["title"]), t(lang, "history_mode_line", mode=session["mode"]), ""]
        if not visible:
            lines.append(t(lang, "history_no_messages"))
        for message in visible:
            role = t(lang, "role_you") if message["role"] == "user" else agent.display_name
            lines.append(f"{role}:\n{message['content']}\n")
        nav: list[InlineKeyboardButton] = []
        if page > 0:
            nav.append(InlineKeyboardButton(t(lang, "btn_older"), callback_data=f"history:{local_session_id}:{page-1}"))
        if page < pages - 1:
            nav.append(InlineKeyboardButton(t(lang, "btn_newer"), callback_data=f"history:{local_session_id}:{page+1}"))
        keyboard: list[list[InlineKeyboardButton]] = []
        if nav:
            keyboard.append(nav)
        keyboard.extend(
            [
                [InlineKeyboardButton(t(lang, "btn_change_mode"), callback_data="menu:mode")],
                [InlineKeyboardButton(t(lang, "btn_project_sessions"), callback_data="sessions:0")],
                [InlineKeyboardButton(t(lang, "btn_main_menu"), callback_data="menu:main")],
            ]
        )
        text = "\n".join(lines)
        if len(text) > TELEGRAM_CHUNK_SIZE:
            text = text[: TELEGRAM_CHUNK_SIZE - 80] + t(lang, "history_shortened")
        await self.safe_edit(update, text, InlineKeyboardMarkup(keyboard))

    async def show_modes(self, update: Update) -> None:
        user_id = update.effective_user.id
        lang = self.lang(user_id)
        state = get_state(user_id)
        agent = self.agent_for(user_id)
        candidate_mode = state.get("selected_mode")
        current = candidate_mode if candidate_mode in allowed_modes(agent.provider) else agent.default_mode
        keyboard = [
            [InlineKeyboardButton(("✅ " if mode == current else "") + mode, callback_data=f"mode:{mode}")]
            for mode in allowed_modes(agent.provider)
        ]
        if state.get("active_session_id"):
            back_callback = f"history:{int(state['active_session_id'])}:latest"
            back_text = t(lang, "back_active_session")
        elif self.active_project(user_id):
            back_callback = "sessions:0"
            back_text = t(lang, "btn_project_sessions")
        else:
            back_callback = "menu:main"
            back_text = t(lang, "btn_main_menu")
        keyboard.append([InlineKeyboardButton(back_text, callback_data=back_callback)])
        await self.safe_edit(
            update,
            t(
                lang,
                "modes_header",
                agent=agent.display_name,
                provider=agent.provider,
                mode=current,
            ),
            InlineKeyboardMarkup(keyboard),
        )

    @staticmethod
    def format_activity_time(value: str | None, lang: str) -> str:
        if not value:
            return t(lang, "no_activity_yet")
        try:
            timestamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
            return timestamp.astimezone().strftime("%Y-%m-%d %H:%M %Z")
        except (TypeError, ValueError):
            return str(value)

    def validate_folder_name(self, raw: str, lang: str) -> tuple[bool, str]:
        name = raw.strip()
        if not name:
            return False, t(lang, "folder_name_empty")
        if len(name) > 100:
            return False, t(lang, "folder_name_too_long")
        if name in {".", ".."} or "/" in name or "\\" in name:
            return False, t(lang, "folder_name_path")
        if re.search(r'[<>:"|?*]', name):
            return False, t(lang, "folder_name_invalid_char")
        if name.endswith((" ", ".")):
            return False, t(lang, "folder_name_trailing")
        if name.split(".", 1)[0].upper() in WINDOWS_RESERVED_NAMES:
            return False, t(lang, "folder_name_reserved")
        return True, name

    async def handle_folder_name(self, update: Update, parent: Path, raw: str) -> None:
        lang = self.lang(update.effective_user.id)
        valid, result = self.validate_folder_name(raw, lang)
        if not valid:
            await update.effective_message.reply_text(t(lang, "send_another_name", result=result))
            return
        new_path = (parent / result).resolve()
        if not self.inside_root(new_path):
            await update.effective_message.reply_text(t(lang, "outside_root"))
            return
        if new_path.exists():
            await update.effective_message.reply_text(t(lang, "already_exists"))
            return
        try:
            new_path.mkdir()
        except OSError as exc:
            await update.effective_message.reply_text(t(lang, "cannot_create_folder", error=exc))
            return
        update_state(
            update.effective_user.id,
            active_project_path=str(new_path),
            active_session_id=None,
            pending_action=None,
            pending_path=None,
        )
        await update.effective_message.reply_text(t(lang, "folder_created", path=new_path))
        await self.show_sessions(update, None, 0)

    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self.is_allowed(update):
            await self.reject(update)
            return
        if not update.effective_message or not update.effective_message.text:
            return
        user_id = update.effective_user.id
        lang = self.lang(user_id)
        state = get_state(user_id)
        if state.get("pending_action") == "folder_name" and state.get("pending_path"):
            await self.handle_folder_name(update, Path(state["pending_path"]), update.effective_message.text)
            return
        project = self.active_project(user_id)
        if not project:
            await update.effective_message.reply_text(t(lang, "choose_project_first"), reply_markup=self.main_menu(lang))
            return
        local_session_id = state.get("active_session_id")
        if not local_session_id:
            await update.effective_message.reply_text(
                t(lang, "choose_session_first"),
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(t(lang, "btn_project_sessions"), callback_data="sessions:0")]]
                ),
            )
            return
        session = get_session(int(local_session_id))
        if not session:
            update_state(user_id, active_session_id=None)
            await update.effective_message.reply_text(t(lang, "active_session_gone"))
            return
        prompt = update.effective_message.text.strip()
        if not prompt:
            return
        lock = self.run_locks.setdefault(user_id, asyncio.Lock())
        if lock.locked():
            await update.effective_message.reply_text(t(lang, "previous_still_running"))
            return
        async with lock:
            if session["title"] == "New session":
                update_session_title(session["id"], shorten(prompt, 80))
            add_message(session["id"], "user", prompt)
            await self.application.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)
            # The session keeps the agent it was created with, so a provider switch cannot
            # resume a session against a CLI that never created it.
            agent = get_agent_by_provider(self.settings, session["provider"]) or self.agent_for(user_id)
            candidate_mode = state.get("selected_mode")
            fallback_mode = session["mode"] or agent.default_mode
            mode = candidate_mode if candidate_mode in allowed_modes(agent.provider) else fallback_mode
            if mode not in allowed_modes(agent.provider):
                mode = agent.default_mode
            adapter = create_adapter(agent)
            try:
                reply = await adapter.send(
                    prompt=prompt,
                    project_path=project,
                    mode=str(mode),
                    external_session_id=session.get("external_session_id"),
                )
            except Exception as exc:
                logger.exception("Agent request failed")
                await update.effective_message.reply_text(
                    t(lang, "agent_request_failed", error_type=type(exc).__name__, error=exc)
                )
                return
            if reply.external_session_id and not session.get("external_session_id"):
                set_external_session_id(session["id"], reply.external_session_id)
            add_message(session["id"], "assistant", reply.text)
            await self.send_long(update.effective_chat.id, reply.text)

    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        logger.exception("Unhandled Telegram update error", exc_info=context.error)
