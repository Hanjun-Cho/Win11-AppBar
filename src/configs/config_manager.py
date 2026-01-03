import os
import shutil
from configs.layout_config import Layout

class ConfigManager():
    def __init__(self):
        self.config_dir = os.path.expanduser("~/Documents/Winbar")
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        if not os.path.exists(self.config_dir):
            os.mkdir(self.config_dir)

            # copies default config into config folder
            default_config_dir = self.current_dir + "/default"
            shutil.copytree(default_config_dir, self.config_dir, dirs_exist_ok=True)
        
        self.layout_config_path = self.config_dir + "/layout.json"
        self.layout_config = Layout(self.layout_config_path, self.current_dir)

    def get_layout_config(self):
        return self.layout_config.get_config()
