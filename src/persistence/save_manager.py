"""Сохранение и загрузка в JSON. Один слот."""

import os
import json

from src.core.constants import SAVE_FILE, SAVE_DIR


def save_game(level_num, seed, hp, buttons, attack=1,
              score=0, kills=0, time=0.0):
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
    data = {
        "level_num": level_num,
        "seed": seed,
        "hp": hp,
        "buttons": buttons,
        "attack": attack,
        "score": score,
        "kills": kills,
        "time": time,
    }
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except OSError:
        return False


def load_game():
    if not os.path.exists(SAVE_FILE):
        return None
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None
