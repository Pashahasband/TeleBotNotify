"""
Конфигурация приложения.
Сохраняется в JSON-файл на устройстве.
"""

import json
import os
from pathlib import Path

CONFIG_FILE = Path("monitor_config.json")


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
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
