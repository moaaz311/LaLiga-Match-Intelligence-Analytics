"""
Check player image availability via ESPN CDN headshot URLs.
Reads player IDs from Dim_Players, validates HTTP responses,
and records verification flags to photo_check.csv.
"""

import os
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import requests
from sqlalchemy import create_engine
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

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

# ---- 1) Does the API already give a photo field? (reads local cache, 0 credits) ----
f = BASE_DIR / "raw_cache" / "leaders_goals.json"
if f.exists():
    data = json.loads(f.read_text(encoding="utf-8"))
    rows = data.get("leaders") or next((v for v in data.values() if isinstance(v, list)), [])
    if rows:
        print("Fields in one leaders record:", list(rows[0].keys()))
        print("First record:", json.dumps(rows[0], ensure_ascii=False)[:400])
    print()

# ---- 2) Does ESPN have a real picture for each player_id? ----
df = pd.read_sql("SELECT player_id, name, team, Player_Image_URL FROM Dim_Players", engine)


def has_image(url):
    try:
        r = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        ctype = r.headers.get("Content-Type", "")
        # A real headshot is an image of a few KB; placeholder responses are tiny or not images
        return r.status_code == 200 and ctype.startswith("image") and len(r.content) > 2000
    except Exception:
        return False


print(f"Checking images for {len(df)} players using ThreadPoolExecutor...")
with ThreadPoolExecutor(max_workers=12) as pool:
    df["has_photo"] = list(pool.map(has_image, df["Player_Image_URL"]))

total, ok = len(df), int(df["has_photo"].sum())
print(f"Players with a real ESPN photo: {ok} of {total} ({ok / total:.0%})")

top = pd.read_sql(
    "SELECT TOP 25 player_id, name, team, value FROM Fact_Player_Leaders "
    "WHERE stat = 'goals' ORDER BY value DESC", engine)
top["player_id"] = top["player_id"].astype(str)
df["player_id"] = df["player_id"].astype(str)
top = top.merge(df[["player_id", "has_photo"]], on="player_id", how="left")
print("\nTop 25 scorers:")
print(top[["name", "team", "value", "has_photo"]].to_string(index=False))

out_csv = BASE_DIR / "data" / "mappings" / "photo_check.csv"
out_csv.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(out_csv, index=False, encoding="utf-8-sig")
# also keep in root for compatibility
df.to_csv(BASE_DIR / "photo_check.csv", index=False, encoding="utf-8-sig")
print(f"\nSaved {out_csv}")

