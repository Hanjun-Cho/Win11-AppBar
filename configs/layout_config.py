from configs.config import Config
from configs.config_file_names import ConfigFileNames
from enum import StrEnum

class LayoutFields(StrEnum):
    WINBAR_COMPONENT_HEIGHT = "winbar_component_height"
    WINBAR_MARGINS = "winbar_margins"
    LEFT = "left"
    RIGHT = "right"
    TOP = "top"
    BOTTOM = "bottom"
    GLOBAL_FONT = "global_font"
    GLOBAL_FONT_SIZE = "global_font_size"

class Layout(Config):
    def __init__(self, config_path, current_dir):
        super().__init__(ConfigFileNames.LAYOUT, config_path, current_dir)
