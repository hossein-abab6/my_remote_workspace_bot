# Security Policy

## Supported versions

Security fixes are currently applied to the latest `0.1.x` release line.

## Reporting a vulnerability

Do not open a public issue containing bot tokens, local paths, credentials, command output, or exploit details. Contact the maintainer privately through the repository security-advisory feature.

Include:

- affected version and operating system
- selected transport, agent provider, and permission mode
- minimal reproduction steps
- impact and suggested mitigation, when known

## Security model

- The dashboard binds to `127.0.0.1` by default.
- Telegram access is restricted to configured numeric user IDs.
- Workspace paths are resolved and constrained below one configured projects root.
- The custom CLI adapter uses direct argument execution and does not invoke a command shell.
- Local settings, tokens, database files, logs, and agent caches are ignored by Git.

## Important limitations

The local Telegram token is stored in plain text in `data/settings.json` so the process can use it. Filesystem and operating-system account security are therefore part of the trust boundary.

Do not expose the dashboard to the public internet without adding strong authentication, TLS, CSRF protections suitable for remote deployment, and a properly configured reverse proxy.

High-permission agent modes can modify or delete files and execute commands. Use a dedicated workspace, source control, backups, and the least-privileged mode that satisfies the task.
