from setuptools import setup

import fdir


def load():

    pkg_dir = 'pyqt5blend'
    working_dir = f'../../{pkg_dir}'

    def process_path(path):

        return f"{pkg_dir}.{path[len(working_dir) + 1:].replace('/', '.')}"

    dirs = []
    ignore_substr = ['__', 'images', '.config']

    # fdir.walk(...), doesn't support hidden files.
    for d in fdir.walk(working_dir, './'):

        ignore = 0

        for substr in ignore_substr:

            if substr in d:
                ignore = 1

        if ignore:
            continue

        dirs.append(d)

    _packages = list(map(process_path, dirs))

    return _packages


packages = load()

setup(
    name='pyqt5blend',
    version='1.0.0',
    description='PyQt5 Desktop App Templates',
    url='https://github.com/m-zayan/pyqt5blend',
    packages=packages,
    package_dir={'': '../../'},
    author='Mohamed Zayan',
    author_email='zayanm410@gmail.com',
    license='MIT',
    keywords=['PyQt5', 'Templates'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License'],
    zip_safe=False,
    include_package_data=True)

print(packages)
