from customQt.clickableLabel import ClickableLabel
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QPoint

class PositionAnimatedClickableLabel(ClickableLabel):
    def __init__(self, parent=None, content="", start_position=QPoint(0,0)):
        self.position = start_position 

        super().__init__(parent=parent, text=content)
    
    def animate_position(self, position, easing_curve=QEasingCurve.Type.OutCubic, duration=250):
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setEasingCurve(easing_curve)
        self.animation.setStartValue(self.position)
        self.animation.setEndValue(position)
        self.animation.setDuration(duration)
        self.animation.start()
        self.position = position
