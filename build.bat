@echo off
python setup.py build
pyinstaller build.spec --upx-dir=upx\
