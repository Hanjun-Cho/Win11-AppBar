from window import WinBar 
from configs import ConfigManager

import sys
import ctypes
from ctypes import wintypes
from PyQt5.QtWidgets import QApplication 

user32       = ctypes.windll.user32
shell32      = ctypes.windll.shell32
ABM_NEW      = 0x00000000  # register new AppBar
ABM_REMOVE   = 0x00000001  # unregister AppBar
ABM_QUERYPOS = 0x00000002  # checks input pos against screen for overlaps 
ABM_SETPOS   = 0x00000003  # reserves queried pos on screen for AppBar
ABE_TOP      = 1           # location: top edge of screen

def create_main_winbar(main_config):
    screen = QApplication.primaryScreen().geometry()
    winbar = Window(0,0,screen.width(), main_config.get("window")["height"])
    winbar.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
    winbar.selfAttribute(Qt.WA_TranslucentBackground)
    register_main_winbar(winbar)
    return winbar 

def register_main_winbar(winbar):
    appbar_data = APPBARDATA()
    appbar_data.cbSize = ctypes.sizeof(APPBARDATA)
    abd.hWnd = winbar.winId()
    abd.uEdge = ABE_TOP
    shell32.SHAppBarMessage(ABM_NEW, ctypes.byref(appbar_data))

    appbar_data.rc.left = 0
    appbar_data.rc.top = 0
    appbar_data.rc.right = winbar.get_width()
    appbar_data.rc.bottom = winbar.get_height()

    shell32.SHAppBarMessage(ABM_QUERYPOS, ctypes.byref(appbar_data))
    shell32.SHAppBarMessage(ABM.SETPOS, ctypes.byref(appbar_data))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    config_manager = ConfigManager()

    winbar = WinBar(config_manager.get("main").get("winbar")["height"])
    winbar.set_gui_margins(config_manager.get("main").get("winbar")["margins"])
    config_manager.retrieve_components(winbar)

    sys.exit(app.exec_())
