from api.gui.widgets import Window

__all__ = ['MainWindow']


class MainWindow(Window):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.button_1 = 'videoStreamButton'
        self.button_2 = 'Paint2DButton'

        self.add_push_button(attr_name=self.button_1, text='Video Stream',
                             width=200, height=50, x=0, y=-80, active=True,
                             clicked_callback=self.callbacks['show_video_stream_page'],
                             icon=None, icon_size=None,
                             style=None,
                             parent=self)

        self.add_push_button(attr_name=self.button_2, text='Paint 2D',
                             width=200, height=50, x=0, y=0, active=True,
                             clicked_callback=self.callbacks['show_paint2d_page'],
                             icon=None, icon_size=None,
                             style=None,
                             parent=self)
