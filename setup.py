#!/usr/bin/python3
# -*- coding: utf-8 -*-

from sys import platform
from cx_Freeze import setup, Executable

executables = [
    Executable('program.py', targetName='prog.exe', base='Console')
]

excludes = [
    'html', 'pydoc_data', 'unittest', 'xml', 'pwd', 'shlex', 'platform', 'webbrowser', 'pydoc', 'tty',
    'inspect', 'doctest', 'plistlib', 'subprocess', 'bz2', '_strptime', 'dummy_threading'
]

zip_include_packages = [
    'collections', 'encodings', 'importlib', 'codecs', 'abc', 'sys',
    'hashlib', 'logging', 'unicodedata', 'progress'
]

options = {
    'build_exe': {
        'excludes': excludes,
        'include_msvcr': True,
        'build_exe': 'cx_build',
        'zip_include_packages': zip_include_packages,
    }
}

setup(
    name='File hash checker',
    version='0.1',
    #description='',
    executables=executables,
    options=options,
    requires=['hashlib', 'progress'],
)
