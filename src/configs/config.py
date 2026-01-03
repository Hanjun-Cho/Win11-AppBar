import os
import shutil
import json

class Config():
    def __init__(self, file_name, config_path, current_dir):
        if not os.path.exists(config_path):
            default_config_path = current_dir + "/default/" + file_name
            shutil.copyfile(default_config_path, config_path)

        with open(config_path, 'r') as f:
            self.data = json.load(f)

    def get_config(self):
        return self.data
