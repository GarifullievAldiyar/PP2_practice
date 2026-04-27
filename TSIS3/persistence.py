import json
import os

def load_json(filename, default):
    if not os.path.exists(filename):
        return default
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except:
        return default

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def load_settings():
    return load_json("settings.json", {
        "sound": True,
        "car_color": "red",
        "difficulty": "medium"
    })

def save_settings(settings):
    save_json("settings.json", settings)


def load_leaderboard():
    return load_json("leaderboard.json", [])

def save_leaderboard(data):
    save_json("leaderboard.json", data)

def add_score(name, score, distance):
    data = load_leaderboard()

    data.append({
        "name": name,
        "score": score,
        "distance": distance
    })

    data = sorted(data, key=lambda x: x["score"], reverse=True)[:10]

    save_leaderboard(data)