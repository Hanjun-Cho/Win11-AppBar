from configs.config_manager import ConfigManager
from PySide6.QtWidgets import QApplication
from winbar import Winbar

if __name__ == "__main__":
    config_manager = ConfigManager()

    app = QApplication([])
    screen = QApplication.primaryScreen()
    winbar = Winbar(screen, config_manager)
    app.exec()
