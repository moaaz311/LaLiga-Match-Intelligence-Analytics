"""
Validate Striker API key format and environment configuration.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

k = os.environ.get("STRIKER_API_KEY", "")
print("STRIKER_API_KEY found:", bool(k))
if k:
    print("Length:", len(k))
    print("Prefix:", k[:8])
    print("Suffix:", k[-4:])
    print("Valid format:", k.startswith("sk_live_") and len(k) >= 40)
    print("Has unwanted spaces/quotes:", any(c in k for c in ' "\''))
else:
    print("Please set STRIKER_API_KEY in your .env file or environment.")

