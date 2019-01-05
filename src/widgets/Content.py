from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QCompleter, QShortcut, QPlainTextEdit, QStatusBar, QLabel
from PyQt5.QtGui import QFont, QKeySequence, QTextCursor
from PyQt5.QtCore import Qt, QPoint
from utils.predictionList import wordList
from utils.config import config_reader
from utils.search_algorithm import tokenize
from widgets.Editor import Editor
from widgets.Customize import Customize
from widgets.Completer import Completer
from widgets.Numberbar import NumberBar
import platform
from widgets.Pythonhighlighter import PyHighlighter
config0 = config_reader(0)
config1 = config_reader(1)
config2 = config_reader(2)

with open("default.json") as choice:
    choiceIndex = int(choice.read())

if choiceIndex == 0:
    editor = config0['editor']
elif choiceIndex == 1:
    editor = config1['editor']
elif choiceIndex == 2:
    editor = config2['editor']
else:
    editor = config0['editor']


class Content(QWidget):
    def __init__(self, text, fileName, baseName, themeIndex, parent, window):
        super().__init__()
        self.editor = Editor(self)
        self.text = text
        self.window = window  # This should be the Main class
        self.parent = parent
        self.status_bar = QStatusBar(self)
        self.wordlist = wordList
        self.fileName = fileName
        print(self.fileName)
        self.baseName = baseName
        self.temporary = 0
        self.font = QFont()
        self.custom = Customize()
        self.font.setFamily(editor["editorFont"])
        self.font.setPointSize(editor["editorFontSize"])
        self.tabSize = editor["TabWidth"]
        self.editor.textChanged.connect(self.changeSaved)
        self.custom = Customize()
        self.saved = True
        self.editor.setPlainText(str(text))
        self.test = QLabel(self)
        self.editor.cursorPositionChanged.connect(self.change_col)
        self.test.setText(str(platform.system()))

        if self.baseName.endswith(".py"):
            self.highlighter = PyHighlighter(self.editor.document(), index=self.custom.index)
            self.tokenize_file()
            self.test.setText(str(platform.system()) + "   " + "Python 3")
        else:
            pass

        self.main_layout = QVBoxLayout(self)
        self.hbox = QHBoxLayout()
        self.status_bar_layout = QHBoxLayout()
        self.status_bar = QStatusBar(self)
        # Create a widget for the line numbers
        # self.numbers = NumberBar(self.editor, index=themeIndex)
        # self.hbox.addWidget(self.numbers)
        self.hbox.addWidget(self.editor)
        self.status_bar_layout.addWidget(self.status_bar)
        self.status_bar_layout.addWidget(self.test)
        self.main_layout.addLayout(self.hbox)
        self.main_layout.addLayout(self.status_bar_layout)
        self.completer = Completer(self.wordlist)
        self.moveCursorRight = QShortcut(QKeySequence(editor["moveCursorRight"]), self)
        self.moveCursorLeft = QShortcut(QKeySequence(editor["moveCursorLeft"]), self)
        self.selectAllBeforeCursor = QShortcut(QKeySequence(editor["selectAllWordsBeforeCursor"]), self)
        self.moveUp = QShortcut(QKeySequence(editor["moveCursorUp"]), self)
        self.moveDown = QShortcut(QKeySequence(editor["moveCursorDown"]), self)

        self.moveDown.activated.connect(self.moveCursorDown)
        self.moveUp.activated.connect(self.moveCursorUp)
        self.selectAllBeforeCursor.activated.connect(self.selectBeforeCursor)
        self.moveCursorRight.activated.connect(self.moveCursorRightFunc)
        self.moveCursorLeft.activated.connect(self.moveCursorLeftFunc)
        self.editor.textChanged.connect(self.changeSaved)
        self.setCompleter(self.completer)

    def change_col(self):
        cursor = self.editor.textCursor()
        current_row = cursor.blockNumber()
        current_line = cursor.positionInBlock()
        self.status_bar.showMessage("Line: " + str(current_row) + " Column: " + str(current_line))

    def tokenize_file(self):

        for i in tokenize(self.fileName):
            for j in i:
                if j not in self.wordlist:
                    self.wordlist.append(j)
                    self.completer = Completer(self.wordlist)
                    self.setCompleter(self.completer)

    def getTextCursor(self):
        textCursor = self.editor.textCursor()
        textCursorPos = textCursor.position()

        return textCursor, textCursorPos

    def changeSaved(self):

        self.modified = self.editor.document().isModified()

        try:
            if self.modified:
                self.window.setWindowTitle("PyPad ~ " + str(self.baseName) + " [UNSAVED]")
            else:
                pass

        except NameError as E:
            print(E)

    def moveCursorRightFunc(self):
        textCursor, textCursorPos = self.getTextCursor()

        textCursor.setPosition(textCursorPos + 1)
        self.editor.setTextCursor(textCursor)

    def moveCursorUp(self):
        textCursor, textCursorPos = self.getTextCursor()

        textCursor.movePosition(textCursor.Up)
        self.editor.setTextCursor(textCursor)

    def moveCursorDown(self):
        textCursor, textCursorPos = self.getTextCursor()

        textCursor.movePosition(textCursor.Down)
        self.editor.setTextCursor(textCursor)

    def moveCursorLeftFunc(self):
        textCursor, textCursorPos = self.getTextCursor()

        textCursor.setPosition(textCursorPos - 1)
        self.editor.setTextCursor(textCursor)

    def selectBeforeCursor(self):
        textCursor, textCursorPos = self.getTextCursor()
        text = self.textUnderCursor()

        textCursor.movePosition(textCursor.StartOfWord, textCursor.KeepAnchor, len(text))
        self.editor.setTextCursor(textCursor)

    def setCompleter(self, completer):

        self.completer.setWidget(self)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer = completer

        self.completer.insertText.connect(self.insertCompletion)

    def insertCompletion(self, completion):
        textCursor = self.editor.textCursor()

        extra = (len(completion) - len(self.completer.completionPrefix()))

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
            self.completer.setWidget(self);
            QPlainTextEdit.focusInEvent(self, event)

    def keyPressEvent(self, event):

        if self.completer and self.completer.popup() and self.completer.popup().isVisible():
            if event.key() in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Escape, Qt.Key_Tab, Qt.Key_Backtab):
                event.ignore()
                return
        isShortcut = (event.modifiers() == Qt.ControlModifier and
                      event.key() == Qt.Key_Space)

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
        popup.setCurrentIndex(
            self.completer.completionModel().index(0, 0))

        cr = self.editor.cursorRect()
        cr.translate(QPoint(10, 10))
        cr.setWidth \
            (self.completer.popup().sizeHintForColumn(0) + self.completer.popup().verticalScrollBar().sizeHint().width())
        self.completer.complete(cr)

