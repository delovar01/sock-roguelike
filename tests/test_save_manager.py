import json

import src.persistence.save_manager as sm
from src.core import constants


def test_save_then_load_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr(sm, "SAVE_DIR", tmp_path)
    monkeypatch.setattr(sm, "SAVE_FILE", tmp_path / "slot1.json")
    sm.save_game(level_num=2, seed=999, hp=2, buttons=5)
    data = sm.load_game()
    assert data == {"level_num": 2, "seed": 999, "hp": 2, "buttons": 5}


def test_load_missing_file_returns_none(tmp_path, monkeypatch):
    monkeypatch.setattr(sm, "SAVE_FILE", tmp_path / "no_such.json")
    assert sm.load_game() is None


def test_save_creates_file(tmp_path, monkeypatch):
    monkeypatch.setattr(sm, "SAVE_DIR", tmp_path)
    monkeypatch.setattr(sm, "SAVE_FILE", tmp_path / "slot1.json")
    sm.save_game(1, 42, 3, 0)
    f = tmp_path / "slot1.json"
    assert f.exists()
    raw = json.loads(f.read_text(encoding="utf-8"))
    assert raw["seed"] == 42
