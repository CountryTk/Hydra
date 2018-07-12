import os
import sys
import uuid

from PyQt5.QtGui import QTextOption
from PyQt5.QtWidgets import QWidget, QFileDialog, QPlainTextEdit, QGridLayout


from pypad import config, dialog, numbers, window, highlighter, utils


class PlainTextEdit(QPlainTextEdit):

    def __init__(self):
        super().__init__()
        self.replace_tabs = False
        if config.config.get('editor.replaceTabs'):
            self.replace_tabs = config.config.get('editor.spacesInTabs')

        self.setFont(config.config.font)
        self.setTabStopWidth(config.config.get('editor.tabWidth'))

        self.createStandardContextMenu()
        self.setWordWrapMode(QTextOption.NoWrap)

    def keyPressEvent(self, e):
        key = e.key()
        if key not in [16777217, 16777219, 16777220]:
            super().keyPressEvent(e)
            return

        e.accept()
        cursor = self.textCursor()

        if key == 16777217 and self.replace_tabs:
            amount = 4 - self.textCursor().positionInBlock() % 4
            self.insertPlainText(' ' * amount)

        elif key == 16777219 and cursor.selectionStart() == cursor.selectionEnd() and self.replace_tabs and \
                cursor.positionInBlock():
            position = cursor.positionInBlock()
            end = cursor.position()
            start = end - (position % 4)

            if start == end and position >= 4:
                start -= 4

            string = self.toPlainText()[start:end]
            if not len(string.strip()):
                for i in range(end - start):
                    cursor.deletePreviousChar()
            else:
                super().keyPressEvent(e)

        elif key == 16777220:
            end = cursor.position()
            start = end - cursor.positionInBlock()
            line = self.toPlainText()[start:end]
            indentation = len(line) - len(line.lstrip())

            chars = '\t'
            if self.replace_tabs:
                chars = '    '
                indentation /= self.replace_tabs

            if line.endswith(':'):
                if self.replace_tabs:
                    indentation += 1

            super().keyPressEvent(e)
            self.insertPlainText(chars * int(indentation))
        else:
            super().keyPressEvent(e)


class Editor(QWidget):

    def __init__(self, path: str=''):
        super().__init__()

        self.layout = QGridLayout(self)

        self.editor = PlainTextEdit()

        self.path = path

        if path:
            self.open_file()
        else:
            self.new_file()

        highlighter_class = None
        extension = os.path.splitext(self.path)[1][1:]
        for name, about in config.config.get('files').items():
            if extension in utils.make_list(about['extensions']):
                highlighter_class = getattr(highlighter, name.capitalize())

        if highlighter_class:
            self.highlighter = highlighter_class(self.editor.document())

        self.line_numbers = numbers.NumberBar(self.editor)

        self.layout.addWidget(self.line_numbers, 0, 0)
        self.layout.addWidget(self.editor, 0, 1)

    def get_name(self):
        return os.path.basename(self.path)

    def new_file(self):
        temp = '/tmp'
        if sys.platform == 'win32':
            temp = os.getenv('temp') or ''

        if not os.path.exists(temp):
            dialog.FatalError("Couldn't find your config directory")

        path = os.path.join(temp, 'pypad-' + str(uuid.uuid4()).split('-')[0] + '.txt')

        # try:
        #     open(path, 'a').close()
        # except PermissionError:
        #     dialog.FatalError("Couldn't write to", path)

        self.path = path
        self.editor.setPlainText('')

    def open_file(self):
        with open(self.path, 'r') as file:
            text = file.read()
        self.editor.setPlainText(text)

    def save(self):
        try:
            with open(self.path, 'w') as file:
                file.write(self.editor.toPlainText())
        except PermissionError:
            dialog.Error("Couldn't write to", self.path)

    def save_as(self):
        options = QFileDialog.Options()
        paths = QFileDialog.getSaveFileName(self, 'Save File', '',
                                            'All Files (*);;Python Files (*.py);;Text Files (*.txt)',
                                            options=options)
        self.path = paths[0]
        window.main_window.set_filename(self.path)
        self.save()
