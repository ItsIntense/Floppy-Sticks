import json
import os

class Utils(object):
    @staticmethod
    def read_models(base_path):
        models = []
        for i in range(len(os.listdir(base_path))):
            with open(base_path + "/" + str(i) + ".json", "r") as file:
                data = json.load(file)
            models.append(data)
        return models

    @staticmethod
    def read_settings(key=None):
        with open("data/config.json", "r") as file:
            data = json.load(file)
        return data[key] if key else data

    @staticmethod
    def write_settings(key, value):
        with open("data/config.json", "r") as file:
            data = json.load(file)
        data[key] = value
        with open("data/config.json", "w") as file:
            json.dump(data, file, indent=4)
