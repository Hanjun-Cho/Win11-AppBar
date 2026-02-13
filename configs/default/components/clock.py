from datetime import datetime
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PySide6.QtCore import QTimer, Qt
from configs.layout_config import LayoutFields

class ClockWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(250)
        self.layout = QHBoxLayout()
        self.layout.addWidget(ClockLabel())
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)

class ClockLabel(QLabel):
    def __init__(self):
        super().__init__(self.get_time_str())
        self.setAlignment(Qt.AlignCenter)
        self.update()

    def update(self):
        # every 1 second updates string in this QLabel
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.setText(self.get_time_str()))
        self.timer.start(1000)

    def get_time_str(self):
        return datetime.now().strftime('%a, %d %b, %H:%M:%S')

def get_widget(layout_config) -> QWidget:
    widget = ClockWidget()
    widget.setFixedHeight(layout_config[LayoutFields.WINBAR_COMPONENT_HEIGHT])
    widget.setStyleSheet(f"""
        border-radius: {layout_config[LayoutFields.WINBAR_COMPONENT_HEIGHT] // 2}px;
        background-color: #222222;
        font-size: {layout_config[LayoutFields.GLOBAL_FONT_SIZE]}px;
    """)
    return widget 
