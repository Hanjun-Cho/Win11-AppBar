import os
from PySide6.QtCore import QSize , QPropertyAnimation, QEasingCurve, Property
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QWidget
from customQt.clickableImageLabel import ClickableImageLabel 
from configs.layout_config import LayoutFields

class SoundControlLabel(ClickableImageLabel):
    def __init__(self, size):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        src_dir = current_dir + "./../src/sound/"
        self.icon_dir = src_dir + "sound.svg"
        self.size = QSize(18,18) 
        self.border = size // 2
        super().__init__(None, self.icon_dir, is_svg=True, size=self.size)
        self._set_color(QColor("#222222"))
        self.setFixedSize(size, size)

        self.clicked.connect(self.on_click)

    def _set_color(self, color):
        self._color = color
        self.setStyleSheet(f"""
            background-color: {self._color.name()};
            border-radius: {self.border}px;
            border: 3px solid #222222;
        """)
    
    @Property(QColor)
    def color(self):
        return self._color

    color = Property(QColor, color, _set_color)

    def on_click(self):
        print("clicked")
    
    def animate_color(self, color):
        self.animation = QPropertyAnimation(self, b"color")
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.setStartValue(self._color)
        self.animation.setEndValue(color)
        self.animation.setDuration(250)
        self.animation.start()

    def dark_icon_path(self):
        if "_dark" in self.icon_dir:
            return
        split = self.icon_dir.split(".svg")
        new_dir = split[0] + "_dark.svg"
        self.icon_dir = new_dir
        return new_dir

    def light_icon_path(self):
        if "_dark" not in self.icon_dir:
            return
        new_dir = self.icon_dir.replace("_dark", "")
        self.icon_dir = new_dir
        return new_dir

    def enterEvent(self, event):
        super().enterEvent(event)
        self.animate_color(QColor("#8cd49e"))
        self.set_icon_pixmap(image_path=self.dark_icon_path(), size=self.size)

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.animate_color(QColor("#222222"))
        self.set_icon_pixmap(image_path=self.light_icon_path(), size=self.size)

def get_widget(layout_config) -> QWidget:
    widget = SoundControlLabel(layout_config[LayoutFields.WINBAR_COMPONENT_HEIGHT])
    return widget
