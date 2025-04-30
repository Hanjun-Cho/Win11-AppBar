from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, pyqtSignal

class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None, text=""):
        if parent is not None:
            super().__init__(text, parent)
        else:
            super().__init__(text)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mouseReleaseEvent(event)

    def enterEvent(self, event):
        self.setCursor(Qt.PointingHandCursor)

    def leaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
