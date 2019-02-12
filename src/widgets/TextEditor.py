from builtins import print
from utils.search_algorithm import tokenize
from PyQt5.Qsci import QsciScintilla, QsciLexerPython, QsciAPIs, QsciLexerCPP, QsciLexerJSON
from PyQt5.QtGui import QFont, QFontMetrics, QColor, QGuiApplication
from PyQt5.QtWidgets import QInputDialog
from PyQt5.Qt import Qt
from utils.predictionList import wordList, funcList, errorList
from widgets.Messagebox import MessageBox
from utils.config import config_reader

with open("default.json") as choice:
    choiceIndex = int(choice.read())
configs = [config_reader(0), config_reader(1), config_reader(2)]
editor = configs[choiceIndex]['editor']

class PythonLexer(QsciLexerPython):
    def __init__(self):
        super().__init__()

    def keywords(self, index):
        keywords = QsciLexerPython.keywords(self, index) or ''
        if index == 1:
            return 'self ' + ' super ' + keywords


class Editor(QsciScintilla):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.fileName = None
        self.parent = parent
        self.debugging = False
        self.line = None
        self.column = None

        self.wordlist = []
        self.searchtext = None

        self.font = QFont()
        self.font.setFamily("Inconsolata")
        self.pointSize = editor["pointSize"] # TODO: Make this customizable
        self.tabWidth = editor["TabWidth"]  # TODO: Make this customizable
        self.font.setPointSize(self.pointSize)
        self.dialog = MessageBox(self)
        self.verticalScrollBar().setStyleSheet(
            """
            background-color: transparent;
            """)

        self.horizontalScrollBar().setStyleSheet(
            """
            background-color: transparent;
            """)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setCaretForegroundColor(QColor("#FFFFFF"))
        self.setEdgeColumn(121)
        self.setEdgeMode(1)
        self.setEdgeColor(QColor("#8c8c8c"))
        self.setFont(self.font)
        self.setMarginSensitivity(1, True)
        self.markerDefine(QsciScintilla.RightArrow, 8)
        self.setMarkerBackgroundColor(QColor('#FF0000'), 8)
        self.indicator_number = 0
        self.indicator_value = 222
        self.indicator_color = QColor("#FF0000")
        self.draw_under_text = True
        # Initializing some stuff
        self.set_brace_colors(QColor("#98b4f9"), QColor("#edf40e"), QColor("#98b4f9"), QColor("red"))

        self.cursorPositionChanged.connect(self.change_col)
        self.textChanged.connect(self.check_lines)

        self.set_linenumbers(QFontMetrics(self.font))
        self.setFoldMarginColors(QColor("#212121"), QColor("#212121"))
        self.set_indentation_settings(self.tabWidth)

    def set_up_tooltips(self):
        self.setCallTipsStyle(QsciScintilla.CallTipsNoContext)
        self.setCallTipsVisible(0)

        self.setCallTipsPosition(QsciScintilla.CallTipsAboveText)
        self.setCallTipsBackgroundColor(QColor("#FF0000"))

        self.setCallTipsForegroundColor(QColor("#FF0000"))
        self.setCallTipsHighlightColor(QColor("#FF0000"))

    def set_brace_colors(self, matched_B=None, matched_F=None, unmatched_B=None, unmatched_F=None):

        self.setMatchedBraceBackgroundColor(matched_B)
        self.setMatchedBraceForegroundColor(matched_F)
        self.setUnmatchedBraceBackgroundColor(unmatched_B)
        self.setUnmatchedBraceForegroundColor(unmatched_F)

        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)

    def set_linenumbers(self, fontmetrics):
        self.setMarginsFont(self.font)

        self.setMarginWidth(0, fontmetrics.width("00000"))
        self.setMarginLineNumbers(0, True)

        self.setMarginsBackgroundColor(QColor("#212121"))
        self.setMarginsForegroundColor(QColor("#FFFFFF"))

    def set_indentation_settings(self, tab_width):
        self.setIndentationsUseTabs(False)

        self.setTabWidth(tab_width)

        self.SendScintilla(QsciScintilla.SCI_SETUSETABS, False)

        self.setAutoIndent(True)
        self.setTabIndents(True)

    def check_lines(self):
        line_n = self.lines()
        for i in range(line_n):
            if self.lineLength(i) > 121:
                # TODO: Make a character format or something
                pass
                #  print("Line over 121 characters on line", str(i+1))
                # self.setCursorPosition(i, 120)

    def python_highlighter(self):
        self.lexer = PythonLexer()
        self.lexer.setFoldComments(True)
        self.setCaretLineVisible(True)

        self.setDefaultSettings(self.lexer)
        self.setPythonAutocomplete()
        self.setFold()

    def json_highlighter(self):
        lexer = QsciLexerJSON()
        self.setDefaultSettings(lexer)

    def c_highlighter(self):
        lexer = QsciLexerCPP()

        self.setDefaultSettings(lexer)

    def setDefaultSettings(self, lexer):
        self.setAutoIndent(True)
        lexer.setFont(self.font)

        lexer.setColor(QColor('white'), 0)  # default
        lexer.setColor(QColor('#6B6E6C'), PythonLexer.Comment)  # = 1
        lexer.setColor(QColor('#ADD4FF'), 2)  # Number = 2
        lexer.setColor(QColor('#38ef7d'), 3)  # DoubleQuotedString
        lexer.setColor(QColor('#38ef7d'), 4)  # SingleQuotedString
        lexer.setColor(QColor('#F6DC74'), 5)  # Keyword
        lexer.setColor(QColor('#38ef7d'), 6)  # TripleSingleQuotedString
        lexer.setColor(QColor('#38ef7d'), 7)  # TripleDoubleQuotedString
        lexer.setColor(QColor('#74F6C3'), 8)  # ClassName
        lexer.setColor(QColor('#FF6666'), 9)  # FunctionMethodName
        lexer.setColor(QColor('magenta'), 10)  # Operator
        lexer.setColor(QColor('white'), 11)  # Identifier
        lexer.setColor(QColor('gray'), 12)  # CommentBlock
        lexer.setColor(QColor('#a8ff78'), 13)  # UnclosedString
        lexer.setColor(QColor('gray'), 14)  # HighlightedIdentifier
        lexer.setColor(QColor('#FF00E7'), 15)  # Decorator

        lexer.setFont(QFont("Iosevka", weight=QFont.Bold), 5)
        self.setCaretLineBackgroundColor(QColor("#3C3B3F"))
        self.setLexer(lexer)

    def setPythonAutocomplete(self):
        self.autocomplete = QsciAPIs(self.lexer)
        self.keywords = wordList

        for word in self.keywords:
            self.autocomplete.add(word)

        self.setAutoCompletionThreshold(2)

        self.setAutoCompletionSource(QsciScintilla.AcsAPIs)
        self.updateAutoComplete(self.parent.fileName)

        self.autocomplete.prepare()

    def setFold(self):
        # setup Fold Styles for classes and functions ...
        x = self.FoldStyle(self.FoldStyle(5))
        # self.textPad.folding()
        if not x:
            self.foldAll(False)

        self.setFolding(x)
        # self.textPad.folding()

    def unsetFold(self):
        self.setFolding(0)

    def updateAutoComplete(self, file_path=None):

        for i in tokenize(file_path):
            for j in i:
                if j not in self.wordlist:
                    self.wordlist.append(j)
        for word in self.wordlist:
            self.autocomplete.add(word)

        self.autocomplete.prepare()

    def change_col(self, line, column):  # Responsible for changing the column bar.
        self.line = line
        self.column = column

    def check_if_func(self, word):  # Checks if a word is a built in function
        word_array = list(word)
        for wo in word_array:
            if wo in ["{", "}", "'", '"', "[", "]", "(", ")"]:
                word_array.remove(wo)
        for w in funcList:
            if w == "".join(word_array):
                return True

    def check_if_error(self, word):
        if word in errorList:  # This is the list where all possible errors are defined
            return True

    def keyReleaseEvent(self, e):
        if e.key() == Qt.Key_Return:
            try:
                self.updateAutoComplete(self.parent.fileName)
            except AttributeError as E:
                print(E, "on line 210 in TextEditor.py")

        if e.key() == Qt.Key_Backspace:
            pass

    def mousePressEvent(self, e):
        super().mousePressEvent(e)

        if QGuiApplication.queryKeyboardModifiers() == Qt.ControlModifier:
            word = self.wordAtLineIndex(self.getCursorPosition()[0], self.getCursorPosition()[1])
            print(word)
            if self.check_if_func(word):
                url = "https://docs.python.org/3/library/functions.html#" + word
                self.parent.parent.openBrowser(url, word)  # Runs the openBrowser function in Main class
            elif self.check_if_error(word):
                url = "https://docs.python.org/3/library/exceptions.html#" + word
                print(url)

                self.parent.parent.openBrowser(url, word)

    def keyPressEvent(self, e):
        if e.modifiers() == Qt.ControlModifier and e.key() == Qt.Key_F:
            text, okPressed = QInputDialog.getText(self, 'Find', 'Find what: ')

            self.setSelectionBackgroundColor(QColor("#6be585"))

            if okPressed:
                if text == "":
                    text = " "
                    self.dialog.noMatch(text)

                self.searchtext = text

                """
                This is the way to implement a search function using QScintilla 
                http://pyqt.sourceforge.net/Docs/QScintilla2/classQsciScintilla.html#a37ac2bea94eafcfa639173557a821200
                """

                if self.findFirst(self.searchtext, False, True, False, True, True, -1, -1, True, False):
                    pass
                else:
                    self.dialog.noMatch(self.searchtext)

        if e.key() == Qt.Key_F3:
            self.findNext()
            self.setSelectionBackgroundColor(QColor("#6be585"))

        if e.modifiers() == Qt.ControlModifier and e.key() == Qt.Key_L:
            self.setCursorPosition(self.line, self.column + 1)
            return
        if e.modifiers() == Qt.ControlModifier and e.key() == 77:

            self.setCursorPosition(self.line + 1, self.column)
            return
        if e.modifiers() == Qt.ControlModifier and e.key() == Qt.Key_J:
            self.setCursorPosition(self.line, self.column - 1)

        if e.modifiers() == Qt.ControlModifier and e.key() == Qt.Key_I:
            self.setCursorPosition(self.line - 1, self.column)

        if e.modifiers() == Qt.ControlModifier and e.key() == Qt.Key_T:
            self.parent.parent.realterminal()
            return

        super().keyPressEvent(e)
