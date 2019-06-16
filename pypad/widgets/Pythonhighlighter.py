from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt5.QtCore import QRegExp
import keyword
from pypad.utils.config import config_reader, LOCATION

config0 = config_reader(0)
config1 = config_reader(1)
config2 = config_reader(2)

with open(LOCATION + "default.json") as choice:
    choiceIndex = int(choice.read())

if choiceIndex == 0:
    editor = config0['editor']
elif choiceIndex == 1:
    editor = config1['editor']
elif choiceIndex == 2:
    editor = config2['editor']
else:
    editor = config0['editor']


class PyHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None, index=choiceIndex, *args):
        super(PyHighlighter, self).__init__(parent, *args)

        if index == "0":
            python = config0['files']['python']

        elif index == "1":
            python = config1['files']['python']

        elif index == "2":
            python = config2['files']['python']
        else:
            python = config0['files']['python']  # This is the default config

        self.highlightingRules = []
        self.formats = {}
        self.regex = {
            "class": "\\bclass\\b",
            "function": "[A-Za-z0-9_]+(?=\\()",
            "magic": "\\__[^']*\\__",
            "decorator": "@[^\n]*",
            "multiLineComment": "[-+]",
            "int": "\\b[-+]?[0-9]+\\b",
            "Qclass": "\\b[Q|q][A-Za-z]+\\b",
            "self": "\\bself\\b",
            "T_bool": "\\bTrue\\b",
            "F_bool": "\\bFalse\\b",
            "N_bool": "\\bNone\\b",
            "singleLineComment": "#[^\n]*",
            "quotation": "\"[^\"]*\"",
            "quotation2": "'[^\']*\'",
        }

        pyKeywordPatterns = keyword.kwlist

        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor(python['highlighting']['keyword']['color']))
        keywordFormat.setFontWeight(QFont.Bold)

        self.highlightingRules = [(QRegExp('\\b' + pattern + '\\b'), keywordFormat) for pattern in pyKeywordPatterns]

        for name, values in self.regex.items():
            self.formats[name] = QTextCharFormat()

            if name == "class":
                self.formats[name].setFontWeight(QFont.Bold)

            elif name == "function":
                self.formats[name].setFontItalic(True)

            elif name == "magic":
                self.formats[name].setFontItalic(True)

            self.formats[name].setForeground(QColor(python['highlighting'][name]['color']))

            self.highlightingRules.append((QRegExp(values), self.formats[name]))

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)
        self.setCurrentBlockState(0)
        self.multiLineHighlight(text)

    def multiLineHighlight(self, text):

        comment = QRegExp('"""')
        if self.previousBlockState() == 1:
            start_index = 0
            index_step = 0
        else:
            start_index = comment.indexIn(text)
            while start_index >= 0 and self.format(start_index+2) in self.formats.values():
                start_index = comment.indexIn(text, start_index + 3)
            index_step = comment.matchedLength()

        while start_index >= 0:
            end = comment.indexIn(text, start_index + index_step)
            if end != -1:
                self.setCurrentBlockState(0)
                length = end - start_index + comment.matchedLength()
            else:
                self.setCurrentBlockState(1)
                length = len(text) - start_index

            self.setFormat(start_index, length, self.formats['multiLineComment'])
            start_index = comment.indexIn(text, start_index + length)
