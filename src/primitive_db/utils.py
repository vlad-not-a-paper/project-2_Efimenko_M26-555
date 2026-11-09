import json
import os

from .constants import DATA_DIR, DATA_FILE_EXTENSION, FILE_ENCODING


def load_metadata(filepath):
    """Loads metadata from a JSON file or returns an empty dict."""
    try:
        with open(filepath, "r", encoding=FILE_ENCODING) as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return {}


def save_metadata(filepath, data):
    """Saves metadata to a JSON file."""
    with open(filepath, "w", encoding=FILE_ENCODING) as file:
        json.dump(data, file)


def get_table_path(table_name):
    """Returns the path to the data file of a table."""
    return os.path.join(DATA_DIR, f"{table_name}{DATA_FILE_EXTENSION}")


def load_table_data(table_name):
    """Loads table records from its JSON file or returns an empty list."""
    try:
        with open(get_table_path(table_name), "r", encoding=FILE_ENCODING) as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return []


def save_table_data(table_name, data):
    """Saves table records to its JSON file."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(get_table_path(table_name), "w", encoding=FILE_ENCODING) as file:
        json.dump(data, file)


def delete_table_data(table_name):
    """Deletes the data file of a table if it exists."""
    try:
        os.remove(get_table_path(table_name))
    except FileNotFoundError:
        pass
