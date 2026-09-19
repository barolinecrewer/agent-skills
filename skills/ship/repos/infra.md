# infra

Path: `~/infra`. Homelab; pushes to the branch trigger deploy workflows.

- If the diff touches stacks, hosts, or networking config, update `README.md` to reflect the current state, and include it in the commit.
- Never read or stage `.env`, `stack.env`, or `Caddyfile` files (live secrets). Only `.j2` sources are committed.
- Suggested scopes: stack name (`media`, `bambu-printer-mcp`), `dns`, `jellyfin`, `ansible`, `vps`, `ci`.
- Always watch the GitHub Actions run after pushing and report status.
