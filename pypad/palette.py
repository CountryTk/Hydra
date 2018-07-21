from PyQt5.QtGui import QPalette, QColor

from pypad import config


class Palette(QPalette):

    def __init__(self):
        """
        create colour palette to apply to the application
        """
        super().__init__()

        colors = {QPalette.Base: 'editor',
                  QPalette.Text: 'editorText',
                  QPalette.Window: 'window',
                  QPalette.WindowText: 'windowText',
                  QPalette.AlternateBase: 'alternateBase',
                  QPalette.ToolTipBase: 'toolTipBase',
                  QPalette.ToolTipText: 'toolTipText',
                  QPalette.Button: 'button',
                  QPalette.ButtonText: 'buttonText',
                  QPalette.Highlight: 'highlight',
                  QPalette.HighlightedText: 'highlightedText',
                  }

        # for item in colors.keys():
        #    attr = item[0].upper() + item[1:]
        #    self.setColor(getattr(QPalette, attr), QColor(config.config['editor']['colors'].get(item)))

        for attribute, name in colors.items():
            self.setColor(attribute, QColor(config.config.get(('editor.colors', name))))


