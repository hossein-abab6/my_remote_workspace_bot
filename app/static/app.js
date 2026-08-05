const I18N = {
  en: {
    "topbar.eyebrow": "LOCAL CONTROL PANEL",
    "topbar.subtitle": "Connect a messaging bot to a coding agent and your local workspaces.",
    "badge.checking": "Checking runtime…",
    "badge.running": "Bot running · {agent}",
    "badge.error": "Bot stopped · configuration error",
    "badge.stopped": "Bot stopped",
    "badge.setupRequired": "Setup required",
    "badge.unavailable": "Dashboard status unavailable",
    "nav.step1": "1. Connection",
    "nav.step2": "2. Agent",
    "nav.step3": "3. Advanced",
    "nav.step4": "4. Review",
    "sidebar.note.title": "Local-first",
    "sidebar.note.body": "Tokens, database files and logs stay on this computer and are ignored by Git.",
    "conn.step": "CONNECTION",
    "conn.title": "Messaging and workspace access",
    "conn.desc": "Set the Telegram bot identity, authorized users, and the only local root the bot may browse.",
    "conn.transport.label": "Transport",
    "conn.transport.hint": "Telegram is included. Additional transports can be added through the transport layer later.",
    "conn.runtime.label": "Runtime",
    "conn.runtime.enable": "Enable Telegram bot",
    "conn.runtime.hint": "Start polling after settings are saved.",
    "conn.token.label": "Telegram bot token",
    "conn.token.show": "Show",
    "conn.token.hide": "Hide",
    "conn.token.hint.default": "Create a simple bot with @BotFather, then paste the complete token here.",
    "conn.token.hint.saved": "A saved local token exists ({mask}). Leave this field blank to keep it.",
    "conn.users.label": "Allowed Telegram user IDs",
    "conn.users.hint": "Enter one or more positive numeric IDs, separated by commas, spaces, or new lines. Run <code>/id</code> on a temporary bot version to find yours.",
    "conn.root.label": "Projects root on this computer",
    "conn.root.test": "Test path",
    "conn.root.hint": "The bot can browse and create folders only inside this directory.",
    "conn.test.telegram": "Test Telegram token",
    "conn.continue.agent": "Continue to agent",
    "agent.step": "AGENT",
    "agent.title": "Choose the local coding agent",
    "agent.desc": "The bot starts the selected CLI or SDK inside the chosen project folder.",
    "agent.selection.title": "Configured agents",
    "agent.selection.desc": "Every agent here appears in the bot's /agent menu. One provider per agent.",
    "agent.selection.label": "Available agents",
    "agent.selection.hint": "Select an agent to edit it in the fields below.",
    "agent.selection.add": "Add agent",
    "agent.selection.makeDefault": "Set as default",
    "agent.selection.remove": "Remove agent",
    "agent.selection.defaultTag": "default",
    "agent.provider.label": "Agent provider",
    "agent.displayName.label": "Display name",
    "agent.executable.label": "Executable path or command",
    "agent.executable.hint": "Examples: <code>claude</code>, <code>codex</code>, <code>gemini</code>, or an absolute executable path.",
    "agent.model.label": "Model override",
    "agent.mode.label": "Default permission mode",
    "agent.mode.hint": "This can also be changed per Telegram user from the bot menu.",
    "agent.maxTurns.label": "Maximum turns",
    "agent.maxTurns.hint": "0 uses the provider default.",
    "agent.maxBudget.label": "Maximum budget (USD)",
    "agent.maxBudget.hint": "Supported by adapters that expose budget limits. 0 disables it.",
    "custom.title": "Custom CLI contract",
    "custom.desc": "Arguments are executed directly without a shell. Use <code>{prompt}</code> and <code>{session_id}</code> placeholders.",
    "custom.executable.label": "Custom executable",
    "custom.newArgs.label": "New-session arguments (JSON array)",
    "custom.resumeArgs.label": "Resume-session arguments (JSON array)",
    "custom.versionArgs.label": "Version-check arguments (JSON array)",
    "custom.outputFormat.label": "Output format",
    "custom.outputFormat.text": "Plain text",
    "custom.responsePath.label": "Response JSON dot path",
    "custom.sessionPath.label": "Session ID JSON dot path",
    "agent.extraEnv.label": "Extra environment variables (JSON object)",
    "agent.extraEnv.hint": "Do not commit secrets. These values are stored only in the ignored local settings file.",
    "agent.test": "Test agent",
    "agent.continue": "Continue to advanced",
    "adv.step": "ADVANCED",
    "adv.title": "Interface limits",
    "adv.desc": "Control pagination without changing source code.",
    "adv.folderPageSize.label": "Folders per page",
    "adv.sessionPageSize.label": "Sessions per page",
    "adv.historyPageSize.label": "History messages per page",
    "adv.warning.title": "Permission warning",
    "adv.warning.body": "Modes such as Claude <code>bypassPermissions</code>, Codex <code>danger-full-access</code>, and Gemini <code>yolo</code> can execute changes with reduced confirmation. Use them only in isolated workspaces you trust.",
    "adv.continue": "Review settings",
    "review.step": "REVIEW",
    "review.title": "Save and start",
    "review.desc": "Review the generated configuration. Saving restarts the Telegram bot with the new settings.",
    "review.notice.title": "Git-safe runtime data",
    "review.notice.body": "The local token, settings, SQLite database, logs, and agent caches are excluded by <code>.gitignore</code>. The application code and empty runtime directories remain tracked.",
    "review.save": "Save settings and restart bot",
    "review.saving": "Saving…",
    "review.label.transport": "Transport",
    "review.label.users": "Authorized users",
    "review.label.root": "Projects root",
    "review.label.agent": "Agent",
    "review.label.mode": "Default mode",
    "review.label.executable": "Executable",
    "review.label.model": "Model",
    "review.label.token": "Telegram token",
    "review.value.none": "None",
    "review.value.providerDefault": "Provider default",
    "review.value.newToken": "New token entered",
    "review.value.missing": "Missing",
    "review.value.default": "default",
    "review.label.validation": "Validation",
    "error.agentRequired": "Configure at least one agent.",
    "error.providerDuplicate": "Provider '{provider}' is configured twice. Each provider can be used once.",
    "error.allProvidersUsed": "Every available provider is already configured.",
    "error.lastAgent": "At least one agent must remain configured.",
    "error.rootRequired": "Projects root is required.",
    "error.tokenRequired": "Telegram bot token is required while Telegram is enabled.",
    "error.userIdsRequired": "Add at least one allowed Telegram user ID.",
    "error.displayNameRequired": "Agent display name is required.",
    "error.customExecutableRequired": "Custom CLI executable is required.",
    "error.customPromptRequired": "Custom new-session arguments must include {prompt}.",
    "error.userIdNotInteger": "Telegram user ID '{part}' is not a positive integer.",
    "error.userIdOutOfRange": "Telegram user ID '{part}' is outside the valid integer range.",
  },
  fa: {
    "topbar.eyebrow": "پنل کنترل محلی",
    "topbar.subtitle": "یک ربات پیام‌رسان را به یک ایجنت کدنویسی و فضاهای کاری محلی خود متصل کنید.",
    "badge.checking": "در حال بررسی وضعیت اجرا…",
    "badge.running": "ربات فعال است · {agent}",
    "badge.error": "ربات متوقف است · خطای پیکربندی",
    "badge.stopped": "ربات متوقف است",
    "badge.setupRequired": "نیاز به تنظیم اولیه",
    "badge.unavailable": "وضعیت داشبورد در دسترس نیست",
    "nav.step1": "۱. اتصال",
    "nav.step2": "۲. ایجنت",
    "nav.step3": "۳. پیشرفته",
    "nav.step4": "۴. بازبینی",
    "sidebar.note.title": "محلی‌محور",
    "sidebar.note.body": "توکن‌ها، فایل‌های پایگاه‌داده و لاگ‌ها روی همین سیستم می‌مانند و توسط Git نادیده گرفته می‌شوند.",
    "conn.step": "اتصال",
    "conn.title": "دسترسی پیام‌رسانی و فضای کاری",
    "conn.desc": "هویت ربات تلگرام، کاربران مجاز، و تنها ریشه محلی که ربات اجازه مرور آن را دارد مشخص کنید.",
    "conn.transport.label": "روش انتقال",
    "conn.transport.hint": "تلگرام به‌صورت پیش‌فرض موجود است. روش‌های انتقال دیگر بعداً از طریق لایه انتقال قابل افزودن هستند.",
    "conn.runtime.label": "اجرا",
    "conn.runtime.enable": "فعال‌سازی ربات تلگرام",
    "conn.runtime.hint": "پس از ذخیره تنظیمات، دریافت پیام‌ها آغاز می‌شود.",
    "conn.token.label": "توکن ربات تلگرام",
    "conn.token.show": "نمایش",
    "conn.token.hide": "پنهان‌سازی",
    "conn.token.hint.default": "با @BotFather یک ربات ساده بسازید، سپس توکن کامل را اینجا وارد کنید.",
    "conn.token.hint.saved": "یک توکن محلی ذخیره‌شده وجود دارد ({mask}). برای نگه‌داشتن آن، این فیلد را خالی بگذارید.",
    "conn.users.label": "شناسه‌های تلگرام مجاز",
    "conn.users.hint": "یک یا چند شناسه عددی مثبت را با کاما، فاصله یا خط جدید وارد کنید. برای یافتن شناسه خود دستور <code>/id</code> را در یک نسخه موقت ربات اجرا کنید.",
    "conn.root.label": "ریشه پروژه‌ها روی این سیستم",
    "conn.root.test": "تست مسیر",
    "conn.root.hint": "ربات فقط می‌تواند داخل این پوشه، پوشه‌ها را مرور یا ایجاد کند.",
    "conn.test.telegram": "تست توکن تلگرام",
    "conn.continue.agent": "ادامه به ایجنت",
    "agent.step": "ایجنت",
    "agent.title": "ایجنت کدنویسی محلی را انتخاب کنید",
    "agent.desc": "ربات، CLI یا SDK انتخاب‌شده را داخل پوشه پروژه انتخابی اجرا می‌کند.",
    "agent.selection.title": "ایجنت‌های پیکربندی‌شده",
    "agent.selection.desc": "هر ایجنت اینجا در منوی /agent ربات نمایش داده می‌شود. هر ارائه‌دهنده فقط یک بار.",
    "agent.selection.label": "ایجنت‌های موجود",
    "agent.selection.hint": "برای ویرایش، یک ایجنت را انتخاب کنید تا در فیلدهای پایین بارگذاری شود.",
    "agent.selection.add": "افزودن ایجنت",
    "agent.selection.makeDefault": "تعیین به‌عنوان پیش‌فرض",
    "agent.selection.remove": "حذف ایجنت",
    "agent.selection.defaultTag": "پیش‌فرض",
    "agent.provider.label": "ارائه‌دهنده ایجنت",
    "agent.displayName.label": "نام نمایشی",
    "agent.executable.label": "مسیر یا دستور اجرایی",
    "agent.executable.hint": "نمونه‌ها: <code>claude</code>، <code>codex</code>، <code>gemini</code>، یا یک مسیر کامل فایل اجرایی.",
    "agent.model.label": "بازنویسی مدل",
    "agent.mode.label": "حالت مجوز پیش‌فرض",
    "agent.mode.hint": "این مورد را می‌توان برای هر کاربر تلگرام از منوی ربات هم تغییر داد.",
    "agent.maxTurns.label": "حداکثر نوبت‌ها",
    "agent.maxTurns.hint": "۰ یعنی استفاده از پیش‌فرض ارائه‌دهنده.",
    "agent.maxBudget.label": "حداکثر بودجه (دلار)",
    "agent.maxBudget.hint": "توسط آداپتورهایی که محدودیت بودجه دارند پشتیبانی می‌شود. ۰ یعنی غیرفعال.",
    "custom.title": "قرارداد CLI سفارشی",
    "custom.desc": "آرگومان‌ها بدون شل و به‌طور مستقیم اجرا می‌شوند. از جای‌گذارهای <code>{prompt}</code> و <code>{session_id}</code> استفاده کنید.",
    "custom.executable.label": "اجرایی سفارشی",
    "custom.newArgs.label": "آرگومان‌های نشست جدید (آرایه JSON)",
    "custom.resumeArgs.label": "آرگومان‌های ازسرگیری نشست (آرایه JSON)",
    "custom.versionArgs.label": "آرگومان‌های بررسی نسخه (آرایه JSON)",
    "custom.outputFormat.label": "قالب خروجی",
    "custom.outputFormat.text": "متن ساده",
    "custom.responsePath.label": "مسیر نقطه‌ای JSON پاسخ",
    "custom.sessionPath.label": "مسیر نقطه‌ای JSON شناسه نشست",
    "agent.extraEnv.label": "متغیرهای محیطی اضافه (شیء JSON)",
    "agent.extraEnv.hint": "اطلاعات محرمانه را کامیت نکنید. این مقادیر فقط در فایل تنظیمات محلی نادیده‌گرفته‌شده ذخیره می‌شوند.",
    "agent.test": "تست ایجنت",
    "agent.continue": "ادامه به پیشرفته",
    "adv.step": "پیشرفته",
    "adv.title": "محدودیت‌های رابط",
    "adv.desc": "صفحه‌بندی را بدون تغییر کد منبع کنترل کنید.",
    "adv.folderPageSize.label": "تعداد پوشه در هر صفحه",
    "adv.sessionPageSize.label": "تعداد نشست در هر صفحه",
    "adv.historyPageSize.label": "تعداد پیام تاریخچه در هر صفحه",
    "adv.warning.title": "هشدار مجوز",
    "adv.warning.body": "حالت‌هایی مانند <code>bypassPermissions</code> در Claude، <code>danger-full-access</code> در Codex، و <code>yolo</code> در Gemini می‌توانند تغییرات را با تأیید کمتر اجرا کنند. فقط در فضاهای کاری ایزوله‌ای که به آن‌ها اعتماد دارید استفاده کنید.",
    "adv.continue": "بازبینی تنظیمات",
    "review.step": "بازبینی",
    "review.title": "ذخیره و شروع",
    "review.desc": "پیکربندی تولیدشده را بررسی کنید. ذخیره‌سازی باعث راه‌اندازی مجدد ربات تلگرام با تنظیمات جدید می‌شود.",
    "review.notice.title": "داده‌های اجرایی امن برای Git",
    "review.notice.body": "توکن محلی، تنظیمات، پایگاه‌داده SQLite، لاگ‌ها و کش ایجنت توسط <code>.gitignore</code> نادیده گرفته می‌شوند. کد برنامه و پوشه‌های خالی اجرایی همچنان ردیابی می‌شوند.",
    "review.save": "ذخیره تنظیمات و راه‌اندازی مجدد ربات",
    "review.saving": "در حال ذخیره…",
    "review.label.transport": "روش انتقال",
    "review.label.users": "کاربران مجاز",
    "review.label.root": "ریشه پروژه‌ها",
    "review.label.agent": "ایجنت",
    "review.label.mode": "حالت پیش‌فرض",
    "review.label.executable": "فایل اجرایی",
    "review.label.model": "مدل",
    "review.label.token": "توکن تلگرام",
    "review.value.none": "هیچ‌کدام",
    "review.value.providerDefault": "پیش‌فرض ارائه‌دهنده",
    "review.value.newToken": "توکن جدید وارد شد",
    "review.value.missing": "وارد نشده",
    "review.value.default": "پیش‌فرض",
    "review.label.validation": "اعتبارسنجی",
    "error.agentRequired": "دست‌کم یک ایجنت پیکربندی کنید.",
    "error.providerDuplicate": "ارائه‌دهنده «{provider}» دو بار پیکربندی شده است. هر ارائه‌دهنده فقط یک بار قابل استفاده است.",
    "error.allProvidersUsed": "همه ارائه‌دهنده‌های موجود از قبل پیکربندی شده‌اند.",
    "error.lastAgent": "دست‌کم یک ایجنت باید باقی بماند.",
    "error.rootRequired": "ریشه پروژه‌ها الزامی است.",
    "error.tokenRequired": "وقتی تلگرام فعال است، توکن ربات تلگرام الزامی است.",
    "error.userIdsRequired": "دست‌کم یک شناسه تلگرام مجاز اضافه کنید.",
    "error.displayNameRequired": "نام نمایشی ایجنت الزامی است.",
    "error.customExecutableRequired": "فایل اجرایی CLI سفارشی الزامی است.",
    "error.customPromptRequired": "آرگومان‌های نشست جدید سفارشی باید شامل {prompt} باشند.",
    "error.userIdNotInteger": "شناسه تلگرام «{part}» یک عدد صحیح مثبت نیست.",
    "error.userIdOutOfRange": "شناسه تلگرام «{part}» خارج از محدوده مجاز است.",
  },
};

const state = {
  meta: null,
  settings: null,
  agents: [],
  activeAgent: 0,
  lang: (localStorage.getItem("mrwb_lang") === "fa") ? "fa" : "en",
};

const PROVIDER_NAMES = {
  claude: "Claude Code",
  codex: "OpenAI Codex CLI",
  gemini: "Gemini CLI",
  custom: "Custom CLI",
};

const $ = (id) => document.getElementById(id);
const form = $("settingsForm");
const alertBox = $("alert");

function tr(key, vars) {
  const dict = I18N[state.lang] || I18N.en;
  let text = dict[key] ?? I18N.en[key] ?? key;
  if (vars) {
    for (const [name, value] of Object.entries(vars)) {
      text = text.replaceAll(`{${name}}`, String(value));
    }
  }
  return text;
}

function applyStaticI18n() {
  document.documentElement.lang = state.lang;
  document.documentElement.dir = state.lang === "fa" ? "rtl" : "ltr";
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    el.textContent = tr(el.dataset.i18n);
  });
  document.querySelectorAll("[data-i18n-html]").forEach((el) => {
    el.innerHTML = tr(el.dataset.i18nHtml);
  });
  $("langToggle").textContent = state.lang === "fa" ? "English" : "فارسی";
  $("toggleToken").textContent = $("botToken").type === "password" ? tr("conn.token.show") : tr("conn.token.hide");
  updateTokenHint();
}

function updateTokenHint() {
  const mask = state.settings?.bot_token_masked;
  $("tokenHint").textContent = mask ? tr("conn.token.hint.saved", { mask }) : tr("conn.token.hint.default");
}

function setLanguage(lang) {
  state.lang = lang;
  localStorage.setItem("mrwb_lang", lang);
  applyStaticI18n();
  refreshStatus();
  if (state.agents.length) renderAgentList();
  if (document.querySelector('.tab-panel[data-panel="review"]').classList.contains("active")) {
    renderReview();
  }
}

function showAlert(message, type = "success") {
  alertBox.textContent = message;
  alertBox.className = `alert ${type}`;
  alertBox.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function clearAlert() {
  alertBox.className = "alert hidden";
  alertBox.textContent = "";
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  let body = {};
  try { body = await response.json(); } catch (_) { body = {}; }
  if (!response.ok) {
    throw new Error(body.detail || body.message || `Request failed with status ${response.status}`);
  }
  return body;
}

function parseUserIds(value) {
  const parts = value.split(/[\s,;]+/).map((item) => item.trim()).filter(Boolean);
  const values = [];
  for (const part of parts) {
    if (!/^\d+$/.test(part)) throw new Error(tr("error.userIdNotInteger", { part }));
    const number = Number(part);
    if (!Number.isSafeInteger(number) || number <= 0) throw new Error(tr("error.userIdOutOfRange", { part }));
    if (!values.includes(number)) values.push(number);
  }
  return values;
}

function parseJsonField(id, expectedType, fallback) {
  const raw = $(id).value.trim();
  if (!raw) return fallback;
  let value;
  try { value = JSON.parse(raw); } catch (error) {
    throw new Error(`${id}: invalid JSON (${error.message}).`);
  }
  if (expectedType === "array" && !Array.isArray(value)) throw new Error(`${id} must be a JSON array.`);
  if (expectedType === "object" && (Array.isArray(value) || value === null || typeof value !== "object")) throw new Error(`${id} must be a JSON object.`);
  return value;
}

function providerDefinition(provider) {
  return (state.meta?.providers || []).find((item) => item.value === provider);
}

function providerModes(provider) {
  return providerDefinition(provider)?.modes || ["default"];
}

function updateModes(preferred = null) {
  const provider = $("agentProvider").value;
  const modes = providerModes(provider);
  const select = $("defaultMode");
  const current = preferred || select.value;
  select.innerHTML = "";
  for (const mode of modes) {
    const option = document.createElement("option");
    option.value = mode;
    option.textContent = mode;
    select.appendChild(option);
  }
  select.value = modes.includes(current) ? current : modes[0];
  $("customAgentPanel").classList.toggle("hidden", provider !== "custom");

  if (!$("agentDisplayName").dataset.touched) $("agentDisplayName").value = PROVIDER_NAMES[provider];
}

function switchTab(name) {
  document.querySelectorAll(".tab-panel").forEach((panel) => {
    panel.classList.toggle("active", panel.dataset.panel === name);
  });
  document.querySelectorAll(".nav-item").forEach((button) => {
    button.classList.toggle("active", button.dataset.tab === name);
  });
  if (name === "review") renderReview();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

// Read the editor fields back into a plain agent object.
function readAgentForm() {
  const current = state.agents[state.activeAgent] || {};
  return {
    provider: $("agentProvider").value,
    display_name: $("agentDisplayName").value.trim(),
    executable: $("agentExecutable").value.trim(),
    model: $("agentModel").value.trim(),
    default_mode: $("defaultMode").value,
    max_turns: Number($("maxTurns").value || 0),
    max_budget_usd: Number($("maxBudget").value || 0),
    extra_environment: parseJsonField("extraEnvironment", "object", {}),
    custom: {
      executable: $("customExecutable").value.trim(),
      new_session_args: parseJsonField("customNewArgs", "array", ["{prompt}"]),
      resume_session_args: parseJsonField("customResumeArgs", "array", ["--resume", "{session_id}", "{prompt}"]),
      version_args: parseJsonField("customVersionArgs", "array", ["--version"]),
      output_format: $("customOutputFormat").value,
      response_json_path: $("customResponsePath").value.trim(),
      session_id_json_path: $("customSessionPath").value.trim(),
      environment: {},
    },
    is_default: Boolean(current.is_default),
  };
}

// Fold the editor's current contents back into the list before anything reads it.
function commitActiveAgent() {
  if (!state.agents.length) return;
  state.agents[state.activeAgent] = readAgentForm();
}

function buildPayload() {
  commitActiveAgent();
  const botToken = $("botToken").value.trim();
  const keepExisting = Boolean(state.settings?.configured && !botToken);
  return {
    projects_root: $("projectsRoot").value.trim(),
    transport: "telegram",
    telegram_enabled: $("telegramEnabled").checked,
    bot_token: botToken,
    keep_existing_bot_token: keepExisting,
    allowed_user_ids: parseUserIds($("allowedUserIds").value),
    agents: state.agents.map((agent) => ({ ...agent })),
    folder_page_size: Number($("folderPageSize").value),
    session_page_size: Number($("sessionPageSize").value),
    history_page_size: Number($("historyPageSize").value),
  };
}

function validateClient(payload) {
  if (!payload.projects_root) throw new Error(tr("error.rootRequired"));
  if (payload.telegram_enabled && !payload.keep_existing_bot_token && !payload.bot_token) {
    throw new Error(tr("error.tokenRequired"));
  }
  if (payload.telegram_enabled && payload.allowed_user_ids.length === 0) {
    throw new Error(tr("error.userIdsRequired"));
  }
  if (!payload.agents.length) throw new Error(tr("error.agentRequired"));
  const seen = new Set();
  for (const agent of payload.agents) {
    if (!agent.display_name) throw new Error(tr("error.displayNameRequired"));
    if (seen.has(agent.provider)) throw new Error(tr("error.providerDuplicate", { provider: agent.provider }));
    seen.add(agent.provider);
    if (agent.provider === "custom") {
      if (!agent.custom.executable) throw new Error(tr("error.customExecutableRequired"));
      if (!agent.custom.new_session_args.some((item) => String(item).includes("{prompt}"))) {
        throw new Error(tr("error.customPromptRequired"));
      }
    }
  }
}

function renderReview() {
  let payload;
  try {
    payload = buildPayload();
    validateClient(payload);
  } catch (error) {
    $("reviewGrid").innerHTML = `<div class="review-item"><span>${escapeHtml(tr("review.label.validation"))}</span><strong>${escapeHtml(error.message)}</strong></div>`;
    return;
  }
  const items = [
    [tr("review.label.transport"), "Telegram"],
    [tr("review.label.users"), payload.allowed_user_ids.join(", ") || tr("review.value.none")],
    [tr("review.label.root"), payload.projects_root],
  ];
  for (const agent of payload.agents) {
    const suffix = agent.is_default ? ` — ${tr("review.value.default")}` : "";
    const executable = agent.provider === "custom"
      ? agent.custom.executable
      : (agent.executable || tr("review.value.providerDefault"));
    items.push([
      `${tr("review.label.agent")}: ${agent.display_name}${suffix}`,
      `${agent.provider} · ${agent.default_mode} · ${executable} · ${agent.model || tr("review.value.providerDefault")}`,
    ]);
  }
  items.push(
    [tr("review.label.token"), payload.keep_existing_bot_token ? state.settings.bot_token_masked : (payload.bot_token ? tr("review.value.newToken") : tr("review.value.missing"))],
  );
  $("reviewGrid").innerHTML = items.map(([label, value]) => (
    `<div class="review-item"><span>${escapeHtml(label)}</span><strong>${escapeHtml(String(value))}</strong></div>`
  )).join("");
}

function escapeHtml(value) {
  return value.replace(/[&<>'"]/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" }[char]));
}

function blankAgent(provider) {
  return {
    provider,
    display_name: PROVIDER_NAMES[provider],
    executable: "",
    model: "",
    default_mode: providerModes(provider)[0],
    max_turns: 0,
    max_budget_usd: 0,
    extra_environment: {},
    custom: {
      executable: "",
      new_session_args: ["{prompt}"],
      resume_session_args: ["--resume", "{session_id}", "{prompt}"],
      version_args: ["--version"],
      output_format: "text",
      response_json_path: "",
      session_id_json_path: "",
      environment: {},
    },
    is_default: false,
  };
}

// Load one agent into the editor fields.
function writeAgentForm(agent) {
  const custom = agent.custom || blankAgent(agent.provider).custom;
  $("agentProvider").value = agent.provider;
  $("agentDisplayName").value = agent.display_name;
  $("agentDisplayName").dataset.touched = "1";
  $("agentExecutable").value = agent.executable || "";
  $("agentModel").value = agent.model || "";
  $("maxTurns").value = agent.max_turns ?? 0;
  $("maxBudget").value = agent.max_budget_usd ?? 0;
  $("extraEnvironment").value = JSON.stringify(agent.extra_environment || {}, null, 2);
  $("customExecutable").value = custom.executable || "";
  $("customNewArgs").value = JSON.stringify(custom.new_session_args, null, 2);
  $("customResumeArgs").value = JSON.stringify(custom.resume_session_args, null, 2);
  $("customVersionArgs").value = JSON.stringify(custom.version_args, null, 2);
  $("customOutputFormat").value = custom.output_format;
  $("customResponsePath").value = custom.response_json_path || "";
  $("customSessionPath").value = custom.session_id_json_path || "";
  updateModes(agent.default_mode);
}

function renderAgentList() {
  const select = $("agentSelection");
  select.innerHTML = "";
  state.agents.forEach((agent, index) => {
    const option = document.createElement("option");
    option.value = String(index);
    option.textContent = agent.is_default
      ? `${agent.display_name} (${agent.provider}) — ${tr("agent.selection.defaultTag")}`
      : `${agent.display_name} (${agent.provider})`;
    select.appendChild(option);
  });
  select.value = String(state.activeAgent);
  $("removeAgent").disabled = state.agents.length <= 1;
  $("makeDefaultAgent").disabled = Boolean(state.agents[state.activeAgent]?.is_default);
}

function selectAgent(index, { commit = true } = {}) {
  if (commit) commitActiveAgent();
  state.activeAgent = Math.max(0, Math.min(index, state.agents.length - 1));
  writeAgentForm(state.agents[state.activeAgent]);
  renderAgentList();
}

function populate(settings) {
  state.settings = settings;
  $("telegramEnabled").checked = settings.telegram_enabled;
  $("projectsRoot").value = settings.projects_root || "";
  $("allowedUserIds").value = settings.allowed_user_ids.join(", ");
  updateTokenHint();

  const agents = (settings.agents || []).map((agent) => ({ ...blankAgent(agent.provider), ...agent }));
  if (!agents.length) agents.push({ ...blankAgent("claude"), is_default: true });
  if (!agents.some((agent) => agent.is_default)) agents[0].is_default = true;
  state.agents = agents;

  $("folderPageSize").value = settings.folder_page_size;
  $("sessionPageSize").value = settings.session_page_size;
  $("historyPageSize").value = settings.history_page_size;
  selectAgent(agents.findIndex((agent) => agent.is_default), { commit: false });
}

async function refreshStatus() {
  try {
    const status = await api("/api/status");
    const badge = $("runtimeBadge");
    if (status.botRunning) {
      badge.className = "status-badge running";
      badge.textContent = tr("badge.running", { agent: status.agentName });
    } else if (status.error) {
      badge.className = "status-badge error";
      badge.textContent = tr("badge.error");
    } else {
      badge.className = "status-badge muted";
      badge.textContent = status.configured ? tr("badge.stopped") : tr("badge.setupRequired");
    }
  } catch (_) {
    $("runtimeBadge").textContent = tr("badge.unavailable");
  }
}

async function initialize() {
  applyStaticI18n();
  try {
    [state.meta, state.settings] = await Promise.all([api("/api/meta"), api("/api/settings")]);
    populate(state.settings);
    await refreshStatus();
  } catch (error) {
    showAlert(error.message, "error");
  }
}

// Agent list controls. The list lives in state.agents and is persisted with the
// rest of the settings by the Save button on the Review step.
$("agentSelection").addEventListener("change", (event) => {
  clearAlert();
  try {
    selectAgent(Number(event.target.value));
  } catch (error) {
    event.target.value = String(state.activeAgent);
    showAlert(error.message, "error");
  }
});

$("addAgent").addEventListener("click", () => {
  clearAlert();
  try { commitActiveAgent(); } catch (error) { showAlert(error.message, "error"); return; }
  const used = new Set(state.agents.map((agent) => agent.provider));
  const free = (state.meta?.providers || []).map((item) => item.value).find((value) => !used.has(value));
  if (!free) { showAlert(tr("error.allProvidersUsed"), "error"); return; }
  state.agents.push(blankAgent(free));
  selectAgent(state.agents.length - 1, { commit: false });
});

$("removeAgent").addEventListener("click", () => {
  clearAlert();
  if (state.agents.length <= 1) { showAlert(tr("error.lastAgent"), "error"); return; }
  const removed = state.agents.splice(state.activeAgent, 1)[0];
  if (removed.is_default) state.agents[0].is_default = true;
  selectAgent(Math.min(state.activeAgent, state.agents.length - 1), { commit: false });
});

$("makeDefaultAgent").addEventListener("click", () => {
  clearAlert();
  try { commitActiveAgent(); } catch (error) { showAlert(error.message, "error"); return; }
  state.agents.forEach((agent, index) => { agent.is_default = index === state.activeAgent; });
  renderAgentList();
});

document.querySelectorAll(".nav-item").forEach((button) => button.addEventListener("click", () => switchTab(button.dataset.tab)));
document.querySelectorAll(".next-tab").forEach((button) => button.addEventListener("click", () => {
  clearAlert();
  try { validateClient(buildPayload()); } catch (error) { showAlert(error.message, "error"); return; }
  switchTab(button.dataset.next);
}));

$("agentProvider").addEventListener("change", () => {
  // A name still equal to a stock provider label was never customised, so retitle it.
  const name = $("agentDisplayName").value.trim();
  if (!name || Object.values(PROVIDER_NAMES).includes(name)) {
    delete $("agentDisplayName").dataset.touched;
  }
  updateModes();
  $("agentDisplayName").dataset.touched = "1";
  try { commitActiveAgent(); renderAgentList(); } catch (_) { /* list label refreshes on next commit */ }
});
$("agentDisplayName").addEventListener("input", (event) => {
  event.target.dataset.touched = "1";
  const agent = state.agents[state.activeAgent];
  if (agent) { agent.display_name = event.target.value.trim(); renderAgentList(); }
});
$("toggleToken").addEventListener("click", () => {
  const input = $("botToken");
  input.type = input.type === "password" ? "text" : "password";
  $("toggleToken").textContent = input.type === "password" ? tr("conn.token.show") : tr("conn.token.hide");
});
$("langToggle").addEventListener("click", () => setLanguage(state.lang === "fa" ? "en" : "fa"));

$("testRoot").addEventListener("click", async (event) => {
  clearAlert(); event.target.disabled = true;
  try {
    const result = await api("/api/validate/root", { method: "POST", body: JSON.stringify({ projects_root: $("projectsRoot").value }) });
    showAlert(result.message, "success");
  } catch (error) { showAlert(error.message, "error"); }
  finally { event.target.disabled = false; }
});

$("testTelegram").addEventListener("click", async (event) => {
  clearAlert(); event.target.disabled = true;
  try {
    const result = await api("/api/validate/telegram", {
      method: "POST",
      body: JSON.stringify({
        bot_token: $("botToken").value,
        keep_existing_bot_token: Boolean(state.settings?.configured && !$("botToken").value.trim()),
      }),
    });
    showAlert(result.message, "success");
  } catch (error) { showAlert(error.message, "error"); }
  finally { event.target.disabled = false; }
});

$("testAgent").addEventListener("click", async (event) => {
  clearAlert(); event.target.disabled = true;
  try {
    const payload = buildPayload(); validateClient(payload);
    const result = await api("/api/validate/agent", { method: "POST", body: JSON.stringify(payload) });
    showAlert(result.message, "success");
  } catch (error) { showAlert(error.message, "error"); }
  finally { event.target.disabled = false; }
});

form.addEventListener("submit", async (event) => {
  event.preventDefault(); clearAlert();
  const button = $("saveSettings"); button.disabled = true; button.textContent = tr("review.saving");
  try {
    const payload = buildPayload(); validateClient(payload);
    const result = await api("/api/settings", { method: "POST", body: JSON.stringify(payload) });
    state.settings = result.settings;
    populate(result.settings);
    showAlert(result.message, result.ok ? "success" : "error");
    await refreshStatus();
  } catch (error) { showAlert(error.message, "error"); }
  finally { button.disabled = false; button.textContent = tr("review.save"); }
});

initialize();
setInterval(refreshStatus, 10000);
