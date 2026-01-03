import ctypes
from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import Qt
from windowsdll import APPBARDATA, AppbarRegistrationCodes, AppbarDirection, WindowsDLL
from configs.layout_config import LayoutFields

class Winbar(QWidget):
    def __init__(self, screen, config_manager):
        super().__init__()
        layout_config = config_manager.get_layout_config()
        winbar_component_height = layout_config[LayoutFields.WINBAR_COMPONENT_HEIGHT]
        winbar_top_margin = layout_config[LayoutFields.WINBAR_MARGINS][LayoutFields.TOP]
        winbar_bottom_margin = layout_config[LayoutFields.WINBAR_MARGINS][LayoutFields.BOTTOM]

        self.winbar_height = winbar_component_height + winbar_top_margin + winbar_bottom_margin
        self.winbar_width  = screen.geometry().width()
        
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
