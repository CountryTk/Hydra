import os
import sys
import uuid

from PyQt5.QtGui import QTextOption, QTextCursor
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

        self.locked_lines = []

    def keyPressEvent(self, e):
        key = e.text()
        cursor = self.textCursor()
        # if the event is on a locked line except if the event is just movement or selection
        line_locked = cursor.block().blockNumber() in self.locked_lines and key and key not in ['\x01', '\x03']

        if line_locked:
            # if return pressed
            if key == '\r':
                # if the cursor isn't at the start
                if cursor.positionInBlock():
                    # move cursor to the end of the line
                    for _ in range(self.toPlainText()[cursor.position():].find('\n')):
                        self.moveCursor(QTextCursor.Right, QTextCursor.MoveAnchor)
                # then create the new line
                super().keyPressEvent(e)

            # if backspace pressed
            elif key == '\x08':
                self.moveCursor(QTextCursor.Left, QTextCursor.MoveAnchor)

        # if tab pressed and they want it replaced with spaces
        elif key == '\t' and self.replace_tabs:
            # insert the number spaces needed
            self.insertPlainText(' ' * (self.replace_tabs - self.textCursor().positionInBlock() % self.replace_tabs))

        # if backspace pressed, the cursor is at the start of the line and the line above is blocked
        elif key == '\x08' and not cursor.positionInBlock() and cursor.block().blockNumber() - 1 in self.locked_lines:
            # if nothing else on the line
            start = cursor.position()
            if self.toPlainText()[start:start + 1] in ['', '\n']:
                super().keyPressEvent(e)

        # if backspace is pressed, nothing is selected, changing tabs to spaces and the cursor is not at the start
        elif key == '\x08' and cursor.selectionStart() == cursor.selectionEnd() and self.replace_tabs and \
                cursor.positionInBlock():
            position = cursor.positionInBlock()
            end = cursor.position()
            start = end - (position % 4)
            if start == end and position >= 4:
                start -= 4

            string = self.toPlainText()[start:end]
            if len(string.strip()):
                super().keyPressEvent(e)
                return
            for i in range(end - start):
                cursor.deletePreviousChar()

        # if return is pressed
        elif key == '\r':
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
