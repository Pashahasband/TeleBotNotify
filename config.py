"""
Конфигурация приложения.
Сохраняется в JSON-файл на устройстве.
"""

import json
from pathlib import Path


def _data_dir() -> Path:
    """Return a writable persistent directory for the current platform."""
    try:
        from android.storage import app_storage_path
    except ImportError:
        return Path.home() / ".tgmonitor"
    return Path(app_storage_path())


DATA_DIR = _data_dir()
DATA_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_FILE = DATA_DIR / "monitor_config.json"


def default_config() -> dict:
    return {
        "telethon_api_id": "",
        "telethon_api_hash": "",
        "telethon_phone": "",
        "bot_token": "",
        "channels": "",
        "target_phrase": "",
        "session_name": "monitor_session",
    }


def load_config() -> dict:
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return default_config()


def save_config(data: dict):
    temporary_file = CONFIG_FILE.with_suffix(".tmp")
    with open(temporary_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    temporary_file.replace(CONFIG_FILE)
