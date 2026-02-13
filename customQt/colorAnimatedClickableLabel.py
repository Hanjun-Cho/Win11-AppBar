from customQt.clickableLabel import ClickableLabel
from PySide6.QtCore import Property, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QColor

class ColorAnimatedClickableLabel(ClickableLabel):
    def __init__(self, parent=None, content="", start_color=""):
        self.start_color = start_color

        super().__init__(parent=parent, text=content)
        self._set_color(QColor(self.start_color))

    def _set_color(self, color):
        self._color = color
        self.setStyleSheet(f"""
            {self.get_default_style()}
            background-color: {self._color.name()};
        """)

    def _get_color(self):
        return self._color
    
    color = Property(QColor, _get_color, _set_color)
    
    def get_default_style(self):
        return ""
    
    def animate_color(self, color, easing_curve=QEasingCurve.Type.OutCubic, duration=250):
        self.animation = QPropertyAnimation(self, b"color")
        self.animation.setEasingCurve(easing_curve)
        self.animation.setStartValue(self._color)
        self.animation.setEndValue(color)
        self.animation.setDuration(duration)
        self.animation.start()
