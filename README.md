# my_remote_workspace_bot

A local-first control panel and Telegram gateway for coding agents. Choose a folder from Telegram, create a workspace, start or resume project sessions, review prior messages, and change the agent permission mode without editing source files.

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-alpha-orange)

> This application runs on the same computer as your projects and agent CLI. Keep that computer powered on and connected to the internet while using the Telegram bot.

## Features

- Browser-based first-run setup and settings editor
- Telegram token validation and multiple authorized user IDs
- Restricted local workspace root with safe folder browsing and folder creation
- Project-specific session list, new sessions, resume, and paginated local history
- Permission-mode selection from Telegram for each authorized user
- Built-in adapters:
  - Claude Code through the Claude Agent SDK
  - OpenAI Codex CLI through `codex exec --json`
  - Gemini CLI through non-interactive JSON output
  - Generic custom CLI adapter with argument placeholders and JSON extraction paths
- SQLite runtime storage and local workflow state
- Runtime secrets, database, settings, logs, and caches excluded from Git
- Responsive neutral UI without a Node.js build step
- GitHub Actions, tests, contribution guide, security policy, issue templates, and MIT license

## Architecture

```text
Browser setup UI (FastAPI)
        │
        ├── local settings.json (ignored)
        ├── SQLite database (ignored)
        └── Telegram transport
                  │
                  ├── workspace browser
                  ├── session/history UI
                  └── agent adapter
                         ├── Claude Code
                         ├── Codex CLI
                         ├── Gemini CLI
                         └── Custom CLI
```

Telegram is the bundled transport. The application separates transport, runtime, persistence, and agent adapters so another messaging transport can be implemented later without rewriting the agent layer.

## Requirements

- Python 3.11 or newer
- A Telegram bot token from [@BotFather](https://t.me/BotFather)
- At least one numeric Telegram user ID
- One supported coding agent installed and authenticated locally
- A writable local directory that will act as the projects root

### Agent prerequisites

Choose only the provider you intend to use:

- **Claude Code:** install and authenticate Claude Code. The Python dependency includes `claude-agent-sdk`.
- **Codex CLI:** install Codex CLI and authenticate it before starting the bot.
- **Gemini CLI:** install Gemini CLI and authenticate it before starting the bot.
- **Custom CLI:** provide an executable and a stable non-interactive command contract.

Official references:

- Claude Agent SDK: https://platform.claude.com/docs/en/agent-sdk/python
- Codex non-interactive mode: https://developers.openai.com/codex/noninteractive
- Gemini CLI non-interactive mode: https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/headless.md

## Quick start on Windows

```powershell
# Clone or extract the repository
cd my_remote_workspace_bot

# Create the virtual environment and install dependencies
powershell -ExecutionPolicy Bypass -File .\scripts\setup_windows.ps1

# Start the local dashboard
.\start_windows.bat
```

The browser opens at `http://127.0.0.1:8787`.

## Quick start on Linux or macOS

```bash
cd my_remote_workspace_bot
chmod +x scripts/setup_unix.sh start_linux.sh
./scripts/setup_unix.sh
./start_linux.sh
```

## First-run setup

1. Create a basic Telegram bot with `@BotFather` and copy its token.
2. Open the local dashboard.
3. Enter the token and one or more authorized numeric Telegram user IDs.
4. Select a writable projects root, such as `C:/Users/Name/Desktop/Projects`.
5. Configure one or more agents. Each agent uses a distinct provider, and one is marked
   as the default that Telegram users get until they pick another with `/agent`.
6. Use the validation buttons for the folder, Telegram token, and agent executable.
7. Save. The application starts or restarts the Telegram bot.
8. Open the bot in Telegram and send `/start`.

If the bot cannot start and the dashboard reports that `api.telegram.org` is unreachable,
Telegram is blocked on your network. Set `MRWB_TELEGRAM_PROXY` in `.env` to a working
proxy URL (`http://…`, `socks5://…`, or `socks5h://…`) and restart the application.
`HTTPS_PROXY` and `ALL_PROXY` are honoured as fallbacks.

## Telegram workflow

```text
Main menu
├── Choose project
│   ├── Browse folders
│   ├── Select project
│   └── Show sessions for that project
│       ├── New session
│       ├── Select an earlier session
│       │   ├── Load previous messages
│       │   ├── Continue the conversation
│       │   └── Browse older messages
│       ├── Agent and permission mode
│       └── Change project
├── Create folder
│   ├── Choose the parent location
│   ├── Enter a folder name
│   ├── Create and select the folder
│   └── Show the folder's session page
└── Current status
    ├── Selected project
    ├── Active session
    ├── Last activity
    └── Agent execution status
```

The visible Telegram command menu is intentionally limited so session creation cannot bypass project selection:

| Command | Purpose |
|---|---|
| `/start` | Open the main menu |
| `/project` | Browse and select a project |
| `/status` | Show project, session, last activity, and execution status |
| `/cancel` | Cancel folder-name input |
| `/language` | Switch the bot language |
| `/agent` | Choose which configured agent to use |
| `/id` | Show the current Telegram user ID |

## Agent modes

The dashboard validates provider-specific modes and the Telegram menu exposes the same choices:

- Claude Code: `default`, `acceptEdits`, `plan`, `dontAsk`, `bypassPermissions`, `auto`
- Codex CLI: `read-only`, `workspace-write`, `danger-full-access`
- Gemini CLI: `default`, `auto_edit`, `plan`, `yolo`
- Custom CLI: `default`

High-permission modes can execute edits or commands with reduced confirmation. Use them only in isolated, trusted workspaces.

## Session behavior

- Every session created or used by the bot is recorded in the local SQLite database.
- User and agent messages are stored locally so Telegram history can be paginated reliably.
- Claude Code sessions already present for a selected project are discovered through the Claude Agent SDK and can be imported into the bot list.
- Codex and Gemini sessions created through this application are resumed using the external session identifier returned by their CLI output when available.
- A custom adapter can resume only when its CLI returns a session identifier and the configured resume argument template uses `{session_id}`.

## Custom CLI adapter

The custom adapter executes an argument array directly, without a shell.

Available placeholders:

- `{prompt}`: current user message
- `{session_id}`: external session identifier for resumed sessions

Example new-session arguments:

```json
["run", "--json", "{prompt}"]
```

Example resume arguments:

```json
["resume", "{session_id}", "--json", "{prompt}"]
```

For JSON or JSONL output, configure dot paths such as:

```text
response.text
session.id
```

The custom adapter intentionally does not use `shell=True`; this reduces command-injection risk from user prompts.

## Local files and Git safety

Tracked runtime placeholders:

```text
data/.gitkeep
logs/.gitkeep
```

Ignored private/runtime files include:

```text
.env
data/settings.json
data/*.db
logs/*
.claude/
.codex/
.gemini/
```

Do not remove these ignore rules before publishing the repository. The token is currently stored in the ignored local settings file in plain text because the bot must read it at runtime. Protect the operating-system account and filesystem.

## Development

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Unix: source .venv/bin/activate
pip install -r requirements-dev.txt
pytest
ruff check .
```

## Known limitations

- Telegram is the only bundled transport in version 0.1.1.
- The app must run on the machine that has the local workspaces and agent credentials.
- Custom CLI compatibility depends on the external tool's non-interactive and session-resume interface.
- Gemini session IDs vary by CLI version/output; local message history remains available even if an external session ID is not returned.
- This is an alpha project. Review generated changes and use source control before enabling high-permission modes.

## Security

Read [SECURITY.md](SECURITY.md) before exposing the dashboard outside localhost. The default host is `127.0.0.1`; do not bind it publicly without adding authentication, TLS, and a trusted reverse proxy.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). By participating, you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## License

MIT. See [LICENSE](LICENSE).
