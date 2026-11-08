"""
Fetch, normalize, and match player headshots from TheSportsDB API.
Cross-references with ESPN verified links, validates image URLs,
and updates Dim_Players in SQL Server.
"""

import os
import json
import re
import time
import unicodedata
from pathlib import Path

import pandas as pd
import requests
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# TheSportsDB API key (test key "123" or custom key from env)
KEY = os.environ.get("THESPORTSDB_API_KEY", "123")
SEARCH = f"https://www.thesportsdb.com/api/v1/json/{KEY}/searchplayers.php"
CACHE = BASE_DIR / "photo_cache"
CACHE.mkdir(exist_ok=True)

DB_SERVER = os.environ.get("DB_SERVER", "DESKTOP-U7Q6F9R")
DB_NAME = os.environ.get("DB_NAME", "SpainLeague")
DB_DRIVER = os.environ.get("DB_DRIVER", "ODBC Driver 17 for SQL Server")
DB_USER = os.environ.get("DB_USER", "")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")

if DB_USER and DB_PASSWORD:
    conn_str = f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}?driver={DB_DRIVER.replace(' ', '+')}"
else:
    conn_str = f"mssql+pyodbc://@{DB_SERVER}/{DB_NAME}?driver={DB_DRIVER.replace(' ', '+')}&trusted_connection=yes"

engine = create_engine(conn_str)


def norm(s):
    """Normalize string: NFKD decomposition, strip accents, remove non-alphanumeric, lowercase."""
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", s.lower())


def has_image(url):
    """Validate image availability and file content length."""
    try:
        r = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        return r.status_code == 200 and r.headers.get("Content-Type", "").startswith("image") and len(r.content) > 2000
    except Exception:
        return False


def search(name):
    """Search player on TheSportsDB API with rate-limiting and local JSON caching."""
    f = CACHE / f"{norm(name)}.json"
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8"))
    for attempt in range(4):
        r = requests.get(
            SEARCH, params={"p": name}, timeout=30,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", "Accept": "application/json"},
        )
        if r.status_code == 429:
            time.sleep(30)
            continue
        if not r.ok:
            print("STATUS:", r.status_code)
            print("BODY:", r.text[:400])
            raise SystemExit("STOP: the photo source refused the request. Database not changed.")
        data = r.json()
        f.write_text(json.dumps(data), encoding="utf-8")
        time.sleep(2.2)  # Respect free-tier rate limit
        return data
    return {}


def main():
    players = pd.read_sql("SELECT player_id, name, team FROM Dim_Players", engine)
    players["player_id"] = players["player_id"].astype(str)
    teams = pd.read_sql("SELECT abbrev, name, display_name, short_name FROM Teams", engine)
    club_names = {
        r.abbrev: {norm(x) for x in (r.name, r.display_name, r.short_name) if x}
        for r in teams.itertuples()
    }

    # ESPN links that really work (from photo_check.csv), prioritized
    espn_ok = {}
    check_csv = BASE_DIR / "data" / "mappings" / "photo_check.csv"
    if not check_csv.exists():
        check_csv = BASE_DIR / "photo_check.csv"
    if check_csv.exists():
        chk = pd.read_csv(check_csv, dtype={"player_id": str})
        espn_ok = dict(zip(chk.loc[chk.has_photo, "player_id"], chk.loc[chk.has_photo, "Player_Image_URL"]))

    results = []
    print(f"Matching photos for {len(players)} players...")
    for i, p in enumerate(players.itertuples(), 1):
        if p.player_id in espn_ok:
            results.append((p.player_id, p.name, espn_ok[p.player_id], "espn"))
            continue
        found = (search(p.name) or {}).get("player") or []
        url, status = None, "no match"
        for c in found:
            same_name = norm(c.get("strPlayer")) == norm(p.name)
            their_team = norm(c.get("strTeam"))
            same_club = any(n and (n in their_team or their_team in n) for n in club_names.get(p.team, set()) if their_team)
            pic = c.get("strCutout") or c.get("strThumb") or c.get("strRender")
            if same_name and same_club and pic and has_image(pic):
                url, status = pic, "verified"
                break
            if same_name and pic:
                status = "name only (club differs) - not used"
        results.append((p.player_id, p.name, url, status))
        if i % 25 == 0:
            print(f"  {i}/{len(players)} checked")

    res = pd.DataFrame(results, columns=["player_id", "name", "photo_url", "status"])
    map_csv = BASE_DIR / "data" / "mappings" / "photo_map.csv"
    map_csv.parent.mkdir(parents=True, exist_ok=True)
    res.to_csv(map_csv, index=False, encoding="utf-8-sig")
    res.to_csv(BASE_DIR / "photo_map.csv", index=False, encoding="utf-8-sig")
    print("\nPhoto Matching Results:")
    print(res["status"].value_counts().to_string())

    # Write the verified URLs into Dim_Players. Everyone else becomes NULL, so dashboard shows club initials.
    with engine.begin() as con:
        con.execute(text("UPDATE Dim_Players SET Player_Image_URL = NULL"))
        con.execute(
            text("UPDATE Dim_Players SET Player_Image_URL = :u WHERE player_id = :p"),
            [{"u": r.photo_url, "p": r.player_id} for r in res.itertuples() if isinstance(r.photo_url, str) and r.photo_url],
        )
    print("Dim_Players updated successfully in SQL Server.")


if __name__ == "__main__":
    main()

