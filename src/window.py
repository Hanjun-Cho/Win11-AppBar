import ctypes
import importlib
from ctypes import wintypes
from collections import defaultdict
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QSizePolicy, QLayout, QGridLayout
from PyQt5.QtCore import Qt

class APPBARDATA(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("hWnd", wintypes.HWND),
        ("uCallbackMessage", wintypes.UINT),
        ("uEdge", wintypes.UINT),
        ("rc", wintypes.RECT),
        ("lParam", wintypes.LPARAM)
    ]

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

    def set_dimensions(self, x, y, width, height):
        self.setGeometry(x,y,width,height)
        self.x      = x
        self.y      = y
        self.width  = width
        self.height = height

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height
    
class WinBar(Window):
    user32       = ctypes.windll.user32
    shell32      = ctypes.windll.shell32
    ABM_NEW      = 0x00000000  # register new AppBar
    ABM_REMOVE   = 0x00000001  # unregister AppBar
    ABM_QUERYPOS = 0x00000002  # checks input pos against screen for overlaps 
    ABM_SETPOS   = 0x00000003  # reserves queried pos on screen for AppBar
    ABE_TOP      = 1           # location: top edge of screen

    def __init__(self, height):
        super().__init__()
        screen = QApplication.primaryScreen().geometry()
        self.window = self.set_dimensions(0,0,screen.width(), height)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.appbar_data        = APPBARDATA()
        self.appbar_data.cbSize = ctypes.sizeof(APPBARDATA)
        self.appbar_data.hWnd   = int(self.winId())
        self.appbar_data.uEdge  = self.ABE_TOP

        self.appbar_data.rc.left   = 0
        self.appbar_data.rc.top    = 0
        self.appbar_data.rc.right  = self.get_width()
        self.appbar_data.rc.bottom = self.get_height()

        self.register_winbar()
        self.init_main_gui()
        self.show()

    def register_winbar(self):
        self.shell32.SHAppBarMessage(self.ABM_NEW, ctypes.byref(self.appbar_data))
        self.shell32.SHAppBarMessage(self.ABM_QUERYPOS, ctypes.byref(self.appbar_data))
        self.shell32.SHAppBarMessage(self.ABM_SETPOS, ctypes.byref(self.appbar_data))

    def init_main_gui(self):
        self.central_widget = QWidget()
        self.main_layout = QGridLayout()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.main_layout)

        self.layouts = {}
        self.layouts["left"]   = QHBoxLayout()
        self.layouts["center"] = QHBoxLayout()
        self.layouts["right"]  = QHBoxLayout()

    def register_all_components(self, components):
        count = defaultdict(int)
        for component in components:
            component_widget = component.get_widget()
            component_widget.setFixedHeight(self.element_height)
            self.layouts[component.get("alignment")].addWidget(component_widget, 0)
            count[component.get("alignment")] += 1
    
        if count["left"] == 0:
            self.main_layout.addWidget(QWidget(), 1, 1, alignment=Qt.AlignLeft)
        else:
            self.main_layout.addLayout(self.layouts["left"], 0, 1, alignment=Qt.AlignLeft)
        if count["center"] == 0:
            self.main_layout.addWidget(QWidget(), 1, 2, alignment=Qt.AlignLeft)
        else:
            self.main_layout.addLayout(self.layouts["center"], 0, 2, alignment=Qt.AlignCenter)
        if count["right"] == 0:
            self.main_layout.addWidget(QWidget(), 1, 3, alignment=Qt.AlignRight)
        else:
            self.main_layout.addLayout(self.layouts["right"], 0, 3, alignment=Qt.AlignRight)

    def set_gui_margins(self, margins):
        self.main_layout.setContentsMargins(
            margins["left"],
            margins["top"],
            margins["right"],
            margins["bottom"]
        )
        self.element_height = self.get_height() - margins["top"] - margins["bottom"]

    def closeEvent(self, event):
        self.shell32.SHAppBarMessage(self.ABM_REMOVE, ctypes.byref(self.appbar_data))
        super().closeEvent()
