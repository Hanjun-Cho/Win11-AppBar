import sys
import ctypes
from ctypes import wintypes
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy, QGridLayout 
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QFont
from widgets import ClockContainer, QuickStartContainer

# accessing the core windows libraries needed
user32 = ctypes.windll.user32
shell32 = ctypes.windll.shell32

# declaring AppBar Message hex codes
ABM_NEW      = 0x00000000  # register new AppBar
ABM_REMOVE   = 0x00000001  # unregister AppBar
ABM_QUERYPOS = 0x00000002  # checks input pos against screen for overlaps 
ABM_SETPOS   = 0x00000003  # reserves queried pos on screen for AppBar
ABE_TOP = 1  # Location: top edge of screen

# AppBar Constants
APPBAR_HEIGHT = 50

class APPBARDATA(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("hWnd", wintypes.HWND),
        ("uCallbackMessage", wintypes.UINT),
        ("uEdge", wintypes.UINT),
        ("rc", wintypes.RECT),
        ("lParam", wintypes.LPARAM)
    ]

class AppBarWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # sets this AppBar as a borderless window that doesn't show up on the taskbar
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        # sets window as completely transparent
        self.setAttribute(Qt.WA_TranslucentBackground)

        # returns the dimensions of the screen and sets current QMainWindow dimensions
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(0, 0, screen.width(), APPBAR_HEIGHT)

        self.create_appbar_gui()

        self.register_appbar()

    def create_appbar_gui(self):
        # initializes a central widget within current QMainWindow
        central_widget_container = QWidget()
        self.setCentralWidget(central_widget_container)

        # creates a horizontally stacked widget layout and sets it as the layout of the central widget
        main_layout = QGridLayout()
        main_layout.setContentsMargins(10,0,10,0)
        central_widget_container.setLayout(main_layout)

        main_layout.addWidget(QuickStartContainer(), 0, 0, alignment=Qt.AlignLeft)
        main_layout.addWidget(ClockContainer(), 0, 1, alignment=Qt.AlignCenter)
        main_layout.addWidget(QWidget(), 0, 2)
        main_layout.setColumnStretch(0,1)
        main_layout.setColumnStretch(1,0)
        main_layout.setColumnStretch(2,1)

    def register_appbar(self):
        hwnd = int(self.winId())

        abd = APPBARDATA()
        abd.cbSize = ctypes.sizeof(APPBARDATA)
        abd.hWnd = hwnd
        abd.uEdge = ABE_TOP

        shell32.SHAppBarMessage(ABM_NEW, ctypes.byref(abd))

        screen = QApplication.primaryScreen().geometry()
        abd.rc.left = 0
        abd.rc.top = 0
        abd.rc.right = screen.width()
        abd.rc.bottom = APPBAR_HEIGHT 

        shell32.SHAppBarMessage(ABM_QUERYPOS, ctypes.byref(abd))
        shell32.SHAppBarMessage(ABM_SETPOS, ctypes.byref(abd))

        self.setGeometry(QRect(
            abd.rc.left, abd.rc.top,
            abd.rc.right - abd.rc.left,
            abd.rc.bottom - abd.rc.top
        ))

    def closeEvent(self, event):
        abd = APPBARDATA()
        abd.cbSize = ctypes.sizeof(APPBARDATA)
        abd.hWnd = int(self.winId())
        shell32.SHAppBarMessage(ABM_REMOVE, ctypes.byref(abd))
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppBarWindow()
    window.show()
    sys.exit(app.exec_())
