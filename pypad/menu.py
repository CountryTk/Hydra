from PyQt5.QtWidgets import QAction, QFileDialog


from pypad import config, tabs, window, dialog, settings


class Menu:

    def __init__(self):

        shortcuts = {
            'Undo': {'shortcut': 'Ctrl+Z', 'action': tabs.tabs.get_current().editor.undo},
            'Redo': {'shortcut': 'Shift+Ctrl+Z', 'action': tabs.tabs.get_current().editor.redo},
            'Cut': {'shortcut': 'Ctrl+X', 'action': tabs.tabs.get_current().editor.cut},
            'Copy': {'shortcut': 'Ctrl+C', 'action': tabs.tabs.get_current().editor.copy},
            'Paste': {'shortcut': 'Ctrl+V', 'action': tabs.tabs.get_current().editor.paste},
            'Select All': {'shortcut': 'Ctrl+A', 'action': tabs.tabs.get_current().editor.selectAll},
            'New': {'shortcut': 'Ctrl+N', 'tip': 'Create a new file', 'action': tabs.tabs.new_tab},
            'Open': {'shortcut': 'Ctrl+O', 'tip': 'Open a file', 'action': tabs.tabs.open},
            'Quit': {'shortcut': 'Ctrl+Q', 'tip': 'Exit application', 'action': dialog.Quit},
            'Save': {'shortcut': 'Ctrl+S', 'tip': 'Save a file', 'action': tabs.tabs.get_current().save},
            'Save As': {'shortcut': 'Ctrl+Shift+S', 'tip': 'Save a file as', 'action': tabs.tabs.get_current().save_as},
            'Settings': {'shortcut': 'Ctrl+Alt+S', 'tip': 'Open settings window', 'action': settings.Settings},
        }

        actions = {}

        for name, values in shortcuts.items():
            actions[name] = QAction(name, window.main_window)
            actions[name].setShortcut(values.get('shortcut'))
            actions[name].setStatusTip(values.get('tip', name))
            actions[name].triggered.connect(values.get('action'))

        for name, items in config.config.get('menus').items():
            menu = window.main_window.menuBar().addMenu(name)
            for item in items:
                if item == 'Separator':
                    menu.addSeparator()
                    continue
                menu.addAction(actions[item])
