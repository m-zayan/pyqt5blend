import sys

from typing import Tuple, Dict, Union

from PyQt5.QtWidgets import QApplication

from ...api.gui.widgets import Window, Logger
from ...api.gui.pages import Page

__all__ = ['Application']


class Application:

    resolution_geometry: Tuple[int, int, int, int] = None

    def __init__(self, name: str, main_window: str, screen_geometry: Tuple[int, int, int, int] = None,
                 config: Dict[str, Union[bool, int, str]] = None):

        """
        flags: {'exit_status': bool}
        """

        self.app = QApplication(sys.argv)

        self.name = name

        self.__current_window__ = None
        self.__prev_window__ = None

        self.flags:  Dict[str, Union[bool, int]] = dict()

        self.config: Dict[str, Union[bool, int, str]] = {'full_screen': False, 'fixed_size': False,
                                                         'min_width': self.device_resolution_geometry[2] // 2,
                                                         'min_height': self.device_resolution_geometry[3] // 2}

        if config is not None:

            self.config.update(config)

        if screen_geometry is None or self.config['full_screen']:

            Application.resolution_geometry = self.device_resolution_geometry

        else:

            center = self.center(screen_geometry)
            Application.resolution_geometry = (*center, screen_geometry[2], screen_geometry[3])

        self.windows: Dict[str, Union[Window, Page]] = dict()

        self.init_windows()

        self.disable_resize(self.config['fixed_size'])
        self.set_min_window_size(self.config['min_width'], self.config['min_height'])
        self.app_full_screen()

        self.set_current_window(main_window)

    def init_windows(self):

        raise NotImplementedError('def init_windows(self):')

    def window(self, name) -> Window:

        if name in self.windows:

            return self.windows[name]

        else:

            raise ValueError('Invalid Window :' + name)

    def show(self):

        self.current_window.setGeometry(*self.prev_window.screen_geometry)
        self.current_window.show()

    def run(self):

        self.show()
        self.exit()

    def close_current_window(self):

        self.current_window.close()

    @property
    def current_window(self) -> Window:

        return self.window(self.__current_window__)

    @property
    def prev_window(self) -> Window:

        if self.__prev_window__ is None:

            return self.current_window

        return self.window(self.__prev_window__)

    def set_current_window(self, name):

        self.__prev_window__ = self.__current_window__
        self.__current_window__ = name

    def exit(self):

        self.flags['exit_status'] = self.app.exec()

        if self.flags['exit_status'] == 0:

            self.current_window.close()

        sys.exit(self.flags['exit_status'])

    @property
    def device_resolution_geometry(self):

        return self.app.desktop().screenGeometry().getRect()

    def set_min_window_size(self, width, height):

        for key in self.windows:

            if not self.config['fixed_size'] or self.is_page(key):

                self.window(key).setMinimumSize(width, height)

    def disable_resize(self, state):

        if state:

            for key in self.windows:

                if self.is_page(key):

                    continue

                self.window(key).setFixedSize(self.window(key).width, self.window(key).height)

    def is_page(self, key):

        return isinstance(self.window(key), Page)

    def app_full_screen(self):

        for key in self.windows:

            self.window(key).set_full_screen(self.config['full_screen'])

    def center(self, screen_geometry):

        center = list(self.device_resolution_geometry[2:])

        center[0] = center[0] // 2 + screen_geometry[0] - screen_geometry[2] // 2
        center[1] = center[1] // 2 + screen_geometry[1] - screen_geometry[3] // 2

        return center

    def add_logger(self):

        logger = Logger(self.name + '_' + 'logger')

        setattr(self, 'msg_logger', logger)

    @property
    def logger(self) -> Logger:

        if hasattr(self, 'msg_logger'):

            return getattr(self, 'msg_logger')

        else:

            raise ValueError('Application has no logger, consider using, sef.add_logger(self), method')
