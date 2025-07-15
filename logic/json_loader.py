# logic/json_loader.py
import json

def load_json(path):
    """Loads a JSON file and returns a Python dictionary."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Failed to load JSON: {e}")
        return {}

def save_json(path, data):
    """Saves a Python dictionary as a JSON file."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Failed to save JSON: {e}")
