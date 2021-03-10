from typing import Tuple, Dict, Union, Callable

from PyQt5.QtWidgets import QWidget, QPushButton, QCheckBox, QLabel, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QMoveEvent, QResizeEvent, QPixmap, QColor, QIcon, QKeyEvent, QPainter, QPen, QBrush
from PyQt5.QtCore import Qt, QSize, QLoggingCategory, QtMsgType, \
                         QtDebugMsg, QtInfoMsg, QtCriticalMsg, QtWarningMsg, QtFatalMsg

from api.common import OS

__all__ = ['Widget', 'Label', 'PushButton', 'CheckBox', 'Window',
           'Painter', 'Pen', 'Brush', 'GraphicsView', 'GraphicsScene',
           'Logger', 'MessageType']


class Widget(QWidget):

    def __init__(self, *args, **kwargs):

        super(Widget, self).__init__(*args, **kwargs)

    @property
    def x(self):

        return super().x()

    @property
    def y(self):

        return super().y()

    @property
    def width(self):

        return super().width()

    @property
    def height(self):

        return super().height()


class Label(QLabel):

    def __init__(self, *args, **kwargs):

        super(Label, self).__init__(*args, **kwargs)

    @property
    def x(self):

        return super().x()

    @property
    def y(self):

        return super().y()

    @property
    def width(self):

        return super().width()

    @property
    def height(self):

        return super().height()


class PushButton(QPushButton):

    def __init__(self, *args, **kwargs):

        super(PushButton, self).__init__(*args, **kwargs)

    @property
    def x(self):

        return super().x()

    @property
    def y(self):

        return super().y()

    @property
    def width(self):

        return super().width()

    @property
    def height(self):

        return super().height()


class CheckBox(QCheckBox):

    def __init__(self, *args, **kwargs):

        super(CheckBox, self).__init__(*args, **kwargs)

    @property
    def x(self):

        return super().x()

    @property
    def y(self):

        return super().y()

    @property
    def width(self):

        return super().width()

    @property
    def height(self):

        return super().height()


class Window(Widget):

    def __init__(self, title: str, screen_geometry:  Tuple[int, int, int, int],
                 style: str = None, parent: Union[Widget] = None,
                 callbacks: Dict[str, Callable] = None, *args, **kwargs):

        super(Window, self).__init__(*args, **kwargs)

        self.__key_code__ = Qt.Key()

        self.base_screen_geometry = screen_geometry
        self.screen_geometry = list(screen_geometry)

        self.callbacks = callbacks

        self.setWindowTitle(title)
        self.setGeometry(*screen_geometry)

        if style is not None:

            self.setStyleSheet(style)

        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)

        if parent is not None:

            self.setParent(parent)

    def resize(self, *args):

        super().resize(args[0], args[1])

        self.screen_geometry[2] = args[0]
        self.screen_geometry[3] = args[1]

    def resizeEvent(self, a0: QResizeEvent):

        super().resizeEvent(a0)

        self.screen_geometry[2] = a0.size().width()
        self.screen_geometry[3] = a0.size().height()

    def moveEvent(self, a0: QMoveEvent):

        self.screen_geometry[0] = a0.oldPos().x()
        self.screen_geometry[1] = a0.oldPos().y()

    def setGeometry(self, *args):

        super().setGeometry(*args)

        self.screen_geometry = list(args)

    def set_full_screen(self, flag: bool):

        if flag:

            self.setWindowState(Qt.WindowFullScreen)

        else:

            self.set_no_state()

    def set_no_state(self):

        self.setWindowState(Qt.WindowNoState)
        self.updateGeometry()

    def center_x(self, width=0, tr=0):

        return self.width // 2 - width // 2 + tr

    def center_y(self, height=0, tr=0):

        return self.height // 2 - height // 2 + tr

    def relative_center(self, parent, tr_x=0, tr_y=0, width=0, height=0):

        rel_width = (parent.width / self.width) * parent.width
        rel_height = (parent.height / self.height) * parent.height

        rel_x = rel_width // 2 - width // 2 + tr_x
        rel_y = rel_height // 2 - height // 2 + tr_y

        return rel_x, rel_y

    def left_x(self, width=0):

        return -self.center_x() + width

    def left_y(self, height=0):

        return -self.center_y() + height

    def right_x(self, width=0):

        return self.center_x() + width

    def right_y(self, height=0):

        return self.center_y() + height

    def keyPressEvent(self, key_event: QKeyEvent):

        self.pressed(key_event.key())

        if self.pressed_key == Qt.Key_Escape:

            self.close()

    def keyReleaseEvent(self, key_event: QKeyEvent):

        self.released(key_event.key())

    def pressed(self, key):

        self.__key_code__ += key

    def released(self, key):

        self.__key_code__ -= key

    @property
    def pressed_key(self):

        return self.__key_code__

    @staticmethod
    def get_keys_code(*args):

        return sum(args)

    def add_push_button(self, attr_name: str, width: int, height: int, x: int = 0, y: int = 0,
                        text: str = None, active=True, clicked_callback: Callable = None,
                        icon: str = None, style: str = None, icon_size: tuple = None,
                        ignore_geometry: bool = False, parent=None):

        button = PushButton()

        if icon is not None:

            if OS.file_exists(icon):

                button.setIcon(QIcon(icon))

                if icon_size is not None:

                    button.setIconSize(QSize(*icon_size))

                if text is not None:

                    text = ' ' * 7 + text

            else:

                raise ValueError('File ' + icon + ' doesn\'t exist')

        if text is not None:

            button.setText(text)

        if style is not None:

            button.setStyleSheet(style)

        if clicked_callback is not None:

            button.clicked.connect(clicked_callback)

        button.setEnabled(active)

        if parent is not None:

            button.setParent(parent)

        if not ignore_geometry:

            if parent is not None:

                button_geo = *self.relative_center(parent, tr_x=x, tr_y=y, width=width, height=height), width, height

            else:

                button_geo = self.center_x(width, x), self.center_y(height, y), width, height

            button.setGeometry(*button_geo)

        if not hasattr(self, attr_name):

            setattr(self, attr_name, button)

        else:

            raise ValueError('Button Attribute: attr_name = ' + attr_name + ' | is Already Exists')

    def add_checkbox_button(self, attr_name: str, width: int, height: int,
                            x: int = 0, y: int = 0, text: str = None, active=True,
                            toggled_callback: Callable = None, icon: str = None,
                            style: str = None, icon_size: tuple = None,
                            ignore_geometry: bool = False, parent=None):

        button = CheckBox()

        if icon is not None:

            if OS.file_exists(icon):

                button.setIcon(QIcon(icon))

                if icon_size is not None:

                    button.setIconSize(QSize(*icon_size))

                if text is not None:

                    text = ' ' * 7 + text

            else:

                raise ValueError('File ' + icon + ' doesn\'t exist')

        if text is not None:

            button.setText(text)

        if style is not None:

            button.setStyleSheet(style)

        if toggled_callback is not None:

            button.toggled.connect(toggled_callback)

        button.setEnabled(active)

        if parent is not None:

            button.setParent(parent)

        if not ignore_geometry:

            if parent is not None:

                button_geo = *self.relative_center(parent, tr_x=x, tr_y=y, width=width, height=height), width, height

            else:

                button_geo = self.center_x(width, x), self.center_y(height, y), width, height

            button.setGeometry(*button_geo)

        if not hasattr(self, attr_name):

            setattr(self, attr_name, button)

        else:

            raise ValueError('Button Attribute: attr_name = ' + attr_name + ' | is Already Exists')

    def add_label(self, attr_name: str, width: int, height: int, x: int = 0, y: int = 0,
                  set_pixmap: bool = False, parent: Widget = None, ignore_geometry: bool = False):

        label = Label()

        if parent is not None:

            label.setParent(parent)

        if not ignore_geometry:

            if parent is not None:

                label_geo = *self.relative_center(parent, tr_x=x, tr_y=y, width=width, height=height), width, height

            else:

                label_geo = self.center_x(width, x), self.center_y(height, y), width, height

            label.setGeometry(*label_geo)

        if set_pixmap:

            pixmap = QPixmap(width, height)

            mask = pixmap.createMaskFromColor(QColor(0, 0, 0), Qt.MaskInColor)

            pixmap.setMask(mask)

            label.setPixmap(pixmap)

        if not hasattr(self, attr_name):

            setattr(self, attr_name, label)

        else:

            raise ValueError('Label Attribute: attr_name = ' + attr_name + ' | is Already Exists')

    def widget(self, attr_name) -> QWidget:

        if hasattr(self, attr_name):

            return getattr(self, attr_name)

        else:

            raise ValueError('QWidget: attr_name = ' + attr_name + ' | doesn\'t Exist')

    def button(self, attr_name) -> Union[PushButton, CheckBox]:

        try:

            return self.widget(attr_name)

        except ValueError:

            raise ValueError('Button Attribute: attr_name = ' + attr_name + ' | doesn\'t Exist')

    def label(self, attr_name) -> Label:

        try:

            return self.widget(attr_name)

        except ValueError:

            raise ValueError('Button Attribute: attr_name = ' + attr_name + ' | doesn\'t Exist')

    def set_style(self, attr_name, *args):

        style = ''.join(args)

        self.widget(attr_name).setStyleSheet(self.widget(attr_name).styleSheet() + style)


class Pen(QPen):

    def __init__(self, *args, **kwargs):

        super(Pen, self).__init__(*args, **kwargs)


class Brush(QBrush):

    def __init__(self, *args, **kwargs):

        super(Brush, self).__init__(*args, **kwargs)


class Painter(QPainter):

    def __init__(self, *args, **kwargs):

        super(Painter, self).__init__(*args, **kwargs)

    def set_pen(self, width: int, color: str):

        pen = Pen()
        pen.setWidth(width)
        pen.setColor(QColor(color))

        self.setPen(pen)

        return self

    def set_brush(self, color: str, style: Qt):

        brush = Brush()
        brush.setColor(QColor(color))
        brush.setStyle(style)

        self.setBrush(brush)

        return self


class GraphicsView(QGraphicsView):

    def __init__(self, *args, **kwargs):

        super(GraphicsView, self).__init__(*args, **kwargs)


class GraphicsScene(QGraphicsScene):

    def __init__(self, *args, **kwargs):

        super(GraphicsScene, self).__init__(*args, **kwargs)


class Logger(QLoggingCategory):

    def __init__(self, *args, **kwargs):

        super(Logger, self).__init__(*args, **kwargs)

    def set_all_msg_enabled(self, enabled: bool):

        for i in range(5):

            msg_type = QtMsgType(i)
            self.setEnabled(msg_type, enabled)

    def set_all_msg_enabled_except(self, enabled, *args):

        for i in range(5):

            msg_type = QtMsgType(i)

            if i in args:

                self.setEnabled(msg_type, not enabled)

            else:

                self.setEnabled(msg_type, enabled)


class MessageType:

    DebugMsg = QtDebugMsg
    InfoMsg = QtInfoMsg
    CriticalMsg = QtCriticalMsg
    WarningMsg = QtWarningMsg
    FatalMsg = QtFatalMsg
