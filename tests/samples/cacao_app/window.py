from utils.constants import Style, Icon

from api.gui import widgets
from api.gui.pages import Page

__all__ = ['MainWindow', 'ToolsWindow', 'TensorPlotPage',
           'GeoDashboardPage', 'HessianMatrixPage', 'LatexGeneratorPage']


class Window(widgets.Window):

    def __init__(self, *args, **kwargs):

        super(Window, self).__init__(*args, **kwargs)

    def add_back_button(self, callback):

        self.add_push_button(attr_name='back_button', text=None,
                             width=50, height=50, x=self.left_x(50), y=self.left_y(50), active=True,
                             icon=Icon.png('previous'), icon_size=(30, 30),
                             style=Style.widgets('PushButtonIcon', 'active'),
                             clicked_callback=callback,
                             ignore_geometry=False, parent=self)

    def activate_push_button(self, attr_name):

        button = self.button(attr_name)
        button.setStyleSheet(Style.widgets('PushButtonIcon', 'active'))
        button.setEnabled(True)

    def deactivate_push_button(self, attr_name):

        button = self.button(attr_name)
        button.setStyleSheet(Style.widgets('PushButtonIcon', 'disabled'))
        button.setEnabled(False)


class MainWindow(Window):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.button_1 = 'newWorkspaceButton'
        self.button_2 = 'settingsButton'
        self.button_3 = 'historyButton'

        # start = -80, step = 80

        self.add_push_button(attr_name=self.button_1, text='New Workspace',
                             width=200, height=50, x=0, y=-80, active=True,
                             clicked_callback=self.callbacks['add_workspace'],
                             icon=Icon.png('add'), icon_size=(25, 25),
                             style=Style.widgets('PushButton', 'active'),
                             parent=self)

        self.add_push_button(attr_name=self.button_2, text='Settings',
                             width=200, height=50, x=0, y=0, active=False,
                             clicked_callback=self.callbacks['show_settings'],
                             icon=Icon.png('controls'), icon_size=(25, 25),
                             style=Style.widgets('PushButton', 'disabled'),
                             parent=self)

        self.add_push_button(attr_name=self.button_3, text='History',
                             width=200, height=50, x=0, y=80, active=False,
                             clicked_callback=self.callbacks['show_history'],
                             icon=Icon.png('history'), icon_size=(25, 25),
                             style=Style.widgets('PushButton', 'disabled'),
                             parent=self)


class ToolsWindow(Window):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.button_1 = 'tensorPlotButton'
        self.button_2 = 'geoDashboard'
        self.button_3 = 'hessianMatrix'
        self.button_4 = 'latexGeneratorButton'

        # start = -80, step = 80

        self.add_push_button(attr_name=self.button_1, text='Tensor Plot',
                             width=200, height=50, x=0, y=-80, active=True,
                             clicked_callback=self.callbacks['show_tensor_plot_page'],
                             icon=Icon.png('tensor'), icon_size=(25, 25),
                             style=Style.widgets('PushButton', 'active'),
                             parent=self)

        self.add_push_button(attr_name=self.button_2, text='Geo Dashboard',
                             width=200, height=50, x=0, y=0, active=False,
                             clicked_callback=self.callbacks['show_geo_dashboard_page'],
                             icon=Icon.png('geo'), icon_size=(25, 25),
                             style=Style.widgets('PushButton', 'disabled'),
                             parent=self)

        self.add_push_button(attr_name=self.button_3, text='Hessian Matrix',
                             width=200, height=50, x=0, y=80, active=False,
                             clicked_callback=self.callbacks['show_hessian_matrix_page'],
                             icon=Icon.png('matrix'), icon_size=(25, 25),
                             style=Style.widgets('PushButton', 'disabled'),
                             parent=self)

        self.add_push_button(attr_name=self.button_4, text='Latex Generator',
                             width=200, height=50, x=0, y=160, active=False,
                             clicked_callback=self.callbacks['show_latex_generator_page'],
                             icon=Icon.png('editor'), icon_size=(25, 25),
                             style=Style.widgets('PushButton', 'disabled'),
                             parent=self)

        self.add_back_button(self.callbacks['back'])


class TensorPlotPage(Page):

    def __init__(self, *args, **kwargs):

        super(TensorPlotPage, self).__init__(*args, **kwargs)

        self.add_back_button(self.callbacks['back'])

    def init_layout(self):

        super().init_layout()

    def init_page(self):

        super().init_page()


class GeoDashboardPage(Page):

    def __init__(self, *args, **kwargs):

        super(GeoDashboardPage, self).__init__(*args, **kwargs)

        self.add_back_button(self.callbacks['back'])

    def init_layout(self):

        super().init_layout()

    def init_page(self):

        super().init_page()


class HessianMatrixPage(Page):

    def __init__(self, *args, **kwargs):

        super(HessianMatrixPage, self).__init__(*args, **kwargs)

        self.add_back_button(self.callbacks['back'])

    def init_layout(self):

        super().init_layout()

    def init_page(self):

        super().init_page()


class LatexGeneratorPage(Page):

    def __init__(self, *args, **kwargs):

        super(LatexGeneratorPage, self).__init__(*args, **kwargs)

        self.add_back_button(self.callbacks['back'])

    def init_layout(self):

        super().init_layout()

    def init_page(self):

        super().init_page()
