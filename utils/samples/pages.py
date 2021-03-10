from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtGui import QPixmap, QKeyEvent

from utils.constants import Style

from api.gui.widgets import *
from api.gui.pages import Page

from api.streams import VideoStream


__all__ = ['VideoStreamPage', 'Paint2DPage', 'Paint3DPage']


class VideoStreamPage(Page):

    def __init__(self, frame_width, frame_height, fix_color=True, flip=True, cache_dir=None, *args, **kwargs):

        self.frame_width = frame_width
        self.frame_height = frame_height

        self.fix_color = fix_color
        self.flip = flip

        self.cache_dir = cache_dir

        super(VideoStreamPage, self).__init__(*args, **kwargs)

    def set_full_screen(self, flag: bool):
        pass

    def keyPressEvent(self, key_event: QKeyEvent):

        super().keyPressEvent(key_event)

        if self.pressed_key == self.get_keys_code(Qt.Key_Control, Qt.Key_S):

            self.video_stream.save_current_frame(to_path=None)

    def update_frame(self, image):

        self.label('viewport').setPixmap(QPixmap.fromImage(image))

    def show(self):

        self.video_stream.start()

        super().show()

    def close(self):

        self.video_stream.stop()

        super().close()

    @property
    def video_stream(self) -> VideoStream:

        return getattr(self, 'videoStream')

    def layout(self) -> QGridLayout:

        return super().layout()

    def init_video_stream(self):

        video_stream = VideoStream(parent=self.layer(0), callback=self.update_frame,
                                   shape=(self.frame_height, self.frame_width), fix_color=self.fix_color,
                                   flip=self.flip, cache_dir=self.cache_dir)

        setattr(self, 'videoStream', video_stream)

    def init_layout(self):

        layout = QGridLayout()

        layout.setSpacing(6)

        # viewport, 10x: height
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 1)

        # viewport, 15x: width
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)

        self.setLayout(layout)

    def init_page(self):

        viewport = [Style.border(3, Style.SOLID, 'gray')]

        self.add_layer(layer_name='viewport', x=0, y=0, width=self.frame_width, height=self.frame_height,
                       layer_style=viewport, ignore_geometry=False)

        self.layout().addWidget(self.layer(-1), 0, 0, 1, 1)

        tpl_cell = [Style.border(3, Style.SOLID, 'gray')]
        self.add_layer(layer_name='tpl_cell', x=0, y=0, width=self.frame_width, height=self.frame_height,
                       layer_style=tpl_cell, ignore_geometry=False)

        self.layout().addWidget(self.layer(-1), 0, 1, 1, 1)

        tbr_cell = [Style.border(3, Style.SOLID, 'gray')]
        self.add_layer(layer_name='tbr_cell', x=0, y=0, width=self.frame_width, height=self.frame_height,
                       layer_style=tbr_cell, ignore_geometry=False)

        self.layout().addWidget(self.layer(-1), 1, 0, 1, 1)

        tbl_cell = [Style.border(3, Style.SOLID, 'gray')]
        self.add_layer(layer_name='tbl_cell', x=0, y=0, width=self.frame_width, height=self.frame_height,
                       layer_style=tbl_cell, ignore_geometry=False)

        self.layout().addWidget(self.layer(-1), 1, 1, 1, 1)

        self.init_video_stream()


class Paint2DPage(Page):

    def __init__(self, *args, **kwargs):

        super(Paint2DPage, self).__init__(*args, **kwargs)

    def painter(self, index: int) -> Painter:

        painter = Painter(self.layer(index).pixmap())

        return painter

    @property
    def scene(self) -> GraphicsScene:

        return self.widget('scene2d')

    @property
    def view(self) -> GraphicsView:

        return self.widget('view2d')

    def layout(self) -> QGridLayout:

        return super().layout()

    def init_graphics_view(self):

        scene = GraphicsScene(parent=self)
        view = GraphicsView(scene)

        setattr(self, 'scene2d', scene)
        setattr(self, 'view2d', view)

    def init_layout(self):

        layout = QGridLayout()

        layout.setSpacing(2)

        # view, 3x: height
        layout.setRowStretch(0, 2)
        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 3)
        layout.setRowStretch(3, 1)
        layout.setRowStretch(4, 1)

        # view, 2x: width
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 2)
        layout.setColumnStretch(2, 1)

        self.setLayout(layout)

    def init_page(self):

        self.init_graphics_view()
        self.layout().addWidget(self.view, 2, 1, 1, 1)

        # toolbar [1]
        toolbar = [Style.border(3, Style.SOLID, 'gray')]
        self.add_layer(layer_name='toolbar', layer_style=toolbar, ignore_geometry=True)
        self.layout().addWidget(self.layer(-1), 1, 1, 1, 1)

        # toolbox [2]
        toolbox = [Style.border(3, Style.SOLID, 'gray')]
        self.add_layer(layer_name='toolbox', layer_style=toolbox, ignore_geometry=True)
        self.layout().addWidget(self.layer(-1), 1, 0, 1, 1)

        # empty cell (top left) [3]
        tpl_cell = [Style.border(3, Style.SOLID, 'gray')]
        self.add_layer(layer_name='tplCell', layer_style=tpl_cell, ignore_geometry=True)
        self.layout().addWidget(self.layer(-1), 2, 0, 1, 1)

        # empty cell (top right) [4]
        tpr_cell = [Style.border(3, Style.SOLID, 'gray')]
        self.add_layer(layer_name='tprCell', layer_style=tpr_cell, ignore_geometry=True)
        self.layout().addWidget(self.layer(-1), 1, 2, 1, 1)

        # toolOptions [5]
        tool_options = [Style.border(3, Style.SOLID, 'gray')]
        self.add_layer(layer_name='toolOptions', layer_style=tool_options, ignore_geometry=True)
        self.layout().addWidget(self.layer(-1), 1, 2, 2, 1)

        # statusBar [6]
        status_bar = [Style.border(3, Style.SOLID, 'gray')]
        self.add_layer(layer_name='statusBar', layer_style=status_bar, ignore_geometry=True)
        self.layout().addWidget(self.layer(-1), 3, 0, 1, 3)


class Paint3DPage(Page):

    def __init__(self, *args, **kwargs):

        super(Paint3DPage, self).__init__(*args, **kwargs)

    def init_layout(self):

        super().init_layout()

    def init_page(self):

        super().init_workspace()
