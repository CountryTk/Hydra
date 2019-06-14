from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QCompleter, QShortcut, QPlainTextEdit, QStatusBar, QLabel
from PyQt5.QtGui import QFont, QKeySequence, QTextCursor
from PyQt5.QtCore import Qt, QPoint
from src.utils.predictionList import wordList
from src.utils.config import config_reader
from src.utils.search_algorithm import tokenize
from src.widgets.Editor import Editor
from src.widgets.Pythonhighlighter import PyHighlighter
from src.widgets.Completer import Completer

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
    def __init__(self, text, fileName, baseName, parent, window, isReadOnly=False):
        super().__init__()
        self.editor = Editor(self, isReadOnly)
        self.text = text
        self.window = window  # This is the <Main> class
        self.parent = parent
        self.wordlist = wordList
        self.fileName = fileName
        self.baseName = baseName
        self.temporary = 0
        self.font = QFont()
        self.font.setFamily(editor["editorFont"])
        self.font.setPointSize(editor["editorFontSize"])
        self.tabSize = editor["TabWidth"]
        self.editor.textChanged.connect(self.changeSaved)
        self.saved = True
        self.editor.setPlainText(str(text))
        self.main_layout = QVBoxLayout(self)
        self.hbox = QHBoxLayout()
        self.status_bar_layout = QHBoxLayout()
        self.status_bar = QLabel(self)
        # Create a widget for the line numbers
        self.hbox.addWidget(self.editor)
        self.status_bar_layout.addWidget(self.status_bar)
        self.status_bar_layout.addWidget(self.status_bar, Qt.AlignLeft)
        self.main_layout.addLayout(self.hbox)
        self.main_layout.addLayout(self.status_bar_layout)

        self.line = None
        self.column = None

        self.completer = Completer(self.wordlist)
        self.setCompleter(self.completer)

        if self.baseName.endswith(".py"):
            self.highlighter = PyHighlighter(self.editor.document())
        elif self.baseName.endswith(".doc"):
            self.highlighter = PyHighlighter(self.editor.document())
        self.editor.cursorPositionChanged.connect(self.change_col)

    def change_col(self):
        textCursor = self.editor.textCursor()

        line = textCursor.blockNumber() + 1
        column = textCursor.positionInBlock()
        self.status_bar.setText("Line: " + str(line) + " Column: " + str(column) + "           Total: " +
            str(self.editor.totalLines() - 1) + " lines" + "     Size: " + str(self.get_size(self.editor.toPlainText())) + " KiB")

        self.status_bar.setFont(QFont(editor["statusBarFont"], editor["statusBarFontSize"]))

    def get_size(self, input):
        return round(len(input.encode("utf-8"))/1000)

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

    def checkIfCanComplete(self):

        pass

    def keyPressEvent(self, event):

        if self.completer and self.completer.popup() and self.completer.popup().isVisible():
            if event.key() in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Escape, Qt.Key_Tab, Qt.Key_Backtab):
                event.ignore()
                return

        isShortcut = (event.modifiers() == Qt.ControlModifier and
                      event.key() == Qt.Key_B)

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

    def getTextCursor(self):
        textCursor = self.editor.textCursor()
        textCursorPos = textCursor.position()

        return textCursor, textCursorPos

    def changeSaved(self):

        self.modified = self.editor.is_modified()

        try:
            if self.modified:
                self.window.setWindowTitle("PyPad ~ " + str(self.baseName) + " [UNSAVED]")
            else:
                pass

        except NameError as E:
            print(E, " on line 124 in the file Content.py")
