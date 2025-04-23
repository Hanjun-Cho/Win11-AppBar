from PyQt5.QtWidgets import QApplication
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtGui import QPainter, QColor, QPixmap
from PyQt5.QtCore import QSize, Qt, QRectF

import subprocess 
import sys

class SvgWidget():
    def __init__(self, svg_path, size, color=Qt.black):
        self.svg_path = svg_path
        self.size = size
        self.color = QColor(color)
        self.original_pixmap = self.generate_initial_pixmap()

    def generate_initial_pixmap(self):
        renderer = QSvgRenderer(self.svg_path)
        pixmap = QPixmap(QSize(256,256))
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter, QRectF(0,0,256,256))
        painter.end()
        return pixmap

    def render_svg(self, color):
        mask = self.original_pixmap.createMaskFromColor(Qt.transparent, Qt.MaskInColor)
        recolored_pixmap = QPixmap(QSize(256,256))
        recolored_pixmap.fill(color)
        recolored_pixmap.setMask(mask)
        return recolored_pixmap.scaled(self.size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

class QuickStartWidget():
    def __init__(self, name, icon_path, application_path):
        self.name = name
        self.icon_path = icon_path
        self.application_path = application_path

    def run(self):
        print(f"Running: {self.name}")
        subprocess.Popen([self.application_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
