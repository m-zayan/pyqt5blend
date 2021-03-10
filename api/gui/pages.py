from typing import Union

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent

from api.gui.widgets import *

__all__ = ['Page']


class Page(Window):

    def __init__(self, *args, **kwargs):

        super(Page, self).__init__(*args, **kwargs)

        self.layers = []
        self.buttons = []

        self.init_layout()

        if self.layout() is None:

            raise AssertionError('Page, layout is not found, consider set layout at the end of, '
                                 'init_layout(self): -> None, method\n\n'
                                 '\tex. self.setLayout(layout)')
        self.init_page()

    def init_page(self):

        raise NotImplementedError('def init_page(self): \n\n'
                                  '\t# add widgets, to page\'s layout ...\n')

    def init_layout(self):

        raise NotImplementedError('def init_layout(self): \n\n'
                                  '\t# construct a layout ...\n\n'
                                  '\tself.setLayout(layout)')

    def keyPressEvent(self, key_event: QKeyEvent):

        super().keyPressEvent(key_event)

        if self.pressed_key == self.get_keys_code(Qt.Key_Control, Qt.Key_F):

            self.set_full_screen(not self.isFullScreen())

    def add_layer(self, layer_name: str, x: int = None, y: int = None,
                  width: int = None, height: int = None, set_pixmap=True,
                  layer_style: list = None, ignore_geometry=True):

        try:

            self.add_label(attr_name=layer_name, width=width, height=height, x=x, y=y,
                           set_pixmap=set_pixmap, ignore_geometry=ignore_geometry, parent=self)

        except ValueError:

            ValueError('Layer: layer_name = ' + layer_name + ' | is Already Exists')

        if layer_style is not None:

            self.set_style(layer_name, *layer_style)

        self.layers.append(layer_name)

    def add_push_button(self, *args, **kwargs):

        super().add_push_button(*args, **kwargs)

        self.buttons.append(kwargs['attr_name'])

    def add_checkbox_button(self, *args, **kwargs):

        super().add_checkbox_button(*args, **kwargs)

        self.buttons.append(kwargs['attr_name'])

    def layer(self, index) -> Label:

        if len(self.layers) <= index or len(self.layers) - abs(index) < 0:

            raise IndexError('Layer index out of range')

        return self.label(self.layers[index])

    def button(self, index: int) -> Union[PushButton, CheckBox]:

        if len(self.buttons) <= index or len(self.buttons) - abs(index) < 0:

            raise IndexError('button gui, index out of range')

        return super().button(self.buttons[index])
