from pyqt5blend.utils.constants import Style
from pyqt5blend.utils.samples.widgets import Application

from tests.samples.cacao_app.window import MainWindow, ToolsWindow

__all__ = ['CacaoApp']


class CacaoApp(Application):

    def __init__(self, *args, **kwargs):

        super(CacaoApp, self).__init__(main_window='mainWindow', *args, **kwargs)

    def init_windows(self):

        # 1. Main Window
        main_window_callbacks = {'add_workspace': self.show_workspace_window,
                                 'show_settings': None,
                                 'show_history': None}

        self.windows['mainWindow'] = MainWindow(title=self.name, screen_geometry=CacaoApp.resolution_geometry,
                                                style=Style.background('gradient'), callbacks=main_window_callbacks)

        # 2. Tools Window
        tools_window_callbacks = {'show_tensor_plot_page': None,
                                  'show_geo_dashboard_page': None,
                                  'show_hessian_matrix_page': None,
                                  'show_latex_generator_page': None,
                                  'back': self.show_main_window}

        self.windows['toolsWindow'] = ToolsWindow(title=self.name, screen_geometry=CacaoApp.resolution_geometry,
                                                  style=Style.background('gradient'),
                                                  callbacks=tools_window_callbacks)

    def show_main_window(self):

        self.close_current_window()

        self.set_current_window('mainWindow')
        self.show()

    def show_workspace_window(self):

        self.close_current_window()

        self.set_current_window('toolsWindow')
        self.show()
