from datetime import datetime
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QPushButton, QWidget, QSizePolicy, QFrame
from PyQt5.QtCore import QTimer, Qt, QSize, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QColor
from utils import SvgWidget, QuickStartWidget

# --------- CUSTOM PYQT5 WIDGETS ------------
class QClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self):
        super().__init__()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mouseReleaseEvent(event)

    def enterEvent(self, event):
        self.setCursor(Qt.PointingHandCursor)

    def leaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)

# ------- CLOCK CONTAINER -----------
class ClockContainer(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(250, 40)
        self.setStyleSheet("""
            color: white;
            background: rgba(0,0,0,150);
            border-radius: 20px;
        """)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.addWidget(ClockLabelWidget())
        self.setLayout(self.layout)

class ClockLabelWidget(QLabel):
    def __init__(self):
        super().__init__(self.get_time_str())
        self.update()
        self.setAlignment(Qt.AlignCenter)
        self.setFont(QFont("Unageo", 12, QFont.Medium))

    def update(self):
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.setText(self.get_time_str()))
        self.timer.start(1000)

    def get_time_str(self):
        return datetime.now().strftime('%a, %d %b, %H:%M:%S')

# --------------- QUICKSTART MENU --------------
QuickStartWidgetList = []
QuickStartWidgetList.append(QuickStartWidget("Chrome", "assets/icon_chrome.svg", r"C:\Program Files\Google\Chrome\Application\chrome.exe"))
QuickStartWidgetList.append(QuickStartWidget("Command Prompt", "assets/icon_terminal.svg",r"C:\WINDOWS\system32\cmd.exe"))

class QuickStartContainer(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("QuickStartContainer")
        self.setFixedSize(len(QuickStartWidgetList) * 50, 40)
        self.setStyleSheet("""
            #QuickStartContainer {
                background: rgba(0,0,0,150);
                border-radius: 20px;
                color: white;
                padding-right: 3px;
                padding-left: 3px;
            }
        """)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        
        for application_widget in QuickStartWidgetList:
            self.layout.addWidget(QuickStartButtonWidget(application_widget))
        self.setLayout(self.layout)

class QuickStartButtonWidget(QClickableLabel):
    def __init__(self, application_widget):
        super().__init__()
        self.application_widget = application_widget
        self.setAlignment(Qt.AlignCenter)
        self.icon = SvgWidget(application_widget.icon_path, QSize(22,22))
        self.setPixmap(self.icon.render_svg(QColor("white")))
        self.clicked.connect(self.clickEvent)

    def clickEvent(self):
        self.application_widget.run()

    def enterEvent(self, event):
        super().enterEvent(event)
        self.setPixmap(self.icon.render_svg(QColor("#7accee")))

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.setPixmap(self.icon.render_svg(QColor("white")))

