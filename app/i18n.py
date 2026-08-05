from __future__ import annotations

DEFAULT_LANG = "en"
LANGUAGES = ("en", "fa")

_STRINGS: dict[str, dict[str, str]] = {
    "access_denied_alert": {"en": "Access denied.", "fa": "دسترسی رد شد."},
    "access_denied_message": {
        "en": "Access denied. Ask the bot owner to add your numeric Telegram user ID in the local dashboard.",
        "fa": "دسترسی رد شد. از مالک ربات بخواهید شناسه عددی تلگرام شما را در داشبورد محلی اضافه کند.",
    },
    "menu_choose_project": {"en": "📁 Choose project", "fa": "📁 انتخاب پروژه"},
    "menu_create_folder": {"en": "➕ Create folder", "fa": "➕ ساخت پوشه"},
    "menu_status": {"en": "📌 Current status", "fa": "📌 وضعیت فعلی"},
    "menu_language": {"en": "🌐 Language", "fa": "🌐 زبان"},
    "main_text": {
        "en": "My Remote Workspace Bot\n\nChoose a project or create a folder. After selecting a project, you can start a new session or continue an earlier one.",
        "fa": "ربات فضای کاری ریموت من\n\nیک پروژه انتخاب کنید یا پوشه‌ای بسازید. پس از انتخاب پروژه می‌توانید نشست جدیدی شروع کنید یا یکی از نشست‌های قبلی را ادامه دهید.",
    },
    "your_user_id": {"en": "Your Telegram user ID: {id}", "fa": "شناسه تلگرام شما: {id}"},
    "input_cancelled": {"en": "Current input was cancelled.", "fa": "ورودی فعلی لغو شد."},
    "btn_previous": {"en": "⬅️ Previous", "fa": "⬅️ قبلی"},
    "btn_next": {"en": "Next ➡️", "fa": "بعدی ➡️"},
    "btn_select_folder": {"en": "✅ Select this folder", "fa": "✅ انتخاب این پوشه"},
    "btn_create_folder_here": {"en": "➕ Create folder here", "fa": "➕ ساخت پوشه اینجا"},
    "btn_parent_folder": {"en": "⬆️ Parent folder", "fa": "⬆️ پوشه والد"},
    "btn_main_menu": {"en": "🔙 Main menu", "fa": "🔙 منوی اصلی"},
    "folder_browser_text": {
        "en": "Folder browser\n\nCurrent: {label}\nSubfolders: {count}\nPage: {page}/{pages}",
        "fa": "مرورگر پوشه\n\nمسیر فعلی: {label}\nزیرپوشه‌ها: {count}\nصفحه: {page}/{pages}",
    },
    "choose_project_first": {"en": "Choose a project first.", "fa": "ابتدا یک پروژه انتخاب کنید."},
    "btn_new_session": {"en": "🆕 New session", "fa": "🆕 نشست جدید"},
    "sessions_project_line": {"en": "Project: {name}", "fa": "پروژه: {name}"},
    "sessions_agent_line": {"en": "Agent: {agent}", "fa": "ایجنت: {agent}"},
    "sessions_none": {"en": "No sessions found for this project.", "fa": "برای این پروژه نشستی یافت نشد."},
    "btn_agent_mode": {"en": "🎛 Agent & mode", "fa": "🎛 ایجنت و حالت"},
    "btn_change_project": {"en": "📁 Change project", "fa": "📁 تغییر پروژه"},
    "new_session_created": {
        "en": "New session created for {project}.\nMode: {mode}\n\nSend your first message.",
        "fa": "نشست جدید برای {project} ساخته شد.\nحالت: {mode}\n\nپیام اول خود را ارسال کنید.",
    },
    "btn_change_mode": {"en": "🎛 Change mode", "fa": "🎛 تغییر حالت"},
    "btn_project_sessions": {"en": "💬 Project sessions", "fa": "💬 نشست‌های پروژه"},
    "session_not_found": {"en": "Session not found.", "fa": "نشست یافت نشد."},
    "history_session_line": {"en": "Session: {title}", "fa": "نشست: {title}"},
    "history_mode_line": {"en": "Mode: {mode}", "fa": "حالت: {mode}"},
    "history_no_messages": {
        "en": "No messages yet. Send a message to begin.",
        "fa": "هنوز پیامی نیست. برای شروع پیام بفرستید.",
    },
    "role_you": {"en": "You", "fa": "شما"},
    "btn_older": {"en": "⬅️ Older", "fa": "⬅️ قدیمی‌تر"},
    "btn_newer": {"en": "Newer ➡️", "fa": "جدیدتر ➡️"},
    "history_shortened": {
        "en": "\n\n[This page was shortened for Telegram.]",
        "fa": "\n\n[این صفحه برای تلگرام کوتاه شد.]",
    },
    "modes_header": {
        "en": "Agent: {agent}\nProvider: {provider}\nCurrent mode: {mode}\n\nChoose the mode used for the current conversation and future sessions.",
        "fa": "ایجنت: {agent}\nارائه‌دهنده: {provider}\nحالت فعلی: {mode}\n\nحالتی را انتخاب کنید که برای گفتگوی فعلی و نشست‌های بعدی استفاده شود.",
    },
    "back_active_session": {"en": "🔙 Active session", "fa": "🔙 نشست فعال"},
    "no_activity_yet": {"en": "No activity yet", "fa": "هنوز فعالیتی نیست"},
    "status_title": {"en": "Current status", "fa": "وضعیت فعلی"},
    "status_selected_project": {"en": "Selected project: {value}", "fa": "پروژه انتخاب‌شده: {value}"},
    "status_not_selected": {"en": "not selected", "fa": "انتخاب نشده"},
    "status_active_session": {"en": "Active session: {value}", "fa": "نشست فعال: {value}"},
    "status_last_activity": {"en": "Last activity: {value}", "fa": "آخرین فعالیت: {value}"},
    "status_agent_status_label": {"en": "{agent} status", "fa": "وضعیت {agent}"},
    "status_agent_line": {"en": "Agent: {agent} ({provider})", "fa": "ایجنت: {agent} ({provider})"},
    "status_mode_line": {"en": "Mode: {mode}", "fa": "حالت: {mode}"},
    "status_running": {"en": "Running a request", "fa": "در حال اجرای یک درخواست"},
    "status_ready": {"en": "Ready for the next message", "fa": "آماده برای پیام بعدی"},
    "status_project_selected": {
        "en": "Project selected; choose or create a session",
        "fa": "پروژه انتخاب شد؛ یک نشست انتخاب یا بسازید",
    },
    "status_waiting_project": {"en": "Waiting for a project", "fa": "در انتظار انتخاب پروژه"},
    "folder_name_empty": {"en": "Folder name cannot be empty.", "fa": "نام پوشه نمی‌تواند خالی باشد."},
    "folder_name_too_long": {
        "en": "Folder name must be 100 characters or fewer.",
        "fa": "نام پوشه باید حداکثر ۱۰۰ کاراکتر باشد.",
    },
    "folder_name_path": {"en": "Enter one folder name, not a path.", "fa": "فقط یک نام پوشه وارد کنید، نه یک مسیر."},
    "folder_name_invalid_char": {
        "en": 'Folder name contains an invalid Windows character: <>:"|?*',
        "fa": 'نام پوشه شامل کاراکتر نامعتبر ویندوز است: <>:"|?*',
    },
    "folder_name_trailing": {
        "en": "Folder name cannot end with a space or dot.",
        "fa": "نام پوشه نمی‌تواند با فاصله یا نقطه پایان یابد.",
    },
    "folder_name_reserved": {
        "en": "That folder name is reserved by Windows.",
        "fa": "این نام پوشه توسط ویندوز رزرو شده است.",
    },
    "send_another_name": {
        "en": "{result}\nSend another name or /cancel.",
        "fa": "{result}\nنام دیگری بفرستید یا /cancel را بزنید.",
    },
    "outside_root": {
        "en": "The requested path is outside the allowed projects root.",
        "fa": "مسیر درخواستی خارج از ریشه مجاز پروژه‌هاست.",
    },
    "already_exists": {
        "en": "A file or folder with that name already exists. Send another name or /cancel.",
        "fa": "فایل یا پوشه‌ای با این نام از قبل وجود دارد. نام دیگری بفرستید یا /cancel را بزنید.",
    },
    "cannot_create_folder": {"en": "Cannot create folder: {error}", "fa": "امکان ساخت پوشه نبود: {error}"},
    "folder_created": {"en": "Folder created and selected:\n{path}", "fa": "پوشه ساخته و انتخاب شد:\n{path}"},
    "choose_session_first": {
        "en": "Choose an existing session or create a new session first.",
        "fa": "ابتدا یک نشست موجود را انتخاب کنید یا نشست جدیدی بسازید.",
    },
    "active_session_gone": {"en": "The active session no longer exists.", "fa": "نشست فعال دیگر وجود ندارد."},
    "previous_still_running": {
        "en": "Your previous agent request is still running. Wait for its response before sending another message.",
        "fa": "درخواست قبلی هنوز در حال اجراست. قبل از ارسال پیام جدید منتظر پاسخ بمانید.",
    },
    "agent_request_failed": {
        "en": "Agent request failed:\n{error_type}: {error}\n\nCheck the local dashboard and agent authentication.",
        "fa": "درخواست ایجنت شکست خورد:\n{error_type}: {error}\n\nداشبورد محلی و احراز هویت ایجنت را بررسی کنید.",
    },
    "send_new_folder_name": {
        "en": "Send the name for the new folder inside:\n{path}\n\nSend /cancel to stop.",
        "fa": "نام پوشه جدید داخل مسیر زیر را بفرستید:\n{path}\n\nبرای توقف /cancel را بزنید.",
    },
    "folder_expired": {
        "en": "This folder button expired. Open the browser again.",
        "fa": "این دکمه پوشه منقضی شده. مرورگر پوشه را دوباره باز کنید.",
    },
    "folder_expired_short": {"en": "This folder button expired.", "fa": "این دکمه پوشه منقضی شده."},
    "unsupported_mode": {"en": "Unsupported mode.", "fa": "حالت پشتیبانی نمی‌شود."},
    "language_prompt": {
        "en": "🌐 Choose your language.",
        "fa": "🌐 زبان خود را انتخاب کنید.",
    },
    "btn_lang_en": {"en": "English", "fa": "English"},
    "btn_lang_fa": {"en": "فارسی", "fa": "فارسی"},
    "language_set": {"en": "✅ Language set to English.", "fa": "✅ زبان به فارسی تغییر یافت."},
    "cmd_start": {"en": "Open main menu", "fa": "باز کردن منوی اصلی"},
    "cmd_project": {"en": "Choose a project", "fa": "انتخاب پروژه"},
    "cmd_status": {"en": "Show current state", "fa": "نمایش وضعیت فعلی"},
    "cmd_cancel": {"en": "Cancel current input", "fa": "لغو ورودی فعلی"},
    "cmd_id": {"en": "Show your Telegram user ID", "fa": "نمایش شناسه تلگرام شما"},
    "cmd_language": {"en": "Change bot language", "fa": "تغییر زبان ربات"},
    "cmd_agent": {"en": "Choose the coding agent", "fa": "انتخاب ایجنت کدنویسی"},
    "agent_selection_prompt": {
        "en": "Choose the coding agent for your sessions.\n\nCurrent agent: {current_agent}",
        "fa": "ایجنت کدنویسی نشست‌های خود را انتخاب کنید.\n\nایجنت فعلی: {current_agent}",
    },
    "agent_not_found": {
        "en": "That agent is no longer configured.",
        "fa": "این ایجنت دیگر پیکربندی نشده است.",
    },
    "btn_agent_selection": {"en": "🤖 Change agent", "fa": "🤖 تغییر ایجنت"},
    "unknown_command": {
        "en": "Unknown command. Send /start to open the main menu.",
        "fa": "دستور ناشناخته است. برای باز کردن منوی اصلی /start را بفرستید.",
    },
}


def t(lang: str | None, key: str, **kwargs: object) -> str:
    lang = lang if lang in LANGUAGES else DEFAULT_LANG
    entry = _STRINGS.get(key)
    if entry is None:
        return key
    template = entry.get(lang) or entry.get(DEFAULT_LANG) or key
    return template.format(**kwargs) if kwargs else template
