from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, Signal 

class ClickableLabel(QLabel):
    clicked = Signal()

    def __init__(self, parent=None, text=""):
        if parent is not None:
            super().__init__(text=text, parent=parent)
        else:
            super().__init__(text)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mouseReleaseEvent(event)

    def enterEvent(self, event):
        self.setCursor(Qt.PointingHandCursor)
        event.accept()

    def leaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        event.accept()
