import keyword

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QColor


from pypad import config


class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super().__init__(parent)
        self.file_type = self.__class__.__name__.lower()

        self.rules = self.get_rules()
        # make sure all expressions are contained in a list
        self.rules.update((key, [value]) for key, value in self.rules.items() if not isinstance(value, list))
        # convert regex stored as strings to QRegExp
        self.rules.update((key, [QRegExp(regex) for regex in value]) for key, value in self.rules.items())

        self.formats = {}

        for name in self.rules.keys():
            self.formats[name] = QTextCharFormat()

            if config.config.get(('files',  self.file_type, 'highlighting', name, 'bold'), False):
                self.formats[name].setFontWeight(QFont.Bold)
            if config.config.get(('files',  self.file_type, 'highlighting', name, 'italic'), False):
                self.formats[name].setFontItalic(True)

            self.formats[name].setForeground(QColor(config.config.get(('files.python.highlighting', name, 'color'))))

    def highlightBlock(self, text):
        for name, expressions in self.rules.items():
            for regex in expressions:
                index = regex.indexIn(text)
                while index >= 0:
                    length = regex.matchedLength()
                    self.setFormat(index, length, self.formats[name])
                    index = regex.indexIn(text, index + length)
        self.setCurrentBlockState(0)
        self.highlight_extra(text)

    def get_rules(self):
        return {}

    def highlight_extra(self, text):
        pass


class Python(Highlighter):

    def get_rules(self):
        rules = {
            "keyword": ['\\b' + word + '\\b' for word in keyword.kwlist],
            "class": '\\bclass\\b',
            "function": '[A-Za-z0-9_]+(?=\\()',
            "magic": '\__[^\']*\__',
            "decorator": '@[^\n]*',
            "int": '[-+]?[0-9]+',
            "string": [r'\'((?:\\\'|[^\'])*)\'', r'\"((?:\\\"|[^\"])*)\"'],
            "comment": '#[^\n]*',
            "multiLine": [],
        }
        return rules

    def highlight_extra(self, text):
        multi_line = QRegExp("'''")

        if self.previousBlockState() == 1:
            start_index = 0
            index_step = 0
        else:
            start_index = multi_line.indexIn(text)
            while start_index >= 0 and self.format(start_index+2) in self.formats.values():
                start_index = multi_line.indexIn(text, start_index + 3)
            index_step = multi_line.matchedLength()
        
        while start_index >= 0:
            end = multi_line.indexIn(text, start_index + index_step)
            if end != -1:
                self.setCurrentBlockState(0)
                length = end - start_index + multi_line.matchedLength()
            else:
                self.setCurrentBlockState(1)
                length = len(text) - start_index
            self.setFormat(start_index, length, self.formats['multiLine'])
            start_index = multi_line.indexIn(text, start_index + length)

