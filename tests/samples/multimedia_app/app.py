from utils.samples.widgets import Application
from utils.samples.pages import VideoStreamPage, Paint2DPage

from .window import MainWindow

__all__ = ['MultimediaApp']


class MultimediaApp(Application):

    def __init__(self, *args, **kwargs):

        super(MultimediaApp, self).__init__(main_window='mainWindow', *args, **kwargs)

    def init_windows(self):

        # 1. Main Window
        main_window_callbacks = {'show_video_stream_page': self.show_video_stream_page,
                                 'show_paint2d_page': self.show_paint2d_page}

        self.windows['mainWindow'] = MainWindow(title=self.name, screen_geometry=MultimediaApp.resolution_geometry,
                                                style=None, callbacks=main_window_callbacks)

        video_stream_page_callbacks = {'back': self.show_main_window}

        self.windows['videoStreamPage'] = VideoStreamPage(frame_width=700, frame_height=480,
                                                          cache_dir='./', title=self.name,
                                                          screen_geometry=MultimediaApp.resolution_geometry,
                                                          style=None, callbacks=video_stream_page_callbacks)

        paint2d_page_callbacks = {'back': self.show_main_window}

        self.windows['paint2DPage'] = Paint2DPage(title=self.name, screen_geometry=MultimediaApp.resolution_geometry,
                                                  style=None, callbacks=paint2d_page_callbacks)

        self.paint2d_page.scene.addText('Press: Ctr + F')

    def show_main_window(self):

        self.close_current_window()

        self.set_current_window('mainWindow')
        self.show()

    def show_video_stream_page(self):

        self.close_current_window()

        self.set_current_window('videoStreamPage')
        self.show()

    def show_paint2d_page(self):

        self.close_current_window()

        self.set_current_window('paint2DPage')
        self.show()

    @property
    def paint2d_page(self) -> Paint2DPage:

        return self.windows['paint2DPage']
