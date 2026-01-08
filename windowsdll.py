import ctypes
from ctypes import wintypes 
from enum import Enum, IntEnum

class APPBARDATA(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("hWnd", wintypes.HWND),
        ("uCallbackMessage", wintypes.UINT),
        ("uEdge", wintypes.UINT),
        ("rc", wintypes.RECT),
        ("lParam", wintypes.LPARAM)
    ]

class AppbarRegistrationCodes(IntEnum):
    NEW       = 0x00000000
    REMOVE    = 0x00000001
    QUERYPOS  = 0x00000002
    SETPOS    = 0x00000003

class AppbarDirection(IntEnum):
    LEFT   = 0
    TOP    = 1
    RIGHT  = 2
    BOTTOM = 3

class WindowsDLL(Enum):
    USER32  = ctypes.windll.user32
    SHELL32 = ctypes.windll.shell32
