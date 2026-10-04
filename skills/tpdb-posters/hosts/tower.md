# tower

Unraid box running Jellyfin (`~/infra/stacks/media`) and Silo (`~/infra/stacks/silo`).

- SSH: prefer the `mcp__aperture__TailnetSSH_run_command` tool on machine `tower`. For `scp` uploads, or when Aperture is down, use `ssh`/`scp root@tower.<tailnet>.ts.net` with `-o BatchMode=yes`.
- Library root: `/mnt/user/data/media`. Jellyfin sees it as `/media`, so NFO `<poster>` tags read `/media/movies/<folder>/folder.jpg`.
- Staging/backups: `/mnt/user/appdata/tpdb-<slug>/`, one per run (e.g. `tpdb-set97`, `tpdb-rhj`).
- Refresh: the Jellyfin MCP `jellyfin_library_manage` with `action: scan`.
- Silo does **not** read local artwork. It pulls posters from TMDB/TVDB into its own cache (`media_items.poster_source_path` is `tmdb://...`), so tell the user these posters will show in Jellyfin only.
- `media/disney/` holds theme-park ride videos, not films; ignore it.
