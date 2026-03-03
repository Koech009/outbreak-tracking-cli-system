# Handles JSON file reading and writing safely.

import json
import os


def load_json(file_path: str) -> list:
    """
    Safely load JSON data from a file.
    If file does not exist or is corrupted,
    return an empty list.
    """
    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        # If file is corrupted
        return []


def save_json(file_path: str, data: list) -> None:
    """
    Save data to JSON file with indentation.
    """
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
