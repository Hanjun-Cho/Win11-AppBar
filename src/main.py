import sys
import ctypes
from PySide6.QtWidgets import QWidget, QApplication
from winbar import Winbar

if __name__ == "__main__":
    app = QApplication([])
    screen = QApplication.primaryScreen()
    winbar = Winbar(screen)
    app.exec()
