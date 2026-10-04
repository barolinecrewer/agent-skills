# tower

Unraid box running Jellyfin (`~/infra/stacks/media`) and Silo (`~/infra/stacks/silo`).

- SSH: prefer the `mcp__aperture__TailnetSSH_run_command` tool on machine `tower`. For `scp` uploads, or when Aperture is down, use `ssh`/`scp root@tower.<tailnet>.ts.net` with `-o BatchMode=yes`.
- Library root: `/mnt/user/data/media`. Jellyfin sees it as `/media`, so NFO `<poster>` tags read `/media/movies/<folder>/folder.jpg`.
- Staging/backups: `/mnt/user/appdata/tpdb-<slug>/`, one per run (e.g. `tpdb-set97`, `tpdb-rhj`).
- Refresh Jellyfin: the Jellyfin MCP `jellyfin_library_manage` with `action: scan`.
- Silo: yes. NFO Files is enabled on Movies and TV (all levels).
  - Silo media root: `/mnt/media`.
  - Postgres: `ssh root@tower 'docker exec -i postgres psql -U postgres -d silo -At -F "<TAB>"' < silo.sql`.
  - `SILO_URL=https://silo.milopolis.org`.
  - `SILO_API_KEY=$(pass-cli item get pass://git-secrets/silo/api-key)`, which is field `api-key` on the existing `silo` item. If it's missing, ask the user to create an API key from Silo's admin account and store it there.
  - Verify by checking that `media_items.poster_source_path` starts with `file:///mnt/media/...` for the refreshed items.
  - Known stale NFOs: `Mean Girls (2024)` points at the 2004 film. Don't refresh it by hand until it's fixed.
- `media/disney/` holds theme-park ride videos, not films; ignore it.
