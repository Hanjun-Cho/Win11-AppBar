import ctypes
from ctypes import wintypes
import win32api
import locale
from PySide6.QtCore import QTimer, Qt, QPropertyAnimation, QEasingCurve, Property
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QWidget, QHBoxLayout
from customQt.colorAnimatedClickableLabel import ColorAnimatedClickableLabel
from configs.layout_config import LayoutFields
from windowsdll import WindowsDLL

class LanguageControlText(ColorAnimatedClickableLabel):
    def __init__(self, font_size, size):
        self.hover = False
        self.border = size // 2
        self.font_size = font_size

        super().__init__(content=self.get_current_language_name(), start_color="#222222")
        self.setFixedSize(size, size)
        self.setAlignment(Qt.AlignCenter)

        self.layout_list = win32api.GetKeyboardLayoutList()
        mapped_layout = list(map(lambda layout: layout & 0xFFF, self.layout_list))
        self.layout_index = mapped_layout.index(self.current_lid)

        self.update()
        self.clicked.connect(self.on_click)

    def get_default_style(self):
        return f"""
            color: {"black" if self.hover else "white"};
            font-size: {self.font_size}px;
            border-radius: {self.border}px;
        """

    def get_current_language_name(self):
        try:
            hwnd = WindowsDLL.USER32.value.GetForegroundWindow()
            thread_id = WindowsDLL.USER32.value.GetWindowThreadProcessId(hwnd, None)
            klid = WindowsDLL.USER32.value.GetKeyboardLayout(thread_id) 
            lid = klid & (2 ** 16 - 1)

            locale_code = locale.windows_locale[lid]
            self.current_lid = lid

            return locale_code.split("_")[1]
        except Exception:
            raise Exception("failed to get current language")

    def update(self):
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.setText(self.get_current_language_name()))
        self.timer.start(100)

    # ------------ mouse events ---------
    def enterEvent(self, event):
        super().enterEvent(event)
        self.animate_color(QColor("#8cd49e"))
        self.hover = True

    def leaveEvent(self, event):
        # TODO: This is giving the CPP Property Error
        super().leaveEvent(event)
        self.animate_color(QColor("#222222"))
        self.hover = False

    def on_click(self):
        self.layout_index = (self.layout_index + 1) % len(self.layout_list)
        locale_id = self.layout_list[self.layout_index] & (2 ** 16 - 1)
        self.current_lid = locale_id
        WindowsDLL.USER32.value.ActivateKeyboardLayout(wintypes.HKL(locale_id), 0)

class LanguageControlLabel(QWidget):
    def __init__(self, size, font_size):
        self.border = size // 2
        self.hover = False
        self.size = size
        self.font_size = font_size
        self.margins = 3
        self.language_ime_control_text = None

        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFixedSize(size, size)
        self.setStyleSheet(f"""
            background-color: #222222;
            border-radius: {self.border}px;
        """)
        self.child_size = self.size - (self.margins * 2)
        self.layout = QHBoxLayout()
        self.language_control_text = LanguageControlText(self.font_size, self.child_size)
        self.layout.addWidget(self.language_control_text)
        self.layout.setContentsMargins(self.margins, self.margins, self.margins, self.margins)
        self.setLayout(self.layout)

def get_widget(layout_config) -> QWidget:
    widget = LanguageControlLabel(
            layout_config[LayoutFields.WINBAR_COMPONENT_HEIGHT],
            layout_config[LayoutFields.GLOBAL_FONT_SIZE])
    return widget
