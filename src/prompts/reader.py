from pathlib import Path

from src.core.settings import settings

BASE_DIR = Path(__file__).resolve().parents[2]

system_prompt_path = BASE_DIR / settings.system_prompt_path / "SYSTEM_PROMPT.md"


def read_system_prompt():
    with open(system_prompt_path, "r") as file:
        return file.read()
