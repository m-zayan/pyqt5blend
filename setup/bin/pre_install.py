import shutil
import fdir


def remove_cache(working_dir, name):

    dirs = fdir.walk(working_dir, './')

    for path in dirs:

        if name in path:

            print(f'Directory: {path}, has been removed')

            shutil.rmtree(path)


__working_dir__ = f'../../pyqt5blend'

remove_cache(__working_dir__, '__pycache__')
