import os
import shutil
from configs.components_config import Components
from configs.layout_config import Layout
from configs.config_file_names import ConfigFileNames

class ConfigManager():
    def __init__(self, config_dir):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        if not os.path.exists(config_dir):
            os.mkdir(config_dir)

            # copies default config into config folder
            default_config_dir = self.current_dir + "/default"
            shutil.copytree(default_config_dir, config_dir, dirs_exist_ok=True)
        
        self.layout_config_path = config_dir + "/" + ConfigFileNames.LAYOUT
        self.layout_config = Layout(self.layout_config_path, self.current_dir)

        self.components_config_path = config_dir + "/" + ConfigFileNames.COMPONENTS
        self.components_config = Components(self.components_config_path, self.current_dir)

    def get_layout_config(self):
        return self.layout_config.get_config()
    
    def get_components_config(self):
        return self.components_config.get_config()
