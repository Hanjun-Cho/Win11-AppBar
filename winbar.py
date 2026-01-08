import ctypes
from PySide6.QtWidgets import QWidget, QApplication, QGridLayout, QHBoxLayout
from PySide6.QtCore import Qt
from windowsdll import APPBARDATA, AppbarRegistrationCodes, AppbarDirection, WindowsDLL
from configs.layout_config import LayoutFields
from configs.components_config import ComponentsFields

class Winbar(QWidget):
    def __init__(self, screen, config_manager):
        super().__init__()
        self.layout_config = config_manager.get_layout_config()
        winbar_component_height = self.layout_config[LayoutFields.WINBAR_COMPONENT_HEIGHT]
        winbar_top_margin = self.layout_config[LayoutFields.WINBAR_MARGINS][LayoutFields.TOP]
        winbar_bottom_margin = self.layout_config[LayoutFields.WINBAR_MARGINS][LayoutFields.BOTTOM]

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
        self.init_gui()
        self.show()

    def register_winbar(self):
        WindowsDLL.SHELL32.value.SHAppBarMessage(AppbarRegistrationCodes.NEW, ctypes.byref(self.winbar_data))
        WindowsDLL.SHELL32.value.SHAppBarMessage(AppbarRegistrationCodes.QUERYPOS, ctypes.byref(self.winbar_data))
        WindowsDLL.SHELL32.value.SHAppBarMessage(AppbarRegistrationCodes.SETPOS, ctypes.byref(self.winbar_data))

    def init_gui(self):
        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)
        self.set_gui_margins()

        self.layouts = {}
        self.layouts["LEFT"] = QHBoxLayout()
        self.layouts["CENTER"] = QHBoxLayout()
        self.layouts["RIGHT"] = QHBoxLayout()

    def set_gui_margins(self):
        self.main_layout.setContentsMargins(
            self.layout_config[LayoutFields.WINBAR_MARGINS][LayoutFields.LEFT],
            self.layout_config[LayoutFields.WINBAR_MARGINS][LayoutFields.TOP],
            self.layout_config[LayoutFields.WINBAR_MARGINS][LayoutFields.RIGHT],
            self.layout_config[LayoutFields.WINBAR_MARGINS][LayoutFields.BOTTOM],
        )

    def populate_gui(self, components):
        self.populate_gui_side(ComponentsFields.LEFT, components[ComponentsFields.LEFT])
        self.populate_gui_side(ComponentsFields.CENTER, components[ComponentsFields.CENTER])
        self.populate_gui_side(ComponentsFields.RIGHT, components[ComponentsFields.RIGHT])

    def populate_gui_side(self, side, components):
        qt_alignment = Qt.AlignCenter
        alignment_value = 2
        if side == ComponentsFields.LEFT:
            qt_alignment = Qt.AlignLeft
            alignment_value = 1
        elif side == ComponentsFields.RIGHT:
            qt_alignment = Qt.AlignRight
            alignment_value = 3

        if len(components) == 0:
            self.main_layout.addWidget(QWidget(), 1, alignment_value, alignment=qt_alignment)
            return

        for component in components:
            self.layouts[side].addWidget(component, 0)
        self.main_layout.addLayout(self.layouts[side], 0, alignment_value, alignment=qt_alignment)

    def closeEvent(self, event):
        self.shell32.value.SHAppBarMessage(AppbarRegistrationCodes.REMOVE, ctypes.byref(self.winbar_data))
        QApplication.quit()
        event.accept()
