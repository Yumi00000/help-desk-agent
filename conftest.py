import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Tests must run without a real .env (fresh clone, CI): fall back to the example values
if not (BASE_DIR / ".env").exists():
    for line in (BASE_DIR / ".env.example").read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())
