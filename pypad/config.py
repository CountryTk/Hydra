import os
import sys
import json
import shutil


from PyQt5.QtGui import QFont


from pypad import dialog


class FakeDict:

    def __init__(self, main=None, fallback=None):
        super().__init__()
        self.main = main if main else {}
        self.fallback = fallback if fallback else {}

    def get(self, key, value=None):
        if key in self.main:
            if key not in self.fallback:
                self.fallback[key] = self.main[key]
            if isinstance(self.main[key], dict):
                return FakeDict(self.main[key], self.fallback[key])
            else:
                return self.main[key]
        if key in self.fallback:
            if isinstance(self.fallback[key], dict):
                return FakeDict(self.fallback[key], self.fallback[key])
            else:
                return self.fallback[key]
        return value

    def __getitem__(self, key):
        value = self.get(key)
        if value:
            return value
        dialog.FatalError("Couldn't find", key, "in config")

    def items(self):
        return self.main.items()


class Config:
    data = fallback = []

    def __init__(self, app_dir: str = ''):

        if app_dir:
            app_dir = os.path.expanduser(app_dir)
            if not os.path.exists(app_dir):
                dialog.FatalError(app_dir, "does not exist")
        else:
            local_config_dir = os.path.expanduser('~/.config')
            if sys.platform == 'darwin':
                local_config_dir = os.path.expanduser('~/Library/Application Support')
            elif sys.platform == 'win32':
                local_config_dir = os.getenv('APPDATA') or ''

            if not os.path.exists(local_config_dir):
                dialog.FatalError("Couldn't find your config directory")

            app_dir = os.path.join(local_config_dir, 'PyPad')
            if not os.path.exists(app_dir):
                try:
                    os.mkdir(app_dir)
                except PermissionError:
                    dialog.FatalError("Couldn't write to", local_config_dir)

        self.config_path = os.path.join(app_dir, 'config.json')
        if not os.path.exists(self.config_path):
            sample_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources/config.json')
            try:
                shutil.copyfile(sample_dir, self.config_path)
            except PermissionError:
                dialog.FatalError("Couldn't write to", self.config_path)
            except FileNotFoundError:
                dialog.FatalError("Couldn't read", sample_dir)

        self.load()
        self.font = self.font()

    def load(self):
        try:
            with open(self.config_path, 'r') as file:
                text = file.read()
                self.data = json.loads(text)

            with open(os.path.join(os.path.dirname(__file__), 'resources/config.json'), 'r') as file:
                text = file.read()
                self.fallback = json.loads(text)

        except FileNotFoundError:
            dialog.FatalError("Couldn't find", self.config_path)

    def save(self):
        try:
            with open(self.config_path, 'w') as file:
                text = json.dumps(self.data)
                file.write(text)

        except FileNotFoundError:
            dialog.FatalError("Couldn't find", self.config_path)

    def __setitem__(self, key, value):
        self.data.__setkey__(key, value)

    def __getitem__(self, key):
        return FakeDict(self.data, self.fallback)[key]

    def get(self, *args):
        return FakeDict(self.data, self.fallback).get(*args)

    def font(self):
        font = QFont()
        font.setFamily(self.data['editor']['editorFont'])
        font.setPointSize(self.data['editor']['editorFontSize'])
        font.setFixedPitch(True)
        return font


config = Config()
