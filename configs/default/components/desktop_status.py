from PySide6.QtWidgets import QWidget, QFrame, QSizePolicy
from PySide6.QtCore import Qt, QTimer, QPoint, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QColor, QPainter, QBrush
from pyvda import VirtualDesktop, get_virtual_desktops
from customQt.colorAnimatedClickableLabel import ColorAnimatedClickableLabel
from customQt.positionAnimatedClickableLabel import PositionAnimatedClickableLabel 
from configs.layout_config import LayoutFields
from enum import IntEnum

class DSCConstant(IntEnum):
    ELEMENT_GAP = 3
    FRAME_MARGIN = 3

class DesktopStatusContainer(QWidget):
    def __init__(self, layout_config, colors):
        super().__init__()
        self.element_size = layout_config[LayoutFields.WINBAR_COMPONENT_HEIGHT] - (2 * DSCConstant.FRAME_MARGIN)
        self.desktop_count = len(get_virtual_desktops())
        self.selected_desktop = VirtualDesktop.current().number - 1

        self.update_width(self.desktop_count)
        self.height = layout_config[LayoutFields.WINBAR_COMPONENT_HEIGHT]
        self.setFixedSize(self.width, self.height)
        self.background = DesktopStatusBackground(self, self.width, self.height, colors["background"])
        
        self.desktop_status_highlight = DesktopStatusLabelBackground(self, colors["highlighted"], self.element_size)
        self.desktop_status_elements = []

        for i in range(self.desktop_count):
            self.desktop_status_elements.append(self.generate_desktop_status_element(i))

        self.switch_desktop(self.selected_desktop)
        self.show()
        self.update()

    def update_width(self, desktop_count):
        total_element_width = desktop_count * self.element_size
        total_frame_margins = 2 * DSCConstant.FRAME_MARGIN
        total_element_gap = ((desktop_count - 1) * DSCConstant.ELEMENT_GAP)
        self.width = total_frame_margins + total_element_width + total_element_gap

    def generate_desktop_status_element(self, index):
        return DesktopStatusLabel(self, index, self.switch_desktop, self.element_size)

    def update(self):
        super().update()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_desktop_status)
        self.timer.start(50)

    def update_desktop_status(self):
        self.update_desktop_count() 
        self.validate_current_desktop()
        self.updateGeometry()

    def update_desktop_count(self):
        updated_desktop_count = len(get_virtual_desktops())
        if self.desktop_count < updated_desktop_count:
            for i in range(updated_desktop_count - self.desktop_count):
                print(self.desktop_count, updated_desktop_count, i)
                self.desktop_status_elements.append(self.generate_desktop_status_element(self.desktop_count + i))
        elif self.desktop_count > updated_desktop_count:
            self.desktop_status_elements = self.desktop_status_elements[0:updated_desktop_count]
        if updated_desktop_count != self.desktop_count:
            self.update_width(updated_desktop_count)
            self.setFixedSize(self.width, self.height)
            self.background.update_dimensions(self.width, self.height)
            print(self.desktop_status_elements[len(self.desktop_status_elements)-1].get_position())
        self.desktop_count = updated_desktop_count

    def validate_current_desktop(self):
        current_desktop = VirtualDesktop.current().number - 1
        if current_desktop != self.selected_desktop:
            self.selected_desktop = current_desktop
            self.switch_desktop(self.selected_desktop)

    def switch_desktop(self, desktop_id):
        self.selected_desktop = desktop_id
        self.desktop_status_highlight.switch_desktop(self.desktop_status_elements[self.selected_desktop].get_position())
        self.deselect_other_desktops()
        VirtualDesktop(number = self.selected_desktop+1).go()
    
    def deselect_other_desktops(self):
        for i in range(self.desktop_count):
            if i == self.selected_desktop and not self.desktop_status_elements[i].is_active():
                self.desktop_status_elements[i].on_click()
            elif i == self.selected_desktop:
                continue
            else:
                self.desktop_status_elements[i].deselect()

class DesktopStatusBackground(QFrame):
    def __init__(self, parent, width, height, color):
        super().__init__(parent)
        self.setFixedSize(width, height)
        self.setStyleSheet(f"""
            background-color: {color};
            border-radius: {height // 2}px;
        """)
    
    def update_dimensions(self, width, height):
        self.setFixedSize(width, height)
        self.updateGeometry()

class DesktopStatusLabelBackground(PositionAnimatedClickableLabel):
    def __init__(self, parent, color, size):
        position = QPoint(DSCConstant.FRAME_MARGIN, DSCConstant.FRAME_MARGIN)
        super().__init__(parent=parent, start_position=position)
        self.move(position)
        self.setFixedSize(size, size)
        self.setStyleSheet(f"""
            background-color: {color};
            border-radius: {size // 2}px;
        """)

    def switch_desktop(self, position):
        self.animate_position(position)

class DesktopStatusLabel(ColorAnimatedClickableLabel):
    def __init__(self, parent, desktop_id, switch_desktop, size):
        self.size = size
        self.switch_desktop = switch_desktop
        self.active = False
        self.desktop_id = desktop_id

        super().__init__(parent, str(desktop_id + 1), start_color="transparent")
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setFixedSize(self.size, self.size)
        self.setAlignment(Qt.AlignCenter)

        leftside_element_width = desktop_id * self.size
        leftside_element_gap = desktop_id * DSCConstant.ELEMENT_GAP
        x_offset = DSCConstant.FRAME_MARGIN + leftside_element_width + leftside_element_gap
        y_offset = DSCConstant.FRAME_MARGIN
        self.move(x_offset, y_offset)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        self.position = QPoint(x_offset, y_offset)
        self.clicked.connect(self.on_click)
        self.show()

    def get_default_style(self):
        return f"""
            border-radius: {self.size // 2}px;
            color: {'black' if self.active else 'white'};
        """

    def deselect(self):
        self.active = False 
        self.animate_color(QColor("transparent"))
    
    def is_active(self):
        return self.active

    def get_position(self):
        return self.position

    # ----- Paint event -----
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(self._color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(self.rect())  # circle
        super().paintEvent(event)

    # ------- mouse events --------
    def on_click(self):
        self.active = True
        self.switch_desktop(self.desktop_id)
        self.animate_color(QColor("transparent"))

    def enterEvent(self, event):
        if self.active: 
            return
        super().enterEvent(event)
        self.animate_color(QColor(255,255,255,25))

    def leaveEvent(self, event):
        if self.active:
            return
        super().leaveEvent(event)
        self.animate_color(QColor("transparent"))

def get_widget(layout_config) -> QWidget:
    widget = DesktopStatusContainer(layout_config, colors={
        "background": "#222222",
        "highlighted": "#8cd49e"
    })
    widget.setStyleSheet(f"""
        font-size: {layout_config[LayoutFields.GLOBAL_FONT_SIZE]}px;
    """)
    return widget
