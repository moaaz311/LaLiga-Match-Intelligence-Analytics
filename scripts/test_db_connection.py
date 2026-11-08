"""
Test SQL Server connectivity and verify table row counts in the SpainLeague database.
"""

import os
from pathlib import Path
from sqlalchemy import create_engine, text
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

print(f"Connecting to SQL Server ({DB_SERVER}) database '{DB_NAME}'...")
try:
    engine = create_engine(conn_str)
    with engine.connect() as con:
        db_name = con.execute(text("SELECT DB_NAME()")).scalar()
        print(f"Connected successfully to: {db_name}\n")
        
        tables = [
            "Teams",
            "Dim_Players",
            "Fact_Matches",
            "Fact_Player_Leaders",
            "Fact_Ratings",
            "Fact_Standings",
            "Fact_Team_Stats",
        ]
        
        print(f"{'Table Name':<25} | {'Row Count':<10}")
        print("-" * 38)
        for t in tables:
            try:
                cnt = con.execute(text(f"SELECT COUNT(*) FROM [{t}]")).scalar()
                print(f"{t:<25} | {cnt:<10}")
            except Exception as te:
                print(f"{t:<25} | NOT FOUND ({te})")
                
except Exception as e:
    print("Database Connection Error:", e)

