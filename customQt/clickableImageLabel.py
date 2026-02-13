from PySide6.QtGui import QPixmap, QIcon 
from PySide6.QtCore import QSize, Qt
from customQt.clickableLabel import ClickableLabel

class ClickableImageLabel(ClickableLabel):
    def __init__(self, parent=None, image_path=None, is_svg=False, size=QSize):
        super().__init__(parent)
        if image_path is None:
            raise Exception("image path cannot be null")

        if is_svg:
            self.set_icon_pixmap(image_path, size)
        else:
            self.set_image_pixmap(image_path, size)

    def set_pixmap(self, pixmap=None):
        if pixmap is None:
            raise Exception("pixmap cannto be None")
        if pixmap.isNull():
            raise Exception("pixmap was null")
        self.pixmap = pixmap
        self.setPixmap(pixmap)
        self.setAlignment(Qt.AlignCenter)
        
    def set_icon_pixmap(self, image_path=None, size=QSize):
        icon = QIcon(image_path)
        pixmap = icon.pixmap(size)
        self.set_pixmap(pixmap)

    def set_image_pixmap(self, image_path=None, size=QSize):
        pixmap = QPixmap(image_path)
        pixmap.scaled(size)
        self.set_pixmap(pixmap)
