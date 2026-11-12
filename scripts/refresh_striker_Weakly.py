"""
LaLiga Match Intelligence - LIVE refresh from Striker API -> SQL Server.
Always calls the API (ignores the cache), then overwrites raw_cache/ so the
old cache-based script (load_striker.py) sees the same fresh data.

Usage:
    python refresh_striker.py               # refresh everything
    python refresh_striker.py matches       # only matches
    python refresh_striker.py matches standings leaders
Targets: teams, standings, team_stats, ratings, matches, leaders
"""

import os
import sys
import json
import requests
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

API = "https://mcp.strikerapi.com/v1/"
KEY = os.environ.get("STRIKER_API_KEY", "").strip()
SEASON = int(os.environ.get("LALIGA_SEASON", "2026"))
LEAGUE = os.environ.get("LALIGA_LEAGUE", "laliga")
CACHE = BASE_DIR / "raw_cache"
CACHE.mkdir(exist_ok=True)

DB_SERVER = os.environ.get("DB_SERVER", "DESKTOP-U7Q6F9R")
DB_NAME = os.environ.get("DB_NAME", "SpainLeague")
DB_DRIVER = os.environ.get("DB_DRIVER", "ODBC Driver 17 for SQL Server")
DB_USER = os.environ.get("DB_USER", "")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")

if DB_USER and DB_PASSWORD:
    conn_str = (f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}"
                f"?driver={DB_DRIVER.replace(' ', '+')}")
else:
    conn_str = (f"mssql+pyodbc://@{DB_SERVER}/{DB_NAME}"
                f"?driver={DB_DRIVER.replace(' ', '+')}&trusted_connection=yes")

engine = create_engine(conn_str, fast_executemany=True)

# ---------------- Safety checks (before spending any credit) ----------------
if not KEY.startswith("sk_live_") or "HERE" in KEY or len(KEY) < 40:
    sys.exit("STOP: STRIKER_API_KEY missing or invalid. Use load_striker.py for cache-only loads.")

try:
    with engine.connect() as c:
        print("Database OK:", c.execute(text("SELECT DB_NAME()")).scalar())
except Exception as e:
    sys.exit(f"STOP: cannot connect to SQL Server (no credits used).\n{e}")

HEADERS = {
    "x-api-key": KEY,
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
}

API_CALLS = 0


# ---------------- Helpers ----------------
def call_live(endpoint, body, name):
    """Always call the API. Only overwrite the cache file if the call succeeds."""
    global API_CALLS
    body = {"league": LEAGUE, **body}
    r = requests.post(API + endpoint, json=body, headers=HEADERS, timeout=60)
    API_CALLS += 1
    if not r.ok:
        print("STATUS:", r.status_code)
        print("BODY:", r.text[:500])
        sys.exit(f"STOP: API call '{name}' failed. Cache and database left untouched for it.")
    data = r.json()
    if isinstance(data, dict) and "error" in data:
        print("API ERROR:", data["error"])
        sys.exit(f"STOP: API returned an error for '{name}'. Cache kept as it was.")
    (CACHE / f"{name}.json").write_text(json.dumps(data), encoding="utf-8")
    print(f"API call:  {name}")
    return data


def get_list(data, key):
    if isinstance(data, dict) and "data" in data and key not in data:
        data = data["data"]
    if key not in data:
        sys.exit(f"STOP: key '{key}' not found. Keys present: {list(data.keys())}")
    return data[key]


def find_rows(data, key, name):
    if isinstance(data, dict) and isinstance(data.get("data"), (dict, list)) and key not in data:
        data = data["data"]
    if isinstance(data, list):
        return data
    if isinstance(data.get(key), list):
        return data[key]
    for k, v in data.items():
        if isinstance(v, list) and v and isinstance(v[0], dict):
            print(f"note: '{name}' records found under key '{k}' (expected '{key}')")
            return v
    sys.exit(f"STOP: no records found in '{name}'. Keys present: {list(data.keys())}")


def clean(df):
    df = df.copy()
    df.columns = [c.replace(".", "_") for c in df.columns]
    for col in df.columns:
        if df[col].map(lambda v: isinstance(v, (list, dict))).any():
            df[col] = df[col].map(lambda v: json.dumps(v) if isinstance(v, (list, dict)) else v)
    return df


def save(df, table):
    df = clean(df)
    if df.empty or len(df.columns) == 0:
        sys.exit(f"STOP: {table} has no data, not saving an empty table.")
    df.to_sql(table, engine, if_exists="replace", index=False)
    print(f"saved {table}: {len(df)} rows")


# ---------------- Refresh steps ----------------
def refresh_teams():
    teams = get_list(call_live("list_teams", {"season": SEASON}, "teams"), "teams")
    save(pd.json_normalize(teams), "Teams")


def refresh_standings():
    rows = get_list(call_live("get_standings", {"season": SEASON}, "standings"), "standings")
    df = pd.json_normalize(rows)
    if "rank" in df.columns:
        df = df.sort_values("rank")
    save(df, "Fact_Standings")


def refresh_team_stats():
    rows = get_list(call_live("get_team_stats", {"season": SEASON}, "team_stats"), "teams")
    save(pd.json_normalize(rows), "Fact_Team_Stats")


def refresh_ratings():
    rows = get_list(call_live("get_ratings", {"limit": 50}, "ratings"), "ratings")
    df = pd.json_normalize(rows)
    if "last_game" in df.columns:
        df["last_game"] = pd.to_datetime(df["last_game"], errors="coerce").dt.date
    save(df, "Fact_Ratings")


def refresh_matches():
    games, offset, page_no = [], 0, 0
    while True:
        page = call_live(
            "list_games",
            {"season": SEASON, "stage": "league", "limit": 110, "offset": offset},
            f"games_{offset}",
        )
        rows = find_rows(page, "games", f"games_{offset}")
        games += rows
        nxt = page.get("next_offset") if isinstance(page, dict) else None
        try:
            nxt = int(nxt) if nxt is not None else None
        except (TypeError, ValueError):
            nxt = None
        if nxt is None and len(rows) >= 110:
            nxt = offset + len(rows)
        if not rows or nxt is None or nxt <= offset:
            break
        offset = nxt
        page_no += 1

    df = pd.json_normalize(games)
    df = df.rename(columns={
        "home.team_id": "Home_Team_ID", "home.abbrev": "Home_Abbreviation",
        "home.name": "Home_Team", "home.score": "Home_Score",
        "away.team_id": "Away_Team_ID", "away.abbrev": "Away_Abbreviation",
        "away.name": "Away_Team", "away.score": "Away_Score",
    })
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
        df = df.sort_values("date")
    for c in ("Home_Score", "Away_Score"):
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").astype("Int64")
    save(df, "Fact_Matches")

    # Show what the API really returned, so you can tell if the source is behind
    if "status" in df.columns and "date" in df.columns:
        fin = df[df["status"] == "final"]
        if not fin.empty:
            print(f"last FINAL match in data: {fin['date'].max()}  ({len(fin)} final matches)")


LEADER_STATS = ["goals", "assists", "goal_contributions", "shots", "shots_on_target",
                "xg", "yellow_cards", "red_cards", "saves", "clean_sheets"]


def refresh_leaders():
    leaders = []
    for s in LEADER_STATS:
        data = call_live("get_leaders", {"season": SEASON, "stat": s, "limit": 100}, f"leaders_{s}")
        rows = find_rows(data, "leaders", f"leaders_{s}")
        for r in rows:
            r["stat"] = s
        leaders += rows
    fl = pd.DataFrame(leaders)
    save(fl, "Fact_Player_Leaders")

    # Dim_Players is derived from the leaders (0 extra API calls)
    dim = (fl[["player_id", "name", "team", "position"]]
           .dropna(subset=["player_id"]).drop_duplicates("player_id").copy())
    dim["player_id"] = dim["player_id"].astype(str)
    dim["Player_Image_URL"] = (
        "https://a.espncdn.com/i/headshots/soccer/players/full/" + dim["player_id"] + ".png")
    save(dim, "Dim_Players")


STEPS = {
    "teams": refresh_teams,
    "standings": refresh_standings,
    "team_stats": refresh_team_stats,
    "ratings": refresh_ratings,
    "matches": refresh_matches,
    "leaders": refresh_leaders,
}


def main():
    wanted = [a.lower() for a in sys.argv[1:]] or list(STEPS)
    unknown = [w for w in wanted if w not in STEPS]
    if unknown:
        sys.exit(f"Unknown target(s): {unknown}. Choose from: {list(STEPS)}")

    print("========================================")
    print("LIVE refresh:", ", ".join(wanted))
    print("========================================")
    for w in wanted:
        print(f"\n--- {w} ---")
        STEPS[w]()
    print(f"\nDONE. API calls used: {API_CALLS}. Now click Refresh in Power BI.")


if __name__ == "__main__":
    main()