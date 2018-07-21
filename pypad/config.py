import os
import sys
import json
import shutil


from PyQt5.QtGui import QFont


from pypad import dialog, utils


class Config:
    merged = main = fallback = []

    def __init__(self, app_dir: str = ''):
        """
        finds the location of the required config files based on operating system, can be overridden
        load configs from this location and sets them ready for reading
        :param app_dir: app's data directory
        """
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
        """
        load config from disk
        """
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
        """
        store the merged values of the main and fallback configs
        """
        self.merged = utils.merge(self.fallback, self.main)

    def save(self):
        """
        write current config to disk
        """
        try:
            with open(self.config_path, 'w') as file:
                text = json.dumps(self.main)
                file.write(text)

        except FileNotFoundError:
            dialog.FatalError("Couldn't find", self.config_path)

    def get(self, name=None, default=None):
        """
        get a config value
        :param name: key to fetch
        :param default: value to fallback to if the key is not found
        :return: requested config value
        """
        if name is None:
            return self.merged
        if isinstance(name, list) or isinstance(name, tuple):
            name = '.'.join(name)
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
        """
        set and overwrite a config value
        :param name: the key to change
        :param value: the value to set
        """
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
        """
        flatten a multi-dimensional dictionary
        :return: flattened dict
        """
        return utils.flatten(self.merged)

    def font(self):
        """
        create font for for the editor
        :return: editor font
        """
        font = QFont()
        font.setFamily(self.get('editor.editorFont'))
        font.setPointSize(self.get('editor.editorFontSize'))
        font.setFixedPitch(True)
        return font


config = Config()
