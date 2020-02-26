import json
import os

class config():

    def __init__(self):
        current_dir = os.getcwd()
        config_path = os.path.join(current_dir, "config.json")

        with open(config_path) as json_file:
            self._json_data = json.load(json_file)

    def save_dir(self):
        # save_dir = self._json_data[""][""]
        # return save_dir
        pass

