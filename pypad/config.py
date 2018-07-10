import os
import sys
import json
import shutil


from pypad import dialog


class Config:
    data = []

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

    def load(self):
        try:
            with open(self.config_path, 'r') as file:
                text = file.read()
                self.data = json.loads(text)

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
        self.data.__setitem__(key, value)

    def __getitem__(self, key):
        return self.data.__getitem__(key)

    def __getattribute__(self, item):
        try:
            return super(Config, self).__getattribute__(item)
        except AttributeError:
            if item in self.data:
                return self.data[item]

    def get(self, *args):
        return self.data.get(*args)


config = Config()
