import json
import os

FILE = "settings.json"

DEFAULT_SETTINGS = {
    "snake_color": [0, 255, 0],
    "grid": True,
    "sound": True
}

def load_settings():
    if not os.path.exists(FILE):
        with open(FILE, "w") as f:
            json.dump(DEFAULT_SETTINGS, f, indent=4)

    with open(FILE, "r") as f:
        return json.load(f)


def save_settings(settings):
    with open(FILE, "w") as f:
        json.dump(settings, f, indent=4)