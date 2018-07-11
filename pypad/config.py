import os
import sys
import json
import shutil


from PyQt5.QtGui import QFont


from pypad import dialog, utils


class Config:
    merged = main = fallback = []

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
                self.main = json.loads(text)

            with open(os.path.join(os.path.dirname(__file__), 'resources/config.json'), 'r') as file:
                text = file.read()
                self.fallback = json.loads(text)

        except FileNotFoundError:
            dialog.FatalError("Couldn't find", self.config_path)

        self.merge()

    def merge(self):
        self.merged = utils.merge(self.fallback, self.main)

    def save(self):
        try:
            with open(self.config_path, 'w') as file:
                text = json.dumps(self.main)
                file.write(text)

        except FileNotFoundError:
            dialog.FatalError("Couldn't find", self.config_path)

    def get(self, name=None, default=None):
        if name is None:
            return self.merged
        keys = name.split('.')
        section = self.merged
        try:
            for key in keys:
                section = section[key]
            return section
        except KeyError:
            if default is not None:
                return default
        dialog.FatalError("Couldn't find", name)

    def set(self, name, value):
        keys = name.split('.')
        section = self.main
        for key in keys[:-1]:
            if key not in section:
                section[key] = {}
            section = section[key]
        section[keys[-1]] = value
        self.merge()

    def items(self):
        return self.merged.items()

    def flat(self):
        return utils.flatten(self.merged)

    def font(self):
        font = QFont()
        font.setFamily(self.get('editor.editorFont'))
        font.setPointSize(self.get('editor.editorFontSize'))
        font.setFixedPitch(True)
        return font


config = Config()
