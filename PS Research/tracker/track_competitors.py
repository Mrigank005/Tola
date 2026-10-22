"""Competitor tracker: snapshot every PS03 repo in repos.json, find new ones, and report what changed.

Each run writes snapshots/<today>.json and prints a Markdown change report against the latest earlier snapshot.
Metadata comes from batched repository searches, READMEs from raw.githubusercontent.com (no API quota), and
commits only for repos pushed since the previous snapshot. Without GITHUB_TOKEN, GitHub allows 60 core calls/hour.

Usage: python track_competitors.py [--since YYYY-MM-DD] [--no-commits]
"""
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

HERE = Path(__file__).parent
SNAPS = HERE / "snapshots"
SNAPS.mkdir(exist_ok=True)
CONFIG = json.loads((HERE / "repos.json").read_text(encoding="utf-8"))
API = "https://api.github.com"
HEADERS = {"Accept": "application/vnd.github+json", "User-Agent": "tola-tracker"}
if os.environ.get("GITHUB_TOKEN"):
    HEADERS["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
SEARCH_PAUSE = 2 if "Authorization" in HEADERS else 7  # search API: 30/min with a token, 10/min without
DISCOVERY_SINCE = "2026-09-20"


def get(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.load(r)


def search(q, per_page=100):
    time.sleep(SEARCH_PAUSE)
    return get(f"{API}/search/repositories?" + urllib.parse.urlencode({"q": q, "per_page": per_page}))["items"]


def slim(d):
    return {
        "full_name": d["full_name"], "created": d["created_at"][:10], "pushed": d["pushed_at"],
        "stars": d["stargazers_count"], "branch": d["default_branch"], "homepage": d.get("homepage") or "",
        "description": (d.get("description") or "")[:200],
    }


def fetch_meta(names):
    """Batched search by repo: qualifier; a batch that fails (renamed or deleted repo) falls back to per-repo GETs."""
    meta = {}
    for i in range(0, len(names), 8):
        batch = names[i:i + 8]
        try:
            for it in search(" ".join("repo:" + n for n in batch)):
                meta[it["full_name"].lower()] = slim(it)
            missing = [n for n in batch if n.lower() not in meta]
        except urllib.error.HTTPError:
            missing = batch
        for n in missing:
            try:
                meta[n.lower()] = slim(get(f"{API}/repos/{n}"))  # follows renames
            except urllib.error.HTTPError as e:
                meta[n.lower()] = {"full_name": n, "gone": e.code}
    return {n: meta[n.lower()] for n in names}


def readme(name, branch):
    for f in ("README.md", "readme.md", "Readme.md", "README"):
        try:
            with urllib.request.urlopen(f"https://raw.githubusercontent.com/{name}/{branch}/{f}", timeout=40) as r:
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError:
            pass
    return ""


def commits_since(name, since):
    try:
        cs = get(f"{API}/repos/{name}/commits?" + urllib.parse.urlencode({"since": since + "T00:00:00Z", "per_page": 100}))
    except urllib.error.HTTPError:  # 409 = empty repo
        return []
    return [{"date": c["commit"]["author"]["date"][:10], "msg": c["commit"]["message"].splitlines()[0][:120]} for c in cs]


def discover(known):
    found = {}
    for q in CONFIG["discovery_queries"]:
        for it in search(f"{q} created:>={DISCOVERY_SINCE}"):
            if it["full_name"].lower() not in known:
                found[it["full_name"]] = slim(it)
    return found


def main():
    args = sys.argv[1:]
    today = date.today().isoformat()
    previous = sorted(p for p in SNAPS.glob("*.json") if p.stem != today)
    prev = json.loads(previous[-1].read_text(encoding="utf-8")) if previous else {"date": "2026-10-13", "repos": {}}
    since = args[args.index("--since") + 1] if "--since" in args else prev["date"]

    names = list(CONFIG["competitors"])
    known = {n.lower() for n in names} | {n.lower() for n in CONFIG["ignore"]}
    meta = fetch_meta(names)
    for n, m in meta.items():
        if "gone" in m:
            continue
        text = readme(m["full_name"], m["branch"])
        m["readme_sha"] = hashlib.sha256(text.encode()).hexdigest()[:12]
        m["readme_len"] = len(text)
        if "--no-commits" not in args and m["pushed"][:10] >= since:
            m["commits"] = commits_since(m["full_name"], since)
    new = discover(known)
    (SNAPS / f"{today}.json").write_text(json.dumps({"date": today, "since": since, "repos": meta, "new": new}, indent=1), encoding="utf-8")

    print(f"# Competitor changes, {since} -> {today}\n")
    print("| Repo | Tier | Pushed | Commits | README | Latest commit |\n|---|---|---|---|---|---|")
    for n in sorted(names, key=lambda n: (CONFIG["competitors"][n]["tier"], n.lower())):
        m, old, tier = meta[n], prev["repos"].get(n, {}), CONFIG["competitors"][n]["tier"]
        if "gone" in m:
            print(f"| {n} | {tier} | **HTTP {m['gone']} (gone)** | | | |")
            continue
        renamed = f" (now {m['full_name']})" if m["full_name"].lower() != n.lower() else ""
        cs = m.get("commits", [])
        rd = "new" if not old else ("changed" if old.get("readme_sha") != m["readme_sha"] else "same")
        print(f"| {n}{renamed} | {tier} | {m['pushed'][:10]} | {len(cs) or ''} | {rd} | {cs[0]['msg'] if cs else ''} |")
    print(f"\n## Not yet in repos.json ({len(new)})\n")
    for n, m in sorted(new.items(), key=lambda kv: kv[1]["created"]):
        print(f"- [{n}](https://github.com/{n}) created {m['created']}, pushed {m['pushed'][:10]}: {m['description'][:120]}")
    print("\nTriage each new repo into repos.json (competitors with a tier, or ignore).", file=sys.stderr)


if __name__ == "__main__":
    main()
