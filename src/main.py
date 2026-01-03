from ctypes import wintypes 
import sys
import random
import ctypes
from PySide6 import QtCore 
from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import Qt
from enum import Enum

class APPBARDATA(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("hWnd", wintypes.HWND),
        ("uCallbackMessage", wintypes.UINT),
        ("uEdge", wintypes.UINT),
        ("rc", wintypes.RECT),
        ("lParam", wintypes.LPARAM)
    ]

class AppbarRegistrationCodes(Enum):
    NEW       = 0x00000000
    REMOVE    = 0x00000001
    QUERYPOS  = 0x00000002
    SETPOS    = 0x00000003

class AppbarDirection(Enum):
    LEFT   = 0
    TOP    = 1
    RIGHT  = 2
    BOTTOM = 3

class WindowsDLL(Enum):
    USER32  = ctypes.windll.user32
    SHELL32 = ctypes.windll.shell32

class Winbar(QWidget):
    def __init__(self, screen):
        super().__init__()
        self.winbar_width  = screen.geometry().width()
        self.winbar_height = 50
        
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setGeometry(0, 0, self.winbar_width, self.winbar_height)

        self.winbar_data = APPBARDATA()
        self.winbar_data.cbSize = ctypes.sizeof(APPBARDATA)
        self.winbar_data.hWnd = int(self.winId())
        # sets the winbar to a side of the primary screen
        self.winbar_data.uEdge = AppbarDirection.TOP

        self.winbar_data.rc.left = 0
        self.winbar_data.rc.top = 0
        self.winbar_data.rc.right = self.winbar_width
        self.winbar_data.rc.bottom = self.winbar_height

    def register_winbar(self):
        WindowsDLL.SHELL32.SHAppBarMessage(AppbarRegistrationCodes.NEW, ctypes.byref(self.winbar_data))
        WindowsDLL.SHELL32.SHAppBarMessage(AppbarRegistrationCodes.QUERYPOS, ctypes.byref(self.winbar_data))
        WindowsDLL.SHELL32.SHAppBarMessage(AppbarRegistrationCodes.SETPOS, ctypes.byref(self.winbar_data))

    def closeEvent(self, event):
        self.shell32.SHAppBarMessage(AppbarRegistrationCodes.REMOVE, ctypes.byref(self.winbar_data))
        QApplication.quit()
        event.accept()

if __name__ == "__main__":
    app = QApplication([])
    screen = QApplication.primaryScreen()
    
    winbar = Winbar(screen)
    winbar.show()

    app.exec()
