from PySide6.QtWidgets import QWidget, QFrame, QSizePolicy
from PySide6.QtCore import Qt, QTimer, QPoint, QPropertyAnimation, QEasingCurve
from pyvda import VirtualDesktop, get_virtual_desktops
from customQt.clickableLabel import ClickableLabel
from configs.layout_config import LayoutFields
from enum import IntEnum

class DSCConstant(IntEnum):
    ELEMENT_SIZE = 30
    ELEMENT_GAP = 3
    FRAME_MARGIN = 5

class DesktopStatusContainer(QWidget):
    def __init__(self, layout_config, colors):
        super().__init__()
        self.desktop_count = len(get_virtual_desktops())
        self.selected_desktop = VirtualDesktop.current().number - 1

        self.update_width(self.desktop_count)
        self.height = layout_config[LayoutFields.WINBAR_COMPONENT_HEIGHT]
        self.setFixedSize(self.width, self.height)
        self.background = DesktopStatusBackground(self, self.width, self.height, colors["background"])
        
        self.desktop_status_highlight = DesktopStatusLabelBackground(self, colors["highlighted"])
        self.desktop_status_elements = []

        for i in range(self.desktop_count):
            self.desktop_status_elements.append(self.generate_desktop_status_element(i))

        self.switch_desktop(self.selected_desktop)
        self.show()
        self.update()

    def update_width(self, desktop_count):
        total_element_width = desktop_count * DSCConstant.ELEMENT_SIZE
        total_frame_margins = 2 * DSCConstant.FRAME_MARGIN
        total_element_gap = ((desktop_count - 1) * DSCConstant.ELEMENT_GAP)
        self.width = total_frame_margins + total_element_width + total_element_gap

    def generate_desktop_status_element(self, index):
        return DesktopStatusLabel(self, index, self.switch_desktop)

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

class DesktopStatusLabelBackground(QFrame):
    def __init__(self, parent, color):
        super().__init__(parent)
        self.setFixedSize(DSCConstant.ELEMENT_SIZE, DSCConstant.ELEMENT_SIZE)
        self.move(DSCConstant.FRAME_MARGIN, DSCConstant.FRAME_MARGIN)
        self.setStyleSheet(f"""
            background-color: {color};
            border-radius: {DSCConstant.ELEMENT_SIZE // 2}px;
        """)

    def switch_desktop(self, position):
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.setEndValue(position)
        self.animation.setDuration(250)
        self.animation.start()

class DesktopStatusLabel(ClickableLabel):
    def __init__(self, parent, desktop_id, switch_desktop):
        super().__init__(parent, str(desktop_id + 1))
        self.switch_desktop = switch_desktop
        self.active = False
        self.desktop_id = desktop_id
        self.setFixedSize(DSCConstant.ELEMENT_SIZE, DSCConstant.ELEMENT_SIZE)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(f"""
            color: white;
            background-color: transparent;
            border-radius: {DSCConstant.ELEMENT_SIZE // 2}px;
        """)

        leftside_element_width = desktop_id * DSCConstant.ELEMENT_SIZE
        leftside_element_gap = desktop_id * DSCConstant.ELEMENT_GAP
        x_offset = DSCConstant.FRAME_MARGIN + leftside_element_width + leftside_element_gap
        y_offset = DSCConstant.FRAME_MARGIN
        self.move(x_offset, y_offset)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        self.position = QPoint(x_offset, y_offset)
        self.clicked.connect(self.on_click)
        self.show()

    def on_click(self):
        self.active = True
        self.switch_desktop(self.desktop_id)
        self.set_default_style()

    def set_default_style(self):
        color = 'black' if self.active else 'white'
        self.setStyleSheet(f"""
            background-color: transparent;
            border-radius: {DSCConstant.ELEMENT_SIZE // 2}px;
            color: {color};
        """)

    def set_hover_style(self):
        self.setStyleSheet(f"""
            background-color: rgba(255,255,255,25);
            border-radius: {DSCConstant.ELEMENT_SIZE // 2}px;
            color: white;
        """)

    def deselect(self):
        self.active = False 
        self.set_default_style()
    
    def is_active(self):
        return self.active

    def get_position(self):
        return self.position

    def enterEvent(self, event):
        if self.active: 
            return
        super().enterEvent(event)
        self.set_hover_style()

    def leaveEvent(self, event):
        if self.active:
            return
        super().leaveEvent(event)
        self.set_default_style()

def get_widget(layout_config):
    widget = DesktopStatusContainer(layout_config, colors={
        "background": "#222222",
        "highlighted": "#8cd49e"
    })
    return widget
