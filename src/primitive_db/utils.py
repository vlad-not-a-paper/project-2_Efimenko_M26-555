import json


def load_metadata(filepath):
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        return {}


def save_metadata(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f)
