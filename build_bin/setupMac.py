from setuptools import setup

APP = ['spotimini.py']
DATA_FILES = ['./img/', 'state.json']
OPTIONS ={
    'argv_emulation': True,
    'iconfile': 'icon.icns'
    }

setup(
    name='SpotiMini',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app']
)
