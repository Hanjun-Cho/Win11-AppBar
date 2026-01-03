import ctypes
from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import Qt
from windowsdll import APPBARDATA, AppbarRegistrationCodes, AppbarDirection, WindowsDLL

class Winbar(QWidget):
    def __init__(self, screen):
        super().__init__()
        self.winbar_width  = screen.geometry().width()
        self.winbar_height = 50
        
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
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

        # gives Windows Winbar data to reserve space at desired position
        self.register_winbar()
        self.show()

    def register_winbar(self):
        WindowsDLL.SHELL32.value.SHAppBarMessage(AppbarRegistrationCodes.NEW, ctypes.byref(self.winbar_data))
        WindowsDLL.SHELL32.value.SHAppBarMessage(AppbarRegistrationCodes.QUERYPOS, ctypes.byref(self.winbar_data))
        WindowsDLL.SHELL32.value.SHAppBarMessage(AppbarRegistrationCodes.SETPOS, ctypes.byref(self.winbar_data))

    def closeEvent(self, event):
        self.shell32.value.SHAppBarMessage(AppbarRegistrationCodes.REMOVE, ctypes.byref(self.winbar_data))
        QApplication.quit()
        event.accept()
