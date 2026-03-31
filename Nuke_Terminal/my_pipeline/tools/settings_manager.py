import os
import json


DEFAULT_BASE_PATH = r"C:\Projects"


def get_config_dir():
    current_dir = os.path.dirname(__file__)
    my_pipeline_dir = os.path.dirname(current_dir)
    config_dir = os.path.join(my_pipeline_dir, "config")
    return config_dir


def get_settings_file():
    return os.path.join(get_config_dir(), "settings.json")


def ensure_config_dir():
    config_dir = get_config_dir()
    os.makedirs(config_dir, exist_ok=True)


def load_settings():
    ensure_config_dir()
    settings_file = get_settings_file()

    if not os.path.exists(settings_file):
        return {
            "base_path": DEFAULT_BASE_PATH
        }

    try:
        with open(settings_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {
                "base_path": data.get("base_path", DEFAULT_BASE_PATH)
            }
    except Exception:
        return {
            "base_path": DEFAULT_BASE_PATH
        }


def save_settings(settings_dict):
    ensure_config_dir()
    settings_file = get_settings_file()

    with open(settings_file, "w", encoding="utf-8") as f:
        json.dump(settings_dict, f, indent=4)


def get_base_path():
    settings = load_settings()
    return settings.get("base_path", DEFAULT_BASE_PATH)


def set_base_path(new_base_path):
    settings = load_settings()
    settings["base_path"] = new_base_path
    save_settings(settings)