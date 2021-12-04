import json
import os

from particle import Particle

def read_models(base_path):
    models = []
    for i in range(len(os.listdir(base_path))):
        with open(base_path + "/" + str(i) + ".json", "r") as file:
            data = json.load(file)
        models.append(data)
    return models

def read_settings(key=None):
    with open("settings.json", "r") as file:
        data = json.load(file)
    return data[key] if key else data

def write_settings(key, value):
    with open("settings.json", "r") as file:
        data = json.load(file)
    data[key] = value
    with open("settings.json", "w") as file:
        json.dump(data, file, indent=4)

def spawn_particles(x, y, radius=6, amount=30):
    return [Particle(x, y, radius) for _ in range(amount)]
