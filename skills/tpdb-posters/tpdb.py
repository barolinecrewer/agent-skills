#!/usr/bin/env python3
"""ThePosterDB -> Jellyfin/Kodi-style local artwork.

  tpdb.py scrape <set-or-user-url>            > posters.tsv   (id, type, title)
  tpdb.py match posters.tsv library.txt [--skip done.txt] > plan.tsv  (id, dest, title)
  tpdb.py fetch plan.tsv <outdir>             downloads <id>.jpg for every plan row
  tpdb.py folders plan.tsv                    > folders.txt   (movies/X, tv/Y: one per touched item)
  tpdb.py silo-sql folders.txt <silo-media-root> > silo.sql   (rel, content_id, tmdb_id)
  tpdb.py silo-refresh silo.tsv nfo.tsv       POST a quick metadata refresh per item (env SILO_URL, SILO_API_KEY)
  tpdb.py selftest

library.txt is produced on the media host by the listing snippet in SKILL.md:
TV lines "<folder>\t<year>\t<Season 1,Specials,...>", then "@@", then movie folders.
"""
import html, json, os, re, subprocess, sys, time, unicodedata, urllib.request
from pathlib import Path

UA = {"User-Agent": "Mozilla/5.0"}
ROW = re.compile(r"data-poster-id='(\d+)' data-poster-type='(\w+)'.*?text-break\">(.*?)</p>", re.S)


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()


def scrape(url):
    """Set URL -> just that set's posters (linked sets on the page are dropped). User URL -> every page."""
    url = url.split("?")[0]
    if "/set/" in url:
        s = get(url).decode()
        n = re.search(r'title="Posters in Set">(\d+)<', s)
        rows = ROW.findall(s)
        return rows[: int(n[1])] if n else rows
    out, p = [], 1
    while rows := ROW.findall(get(f"{url}?page={p}").decode()):
        out += rows
        p += 1
        time.sleep(1)  # be polite to TPDB
    return out


def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower().replace("&", "and")
    return re.sub(r"[^a-z0-9]", "", s)


def fuzzy(d, k, y):
    # ponytail: ±1yr fuzz covers folder/TPDB year drift (Toy Story 3 2009 vs 2010); a remake one year apart would mis-hit
    return d.get((k, y)) or d.get((k, y - 1)) or d.get((k, y + 1))


def match(posters, library, skip=()):
    """posters: [(id, type, title)]. Returns {dest_relpath: (id, title)}; first row per dest wins (TPDB lists newest first)."""
    tv, movies = library.split("@@\n")
    mov = {}
    for f in movies.splitlines():
        if m := re.match(r"(.*) \((\d{4})\)$", f):
            mov[(norm(m[1]), int(m[2]))] = f
    shows = {}
    for line in filter(None, tv.splitlines()):
        name, y, seasons = line.split("\t")
        base = re.sub(r" \((\d{4}|US|UK)\)$", "", name)
        shows[(norm(base), int(y) if y else 0)] = (name, seasons.rstrip(",").split(","))
    plan = {}
    for pid, typ, t in posters:
        if typ == "movie":
            m = re.match(r"(.*) \((\d{4})\)$", t)
            f = m and fuzzy(mov, norm(m[1]), int(m[2]))
            if f and f not in skip:
                plan.setdefault(f"movies/{f}/folder.jpg", (pid, t))
        elif typ == "show":
            m = re.match(r"(.*?) \((\d{4})\)(?: - (Season (\d+)|Specials))?$", t)
            if not m:
                continue
            k = norm(m[1])
            s = fuzzy(shows, k, int(m[2])) or shows.get((k, 0))
            if not s or s[0] in skip:
                continue
            name, seasons = s
            if m[3] is None:
                dest = "folder.jpg"
            elif m[3] == "Specials":
                dest = "season-specials-poster.jpg" if "Specials" in seasons else None
            else:
                n = int(m[4])
                hit = any(re.fullmatch(rf"Season 0*{n}", x) for x in seasons)
                dest = f"season{n:02d}-poster.jpg" if hit else None
            if dest:
                plan.setdefault(f"tv/{name}/{dest}", (pid, t))
        # collection/company/person posters: no local folder convention, skipped
    return plan


def fetch(plan_rows, outdir):
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    for pid in sorted({r[0] for r in plan_rows}):
        jpg = out / f"{pid}.jpg"
        if jpg.exists() and jpg.stat().st_size:
            continue
        data = get(f"https://theposterdb.com/api/assets/{pid}")
        if data[:3] == b"\xff\xd8\xff":  # already JPEG
            jpg.write_bytes(data)
        else:  # usually PNG; folder.jpg must really be JPEG
            raw = out / f"{pid}.raw"
            raw.write_bytes(data)
            # ponytail: sips is macOS-only; swap for `magick` / Pillow if run elsewhere
            r = subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "92", raw, "--out", jpg], capture_output=True)
            raw.unlink()
            if r.returncode:
                print(f"FAIL {pid}", file=sys.stderr)
        time.sleep(1)


def folders(plan_rows):
    return sorted({"/".join(r[1].split("/")[:2]) for r in plan_rows})


def silo_sql(rels, root):
    q = lambda v: "'" + v.replace("'", "''") + "'"
    vals = ",".join(f"({q(r)})" for r in rels)
    return (f"with t(rel) as (values {vals}) select t.rel, mi.content_id, coalesce(mi.tmdb_id::text, '') from t "
            f"cross join lateral (select content_id from media_files where starts_with(file_path, {q(root.rstrip('/') + '/')} || t.rel || '/') limit 1) f "
            "join media_items mi on mi.content_id = f.content_id;")


def silo_targets(silo_rows, nfo_ids):
    """Admin item refresh is a *manual* refresh, where NFO <uniqueid>s beat Silo's stored match.
    Skip items whose NFO tmdb id disagrees with Silo's, so a stale NFO can't re-anchor them."""
    go, skipped = [], []
    for rel, cid, silo_tmdb in silo_rows:
        nfo = nfo_ids.get(rel, "")
        (skipped if nfo and silo_tmdb and nfo != silo_tmdb else go).append((rel, cid, nfo, silo_tmdb))
    return go, skipped


def silo_refresh(go):
    url, key = os.environ["SILO_URL"].rstrip("/"), os.environ["SILO_API_KEY"]
    for rel, cid, *_ in go:
        req = urllib.request.Request(f"{url}/api/v2/admin/items/{cid}/refresh-metadata", data=b'{"mode":"quick"}', method="POST",
                                     headers={**UA, "Authorization": f"Bearer {key}", "Content-Type": "application/json"})
        try:
            urllib.request.urlopen(req, timeout=30)
            print(f"queued\t{rel}")
        except urllib.error.HTTPError as e:
            print(f"FAIL {e.code}\t{rel}\t{e.read()[:200]!r}", file=sys.stderr)


def selftest():
    lib = ("Ted Lasso\t2020\t\nEuphoria (US)\t2019\tSeason 1,Season 2,\nBoJack\t2014\tSeason 01,Specials,\n@@\n"
           "Toy Story 3 (2009)\nCoco (2017)\nWALL·E (2008)\n")
    posters = [
        ("1", "movie", "Toy Story 3 (2010)"), ("2", "movie", "Coco (2017)"), ("3", "movie", "Coco (2017)"),
        ("4", "movie", "WALL·E (2008)"), ("5", "show", "Euphoria (2019)"), ("6", "show", "Euphoria (2019) - Season 2"),
        ("7", "show", "Euphoria (2019) - Season 9"), ("8", "show", "BoJack (2014) - Season 1"),
        ("9", "show", "BoJack (2014) - Specials"), ("10", "show", "Ted Lasso (2020) - Specials"),
        ("11", "collection", "Pixar Collection"), ("12", "movie", "Nope (2022)"),
    ]
    p = {d: i for d, (i, _) in match(posters, lib, skip={"Coco (2017)"}).items()}
    assert p == {
        "movies/Toy Story 3 (2009)/folder.jpg": "1",
        "movies/WALL·E (2008)/folder.jpg": "4",
        "tv/Euphoria (US)/folder.jpg": "5",
        "tv/Euphoria (US)/season02-poster.jpg": "6",
        "tv/BoJack/season01-poster.jpg": "8",
        "tv/BoJack/season-specials-poster.jpg": "9",
    }, p
    assert folders([("1", "movies/A (1)/folder.jpg", ""), ("2", "tv/B/season01-poster.jpg", ""), ("3", "tv/B/folder.jpg", "")]) == ["movies/A (1)", "tv/B"]
    assert "('movies/A Bug''s Life (1998)')" in silo_sql(["movies/A Bug's Life (1998)"], "/mnt/media/")
    go, skip = silo_targets([("m/Ok", "c1", "5"), ("m/Bad", "c2", "6"), ("m/Local", "local-x", ""), ("m/NoNfo", "c4", "8")],
                            {"m/Ok": "5", "m/Bad": "7", "m/Local": "9"})
    assert [g[0] for g in go] == ["m/Ok", "m/Local", "m/NoNfo"] and [k[0] for k in skip] == ["m/Bad"], (go, skip)
    print("ok")


if __name__ == "__main__":
    cmd, *a = sys.argv[1:] or ["-h"]
    if cmd == "scrape":
        for pid, typ, t in scrape(a[0]):
            print(f"{pid}\t{typ}\t{html.unescape(t).strip()}")
    elif cmd == "match":
        skip = set(Path(a[a.index("--skip") + 1]).read_text().splitlines()) if "--skip" in a else set()
        posters = [l.split("\t") for l in Path(a[0]).read_text().splitlines() if l]
        for dest, (pid, t) in sorted(match(posters, Path(a[1]).read_text(), skip).items()):
            print(f"{pid}\t{dest}\t{t}")
    elif cmd == "fetch":
        fetch([l.split("\t") for l in Path(a[0]).read_text().splitlines() if l], a[1])
    elif cmd == "folders":
        print("\n".join(folders([l.split("\t") for l in Path(a[0]).read_text().splitlines() if l])))
    elif cmd == "silo-sql":
        print(silo_sql([l for l in Path(a[0]).read_text().splitlines() if l], a[1]))
    elif cmd == "silo-refresh":
        rows = [l.split("\t") for l in Path(a[0]).read_text().splitlines() if l]
        nfo = dict(l.split("\t")[:2] for l in Path(a[1]).read_text().splitlines() if "\t" in l)
        go, skipped = silo_targets(rows, nfo)
        for rel, cid, n, st in skipped:
            print(f"SKIP\t{rel}\tNFO tmdb {n} != Silo tmdb {st} ({cid}); fix the NFO, then refresh by hand")
        silo_refresh(go)
    elif cmd == "selftest":
        selftest()
    else:
        print(__doc__)
