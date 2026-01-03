import sys
import os
from configs.config_manager import ConfigManager
from configs.component_manager import ComponentManager
from PySide6.QtWidgets import QApplication
from winbar import Winbar

if __name__ == "__main__":
    config_dir = os.path.expanduser("~/Documents/Winbar")
    config_manager = ConfigManager(config_dir)
    component_manager = ComponentManager(config_dir, config_manager.get_components_config())
    app = QApplication([])

    component_manager.init_components(config_manager.get_layout_config())
    component_layout = component_manager.get_component_layout()
    screen = QApplication.primaryScreen()
    winbar = Winbar(screen, config_manager)
    winbar.populate_gui(component_layout)
    sys.exit(app.exec())
