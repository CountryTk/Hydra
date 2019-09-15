"""
This file contains all the important stuff for the actual 'code' editor
"""

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QCompleter,
    QPlainTextEdit,
    QLabel,
    QTextEdit,
    QToolTip,
    QAction,
    QApplication,
    QMenu,
    QInputDialog,
)
from PyQt5.QtGui import (
    QFont,
    QTextCursor,
    QTextOption,
    QTextBlock,
    QColor,
    QTextCharFormat,
    QCursor,
    QTextFormat,
    QPainter,
    QTextLayout,
)
from PyQt5.QtCore import Qt, QPoint, QSize, QProcess, QRect, pyqtSignal, QRegExp, QEvent
from Hydra.utils.config import config_reader, LOCATION
from Hydra.utils.completer_utility import tokenize
from Hydra.utils.find_utility import find_all
from Hydra.utils.completer_utility import wordList
from Hydra.widgets.Pythonhighlighter import PyHighlighter
from Hydra.widgets.Pythonhighlighter import PyHighlighter
from Hydra.widgets.OpenFile import OpenFile
from Hydra.widgets.SaveFile import SaveFile
from Hydra.widgets.Editor import Editor, Completer
from Hydra.widgets.numberBar import NumberBar
from Hydra.widgets.foldArea import FoldArea
from Hydra.widgets.Label import StatusLabel
from PyQt5.QtTest import QTest
import os

configs = [config_reader(0), config_reader(1), config_reader(2)]

with open(LOCATION + "default.json") as choice:
    choiceIndex = int(choice.read())

editor = configs[choiceIndex]["editor"]


class Content(QWidget):

    readyToShow = pyqtSignal(bool)

    def __init__(
        self, text, fileName, baseName, parent, isReadOnly=False, searchCommand=None
    ):
        super().__init__()

        self.lazy = None
        if os.path.isfile(fileName):
            self.size_of_file = os.path.getsize(fileName)
            self.lazy = True  # If file exists then we can lazy load it

        else:
            self.size_of_file = 0
            self.lazy = False

        self.editor = Editor(self, isReadOnly)
        self.numberbar = NumberBar(self.editor)
        self.foldArea = FoldArea(self.editor)

        self.stack = []
        self.text = text
        self.parent = parent
        self.wordlist = wordList
        self.fileName = fileName
        self.baseName = baseName
        self.setting_up = 0
        self.temporary = 0

        self.searchCommand = searchCommand
        self.font = QFont()
        self.font.setFamily(editor["editorFont"])
        self.font.setPointSize(editor["editorFontSize"])
        self.tabSize = editor["TabWidth"]

        self.highlighter = PyHighlighter(self.editor)
        self.currentBlockCount = None
        self.saved = True
        self.editor.setPlainText(str(text))
        self.main_layout = QVBoxLayout(self)
        self.hbox = QHBoxLayout()

        self.status_bar_layout = QHBoxLayout()
        self.statusBarFont = QFont(editor["statusBarFont"], editor["statusBarFontSize"])
        self.columnLabel = StatusLabel(text="", font=self.statusBarFont)
        self.rowLabel = StatusLabel(text="", font=self.statusBarFont)
        self.totalLineLabel = StatusLabel(text="", font=self.statusBarFont)

        self.open_file = OpenFile()
        self.save_file = SaveFile(self)

        self.open_file.add_args(self.fileName, self.lazy)
        # Create a widget for the line numbers
        self.hbox.addWidget(self.numberbar)
        self.hbox.addWidget(self.foldArea)
        self.hbox.addWidget(self.editor)

        self.hbox.setSpacing(0)

        self.status_bar_layout.addWidget(self.columnLabel)
        self.status_bar_layout.addSpacing(10)
        self.status_bar_layout.addWidget(self.rowLabel)
        self.status_bar_layout.addSpacing(10)
        self.status_bar_layout.addWidget(self.totalLineLabel)
        self.status_bar_layout.addStretch()

        self.main_layout.addLayout(self.hbox)
        self.main_layout.addLayout(self.status_bar_layout)
        self.open_file.dataSignal.connect(
            self.insertText
        )  # This causes a bug if the cursor isn't in a position
        self.open_file.readDone.connect(self.readCompleted)
        # self.save_file.updateOffset.connect(lambda amount: self.change_offset(amount))

        self.open_file.readDone.connect(self.opening)
        # self.open_file.readAmountSignal.connect(self.prepare_to_save) lazy load [not working]
        # self.open_file.EndOfFileSignal.connect(self.EOF) lazy load [not working]

        self.IO_status = QLabel("Opening...")
        self.IO_status.setFont(self.font)

        self.save_file.readDone.connect(self.saving)

        self.line = None
        self.column = None
        # self.opening = True
        self.startLine = None
        self.endLine = None

        self.end = [False, 0]
        self.start_from = 0

        self.completer = Completer(self.wordlist)
        self.setCompleter(self.completer)

        if self.baseName.endswith(".py"):
            self.highlighter = PyHighlighter(self.editor.document(), self.editor)
        elif self.baseName.endswith(".doc"):
            self.highlighter = PyHighlighter(self.editor.document(), self.editor)

        self.editor.cursorPositionChanged.connect(self.change_col)
        # self.editor.textChanged.connect()

    def assignLines(self, array: list) -> None:

        self.startLine = array[0]
        self.endLine = array[1]

    def change_read_amount(self, amount: int) -> None:

        self.open_file.change_read_amount(amount)

    def change_offset(self, amount: int) -> None:

        self.open_file.change_offset(amount)

    def opening(self, state: bool) -> None:

        if state:
            self.readyToShow.emit(True)

    def saving(self, state: bool) -> None:

        if state:  # Saving has finished

            pass  # TODO: indicate that we have finished

        else:

            pass  # TODO: Indicate that we haven't finished

    def start_saving(self):

        self.save_file.add_args(self)
        self.save_file.start()

    def readCompleted(self, state: bool) -> None:

        if state:

            self.initialize(True)

    def initialize(self, justOpened=False):
        """
        After content is loaded into the file, this function will handle jump to definition when opening a file
        """
        QTest.qWait(5)  # Without this, it won't work

        if self.searchCommand:

            self.searchFor(self.searchCommand)

    def searchFor(self, searchCommand: str):

        regex = QRegExp(searchCommand)

        index = find_all(self.editor.toPlainText(), searchCommand)
        a = list(index)

        textCursor = self.editor.textCursor()
        try:
            textCursor.setPosition(a[0])
            textCursor.movePosition(
                textCursor.Right, textCursor.KeepAnchor, regex.matchedLength()
            )
            self.editor.setTextCursor(textCursor)

        except Exception as E:
            pass

    def jumpToDef(self, tagList: list):

        tagInfo = tagList[0]
        fileName = tagList[1]
        searchCommand = tagList[2]

        if fileName.split("/")[-1] == self.baseName:
            self.searchFor(searchCommand)

        self.parent.cleanOpen(fileName, False, searchCommand)

    def EOF(self, data: list) -> None:
        """

        :param data[0]: bool
        :param data[1]: int
        :return: None
        """

        if data[0]:

            self.end = [*data]  # unpack the data

        else:  # this should never happen
            self.end = False

    def insertText(self, text: str) -> None:

        cursor = QTextCursor(self.editor.document())

        cursor.movePosition(QTextCursor.End)

        self.editor.setTextCursor(cursor)

        self.editor.insertPlainText(text)

    def prepare_to_save(self, array):

        currently_read_bytes = array[0]
        maximum_bytes = array[1]
        """If the user hasn't scrolled to the bottom
        (lazy loading isn't completed) and saves the file. no data gets lost"""
        self.start_from = currently_read_bytes

    def decide(self, array):  # Right now this function is not used anywhere

        """
        Decides if we lazy load text to the user or not
        :param array:
        :return: None
        """

        if not self.lazy:
            return
        else:
            text_size = len(self.editor.toPlainText().encode("utf-8"))
            if self.size_of_file != text_size:
                min_value = array[0]
                max_value = array[1]

                if min_value == max_value:
                    self.open_file.our_start()

    def start_opening(self):

        self.open_file.start()

    def change_col(self):
        textCursor = self.editor.textCursor()

        line = textCursor.blockNumber() + 1
        column = textCursor.positionInBlock()

        """self.status_bar.setText(
            "Line: "
            + str(line)
            + " Column: "
            + str(column)
            + "           Total: "
            + str(self.editor.totalLines() - 1)
            + " lines"
            + "     Size: "
            + str(self.size_of_file / 1000)
            + " KiB"
        )"""

        self.rowLabel.setText("Ln: {}".format(line))
        self.columnLabel.setText("Col: {}".format(column))
        self.totalLineLabel.setText("Total: {}".format(self.editor.totalLines()))

        self.editor.highlightCurrentLine()

    def get_size(self, input):
        return round(len(input.encode("utf-8")) / 1000)

    def leaveEvent(self, event: QEvent) -> None:

        self.editor.returnCursorToNormal()
        super().leaveEvent(event)

    def code_info(self, data):
        counter = 1
        keywords = {}
        text_array = data.splitlines()

        for w in text_array:
            word = w.strip()
            if word.startswith("class ") or word.startswith("def "):
                keywords[counter] = word.strip()

            counter += 1
        return keywords

    def tokenize_file(self):

        for i in tokenize(self.fileName):
            for j in i:
                if j not in self.wordlist:
                    self.wordlist.append(j)

    def setCompleter(self, completer):

        self.completer.setWidget(self)

        completer.setCompletionMode(QCompleter.PopupCompletion)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer = completer

        self.completer.insertText.connect(self.insertCompletion)

    def insertCompletion(self, completion):
        textCursor = self.editor.textCursor()

        extra = len(completion) - len(self.completer.completionPrefix())

        textCursor.movePosition(QTextCursor.Left)

        textCursor.movePosition(QTextCursor.EndOfWord)
        textCursor.insertText(completion[-extra:])

        if completion.endswith("()"):
            cursorPos = textCursor.position()
            textCursor.setPosition(cursorPos - 1)

        self.editor.setTextCursor(textCursor)

    def textUnderCursor(self):
        textCursor = self.editor.textCursor()
        textCursor.select(QTextCursor.WordUnderCursor)

        return textCursor.selectedText()

    def focusInEvent(self, event):
        if self.completer:
            self.completer.setWidget(self)
            QPlainTextEdit.focusInEvent(self, event)

    def checkIfCanComplete(self):

        pass

    def keyPressEvent(self, event):

        if (
            self.completer
            and self.completer.popup()
            and self.completer.popup().isVisible()
        ):
            if event.key() in (
                Qt.Key_Enter,
                Qt.Key_Return,
                Qt.Key_Escape,
                Qt.Key_Tab,
                Qt.Key_Backtab,
            ):
                event.ignore()
                return

        isShortcut = event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_B

        if not self.completer or not isShortcut:
            QPlainTextEdit.keyPressEvent(self.editor, event)

        completionPrefix = self.textUnderCursor()

        if not isShortcut:
            if self.completer.popup():
                self.completer.popup().hide()
            return

        self.completer.setCompletionPrefix(completionPrefix)

        popup = self.completer.popup()

        popup.setFont(self.font)
        popup.setCurrentIndex(self.completer.completionModel().index(0, 0))

        cr = self.editor.cursorRect()
        cr.translate(QPoint(10, 10))
        cr.setWidth(
            self.completer.popup().sizeHintForColumn(0)
            + self.completer.popup().verticalScrollBar().sizeHint().width()
        )
        self.completer.complete(cr)

    def getTextCursor(self):
        textCursor = self.editor.textCursor()
        textCursorPos = textCursor.position()

        return textCursor, textCursorPos

    def changeSaved(self):
        self.modified = self.editor.is_modified()

        try:
            if self.modified:
                self.parent.setWindowTitle(
                    "Hydra ~ " + str(self.baseName) + " [UNSAVED]"
                )

            else:
                pass

        except NameError as E:
            print(E, " on line 124 in the file Content.py")
