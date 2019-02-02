from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QCompleter, QShortcut, QPlainTextEdit, QStatusBar, QLabel
from PyQt5.QtGui import QFont, QKeySequence, QTextCursor
from PyQt5.QtCore import Qt, QPoint
from utils.predictionList import wordList
from utils.config import config_reader
from utils.search_algorithm import tokenize
from widgets.TextEditor import Editor

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
    def __init__(self, text, fileName, baseName, parent, window):
        super().__init__()
        self.editor = Editor(self)
        self.text = text
        self.window = window  # This is be the <Main> class
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
        self.editor.setText(str(text))
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

        self.editor.cursorPositionChanged.connect(self.change_col)

        if self.baseName.endswith(".py"):
            self.editor.python_highlighter()
        elif self.baseName.endswith(".c") or self.baseName.endswith(".cpp") or self.baseName.endswith(".h"):
            self.editor.c_highlighter()
        elif self.baseName.endswith(".json"):
            self.editor.json_highlighter()
        self.editor.cursorPositionChanged.connect(self.change_col)

    def change_col(self, line, column):
        self.line = line
        self.column = column
        self.status_bar.setText("Line: " + str(line) + " Column: " + str(column) + "           Total: " +
            str(self.editor.lines() - 1) + " lines" + "     Size: " + str(self.get_size(self.editor.text())) + " KiB")

        self.status_bar.setFont(QFont("Iosevka", 11))

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

    def getTextCursor(self):
        textCursor = self.editor.textCursor()
        textCursorPos = textCursor.position()

        return textCursor, textCursorPos

    def changeSaved(self):

        self.modified = self.editor.isModified()

        try:
            if self.modified:
                self.window.setWindowTitle("PyPad ~ " + str(self.baseName) + " [UNSAVED]")
            else:
                pass

        except NameError as E:
            print(E, " on line 124 in the file Content.py")
