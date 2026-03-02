import pytest
import json
import os
from utils import file_handler


def test_load_json_missing_file(tmp_path):
    file_path = tmp_path / "missing.json"
    data = file_handler.load_json(str(file_path))
    assert data == []  # should return empty list if file doesn't exist


def test_load_json_valid_file(tmp_path):
    file_path = tmp_path / "valid.json"
    sample_data = [{"id": "1", "name": "Test"}]
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(sample_data, f)

    data = file_handler.load_json(str(file_path))
    assert data == sample_data


def test_load_json_corrupted_file(tmp_path):
    file_path = tmp_path / "corrupted.json"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("{invalid json}")

    data = file_handler.load_json(str(file_path))
    assert data == []  # should return empty list if corrupted


def test_save_json_and_reload(tmp_path):
    file_path = tmp_path / "save.json"
    sample_data = [{"id": "2", "name": "Saved"}]

    file_handler.save_json(str(file_path), sample_data)

    # Reload to verify
    with open(file_path, "r", encoding="utf-8") as f:
        loaded = json.load(f)

    assert loaded == sample_data


def test_save_json_overwrites_existing(tmp_path):
    file_path = tmp_path / "overwrite.json"
    initial_data = [{"id": "3", "name": "Initial"}]
    new_data = [{"id": "4", "name": "Updated"}]

    # Save initial
    file_handler.save_json(str(file_path), initial_data)

    # Overwrite with new data
    file_handler.save_json(str(file_path), new_data)

    with open(file_path, "r", encoding="utf-8") as f:
        loaded = json.load(f)

    assert loaded == new_data
