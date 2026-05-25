"""Простое сохранение/загрузка в JSON. Один слот."""

import json

from src.core.constants import SAVE_FILE, SAVE_DIR


def save_game(level_num, seed, hp, buttons, attack=1,
              score=0, kills=0, time=0.0):
    SAVE_DIR.mkdir(parents=True, exist_ok=True)
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
        SAVE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                             encoding="utf-8")
        return True
    except OSError:
        return False


def load_game():
    if not SAVE_FILE.exists():
        return None
    try:
        return json.loads(SAVE_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def delete_save():
    if SAVE_FILE.exists():
        try:
            SAVE_FILE.unlink()
            return True
        except OSError:
            return False
    return False
