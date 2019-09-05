from PyQt5.QtGui import (
    QSyntaxHighlighter,
    QTextCharFormat,
    QColor,
    QFont,
    QTextCursor,
    QTextLayout,
    QTextBlock,
)
from PyQt5.QtCore import QRegExp, QObject, QPoint, pyqtSignal
import keyword
from Hydra.utils.config import config_reader, LOCATION
from Hydra.utils.find_utility import find_all

config0 = config_reader(0)
config1 = config_reader(1)
config2 = config_reader(2)

with open(LOCATION + "default.json") as choice:
    choiceIndex = int(choice.read())

if choiceIndex == 0:
    editor = config0["editor"]
elif choiceIndex == 1:
    editor = config1["editor"]
elif choiceIndex == 2:
    editor = config2["editor"]
else:
    editor = config0["editor"]


class PyHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None, editor=None, index=choiceIndex, *args):
        super(PyHighlighter, self).__init__(parent, *args)

        if index == "0":
            python = config0["files"]["python"]

        elif index == "1":
            python = config1["files"]["python"]

        elif index == "2":
            python = config2["files"]["python"]
        else:
            python = config0["files"]["python"]  # This is the default config

        self.highlightingRules = []
        self.formats = {}

        self.editor = editor
        self.parent = parent

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
            "quotation": '"[^"]*"',
            "quotation2": "'[^']*'",
        }

        pyKeywordPatterns = keyword.kwlist

        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor(python["highlighting"]["keyword"]["color"]))
        keywordFormat.setFontWeight(QFont.Bold)

        self.highlightingRules = [
            (QRegExp("\\b" + pattern + "\\b"), keywordFormat)
            for pattern in pyKeywordPatterns
        ]

        for name, values in self.regex.items():
            self.formats[name] = QTextCharFormat()

            if name == "class":
                self.formats[name].setFontWeight(QFont.Bold)

            elif name == "function":
                self.formats[name].setFontItalic(True)

            elif name == "magic":
                self.formats[name].setFontItalic(True)

            self.formats[name].setForeground(
                QColor(python["highlighting"][name]["color"])
            )

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
            while (
                start_index >= 0
                and self.format(start_index + 2) in self.formats.values()
            ):
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

            self.setFormat(start_index, length, self.formats["multiLineComment"])
            start_index = comment.indexIn(text, start_index + length)


class SyntaxHighlighter(QObject):
    """

    """

    lineSignal = pyqtSignal(list)

    def __init__(self, editor, index=choiceIndex):

        super(SyntaxHighlighter, self).__init__()

        self.editor = editor
        self.document = self.editor.document()
        self.target = self.calculate_target()
        self.highlighted_lines = 250
        self.start_from = 37

        if index == "0":
            python = config0["files"]["python"]

        elif index == "1":
            python = config1["files"]["python"]

        elif index == "2":
            python = config2["files"]["python"]
        else:
            python = config0["files"]["python"]  # This is the default config

        self.highlightingRules = []
        self.formats = {}

        self.random_array = []

        self.editor = editor

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
            "quotation": '"[^"]*"',
            "quotation2": "'[^']*'",
        }

        pyKeywordPatterns = keyword.kwlist

        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor(python["highlighting"]["keyword"]["color"]))
        keywordFormat.setFontWeight(QFont.Bold)

        self.highlightingRules = [
            (QRegExp("\\b" + pattern + "\\b"), keywordFormat)
            for pattern in pyKeywordPatterns
        ]

        for name, values in self.regex.items():
            self.formats[name] = QTextCharFormat()

            if name == "class":
                self.formats[name].setFontWeight(QFont.Bold)

            elif name == "function":
                self.formats[name].setFontItalic(True)

            elif name == "magic":
                self.formats[name].setFontItalic(True)

            self.formats[name].setForeground(
                QColor(python["highlighting"][name]["color"])
            )

            self.highlightingRules.append((QRegExp(values), self.formats[name]))

        self.visibleTextBlocks = []  # stores QTextBlocks

        self.running = True
        self.i = 0

    def calculate_target(self) -> int:

        self.x = self.editor.blockCount() / 45

        self.target = self.editor.blockCount() / self.x

        return self.target

    def visibleBlocks(self):

        startPos = self.editor.cursorForPosition(QPoint(0, 0)).position()
        bottomRight = QPoint(
            self.editor.viewport().width() - 1, self.editor.viewport().height() - 1
        )

        endPos = self.editor.cursorForPosition(bottomRight).position()

        cursor = self.editor.textCursor()
        cursor.setPosition(startPos)

        startBlock = cursor.block()
        cursor.setPosition(endPos)

        endBlock = cursor.block()
        startLine = startBlock.firstLineNumber()
        endLine = endBlock.firstLineNumber() + cursor.block().lineCount()

        self.lineSignal.emit([startLine, endLine])

        m = startBlock
        self.visibleTextBlocks.append(m)
        while m.isValid() and m != endBlock:

            m = m.next()
            self.visibleTextBlocks.append(m)

    def onFirstOpen(self):

        endBlock = self.editor.document().findBlockByLineNumber(500)
        a = []
        start = self.editor.firstVisibleBlock()
        a.append(start)

        while start != endBlock:
            start = start.next()
            a.append(start)

        return a

    def highlightOneBlock(self, block):

        layout = block.layout()
        if not layout:
            return self.editor.blockCount()

        ranges = layout.formats()

        if len(ranges) > 0:
            ranges.clear()

        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(block.text())

            while index >= 0:
                length = expression.matchedLength()
                formatrange = QTextLayout.FormatRange()

                formatrange.format = format
                formatrange.length = length
                formatrange.start = index

                ranges.append(formatrange)

                layout.setFormats(ranges)
                self.editor.document().markContentsDirty(
                    block.position(), block.length()
                )
                index = expression.indexIn(block.text(), index + length)

    def highlightBlocks(self, justOpened=False):

        if justOpened:  # Highlight more than the user can see

            self.visibleTextBlocks = self.onFirstOpen()

        for block in self.visibleTextBlocks:

            layout = block.layout()

            ranges = layout.formats()
            for pattern, format in self.highlightingRules:
                expression = QRegExp(pattern)
                index = expression.indexIn(block.text())
                while index >= 0:
                    length = expression.matchedLength()
                    formatrange = QTextLayout.FormatRange()

                    formatrange.format = format
                    formatrange.length = length
                    formatrange.start = index

                    ranges.append(formatrange)

                    layout.setFormats(ranges)
                    self.editor.document().markContentsDirty(
                        block.position(), block.length()
                    )
                    index = expression.indexIn(block.text(), index + length)
