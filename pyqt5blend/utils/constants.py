from PyQt5.QtCore import Qt

from ..api.common import OS, Reader, ResManger

__all__ = ['Res', 'Style', 'Icon']


class Res:

    MAIN_DIR = ResManger.get_intersect_path(dirname='pyqt5blend', current=__file__)
    print(MAIN_DIR)
    IMAGE_DIRS = [OS.join(MAIN_DIR, 'images')]

    CONFIG_DIR = OS.join(MAIN_DIR, '.config')

    PATH = {'style': OS.join(CONFIG_DIR, 'style.json')}

    KEY_NAME = ResManger.get_vars_name(Qt, Qt.Key)


class Icon:

    @staticmethod
    def get_icon_path(name, ext):

        filename = f'{name}.{ext}'

        if filename not in Res.PATH:

            img_dir = OS.file_at(filename, Res.IMAGE_DIRS)

            Res.PATH[filename] = OS.join(img_dir, filename)

        return Res.PATH[filename]

    @staticmethod
    def png(name):

        return Icon.get_icon_path(name, 'png')


class Style:

    DICT = Reader.json_to_dict(Res.PATH['style'])
    TEMPLATE = DICT['template']

    SOLID = 'solid'
    DASHED = 'dashed'

    Transparent = 'rgba(0, 0, 0, 0)'

    @staticmethod
    def background(name):

        return ''.join(Style.TEMPLATE['background'][name])

    @staticmethod
    def widgets(name, state):

        return ''.join(Style.TEMPLATE['widgets'][name][state])

    @staticmethod
    def border(size, btype, color):

        return f'border: {size}px {btype} {color};'

    @staticmethod
    def border_radius(radius):

        return f'border-radius: {radius}px;'

    @staticmethod
    def color(color):

        return f'color: {color};'

    @staticmethod
    def background_color(color):

        return f'background-color: {color};'
