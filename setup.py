from setuptools import setup

APP = ['FolderCreatorGUI_Updated_UI.py']
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'icon.icns',  # Bu dosyayı bir sonraki adımda ekleyeceğiz
    'packages': ['tkinter'],
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
