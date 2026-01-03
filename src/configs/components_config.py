from configs.config import Config
from configs.config_file_names import ConfigFileNames
from enum import StrEnum 

class ComponentsFields(StrEnum):
    LEFT = "LEFT"
    CENTER = "CENTER"
    RIGHT = "RIGHT"

class Components(Config):
    def __init__(self, config_path, current_dir):
        super().__init__(ConfigFileNames.COMPONENTS, config_path, current_dir)
