#!/bin/sh

pip uninstall pyqt5blend
rm -r ./build ./dist ../../pyqt5blend.egg-info

python pre_install.py
python setup.py install
