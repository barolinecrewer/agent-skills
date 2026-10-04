---
name: tpdb-posters
description: Download posters from ThePosterDB (a set URL or a whole uploader's page) and apply them as local artwork (folder.jpg, seasonNN-poster.jpg) in a Jellyfin/Kodi NFO media library over SSH. Use when asked to grab, apply, or swap posters from theposterdb.com.
argument-hint: <theposterdb set or user URL>
---

# ThePosterDB posters

Apply posters from a ThePosterDB set (`https://theposterdb.com/set/<id>`) or uploader (`https://theposterdb.com/user/<name>`) to the local library. All the parsing lives in `tpdb.py` next to this file (stdlib only; run `python3 tpdb.py selftest` after editing it).

Read `hosts/<host>.md` relative to this skill for the media host, SSH method, library root, and media-server refresh. If none exists, ask the user where the library lives, then write one.

Work in the session scratchpad; call it `$W`. `$T` is this skill's directory.

1. **Scrape.** `python3 $T/tpdb.py scrape <url> > $W/posters.tsv`. A set URL returns only that set's posters (the page also shows linked sets; those are dropped). A user URL walks every page at 1s/page, so roughly 2 minutes per 3,000 uploads.
2. **List the library** on the host, from the library root (it must contain `movies/` and `tv/`):
   ```sh
   cd <root>; for d in tv/*/; do s=$(basename "$d"); y=$(grep -m1 -oE "<year>[0-9]{4}" "$d/tvshow.nfo" 2>/dev/null | cut -c7-); printf "%s\t%s\t%s\n" "$s" "$y" "$(ls "$d" | grep -oE "^Season [0-9]+|^Specials" | tr "\n" ",")"; done; echo "@@"; ls movies
   ```
   Save the output to `$W/library.txt`.
3. **Match.** `python3 $T/tpdb.py match $W/posters.tsv $W/library.txt [--skip $W/skip.txt] > $W/plan.tsv`. `--skip` takes folder names, one per line, that should keep their current poster. Matching ignores case and punctuation, drops a `(US)`/`(UK)` suffix, and allows a ±1 year difference. When a title has several posters, the first one listed wins, which is the newest upload on user pages. Collection, company and person posters are skipped because they have no local file convention.
4. **Review before writing.** Show the counts (movies, shows, season posters) and anything doubtful. If a title has alternates inside one set, preview them (`sips -Z 400`, then Read the image) and say which one you picked. Also run a near-miss check: list poster shows/movies whose normalized name is a substring of a local folder name, or the other way round. Report real misses; don't force them.
5. **Fetch.** `python3 $T/tpdb.py fetch $W/plan.tsv $W/img`. This saves every poster as a real JPEG (`<id>.jpg`; PNGs are converted with `sips`).
6. **Apply with backups.** Upload `$W/img/*.jpg` and `plan.tsv` to `<stage>/new/` on the host, then run there:
   ```sh
   B=<stage>; M=<root>; while IFS="	" read -r id dest t; do d=$(dirname "$M/$dest"); [ -d "$d" ] || { echo "MISSING $dest"; continue; }; mkdir -p "$(dirname "$B/backup/$dest")"; [ -f "$M/$dest" ] && [ ! -f "$B/backup/$dest" ] && cp -p "$M/$dest" "$B/backup/$dest"; cp "$B/new/$id.jpg" "$M/$dest" || echo "FAIL $dest"; done < $B/new/plan.tsv
   ```
   The backup is written only once, so a re-run never overwrites the true original. Restoring is `cp -a $B/backup/. $M/`.
7. **Refresh the media server** as the host file says. Then report what was applied, what was skipped and why, and where the backups are.

## Notes

- Assets download from `https://theposterdb.com/api/assets/<poster-id>`. Use the `data-poster-id` from the page; the `/posters/<n>` links on the page are title pages, not poster IDs.
- NFO `<poster>` tags already point at `folder.jpg`, so replacing the file is enough. Don't edit the NFOs.
