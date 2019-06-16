"""
This file contains all the important stuff for the actual 'code' editor
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QCompleter, QPlainTextEdit,\
    QLabel, QTextEdit, QToolTip, QAction, QApplication, QMenu, QInputDialog
from PyQt5.QtGui import QFont, QTextCursor, QTextOption, QColor, QTextCharFormat, QCursor, QTextFormat,\
    QPainter
from PyQt5.QtCore import Qt, QPoint, QSize, QProcess, QRect, pyqtSignal
from pypad.utils.config import config_reader, LOCATION
from pypad.utils.completer_utility import tokenize
from pypad.utils.find_utility import find_all
from pypad.utils.completer_utility import wordList
from pypad.widgets.Pythonhighlighter import PyHighlighter
from pypad.widgets.Messagebox import MessageBox
import platform


configs = [config_reader(0), config_reader(1), config_reader(2)]

with open(LOCATION + "default.json") as choice:
    choiceIndex = int(choice.read())

editor = configs[choiceIndex]['editor']


class Content(QWidget):
    def __init__(self, text, fileName, baseName, parent, isReadOnly=False):
        super().__init__()
        self.editor = Editor(self, isReadOnly)
        self.text = text
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
                self.parent.setWindowTitle("PyPad ~ " + str(self.baseName) + " [UNSAVED]")
            else:
                pass

        except NameError as E:
            print(E, " on line 124 in the file Content.py")


class QLineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)


class Editor(QPlainTextEdit):

    def __init__(self, parent, isReadOnly=False):
        super().__init__(parent)
        self.lineNumberArea = QLineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateLineNumberAreaWidth(0)
        self.setReadOnly(isReadOnly)
        self.parent = parent
        self.font = QFont()
        self.size = 12
        self.worldList = wordList
        self.dialog = MessageBox(self)
        self.menu_font = QFont()
        self.menu_font.setFamily(editor["menuFont"])
        self.menu_font.setPointSize(editor["menuFontSize"])
        self.font.setFamily(editor["editorFont"])
        self.font.setPointSize(editor["editorFontSize"])
        self.focused = None
        self.text = None
        self.replace_tabs = 4
        self.setWordWrapMode(4)
        self.setFont(self.font)
        self.l = 0
        self.highlightingRules = []
        self.extraSelections_ = []
        self.indexes = None
        self.setMouseTracking(True)

        self.completer = None

        self.info_process = QProcess()

        self.setTabStopWidth(editor["TabWidth"])
        self.createStandardContextMenu()
        self.setWordWrapMode(QTextOption.NoWrap)

        self.cursorPositionChanged.connect(self.getColAndRow)
        self.info_process.readyReadStandardOutput.connect(self.get_pydoc_output)

    def getTextCursor(self):
        textCursor = self.textCursor()
        textCursorPos = textCursor.position()

        return textCursor, textCursorPos

    def getColAndRow(self):

        textCursor = self.getTextCursor()[0]

        # print("row: {} column: {}".format(textCursor.blockNumber(), textCursor.positionInBlock()))

    def totalLines(self):
        return self.blockCount()

    def is_modified(self):
        return self.document().isModified()

    def check(self):
        cursor = self.textCursor()
        b = cursor.block()
        extraSelections = []
        if len(b.text()) > 120:
            selection = QTextEdit.ExtraSelection()
            # TODO: implement something using flake8
            selection.format.setFontUnderline(True)
            selection.format.setUnderlineColor(QColor("#FF0000"))

            selection.format.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)

            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()

            self.extraSelections_.append(selection)
            self.setExtraSelections(self.extraSelections_)

            font = QFont()
            font.setFamily("Iosevka")
            font.setPointSize(10)

            QToolTip.setFont(font)
            cursor = self.textCursor()
            current_line = cursor.positionInBlock()
            QToolTip.showText(QCursor.pos(), "Line too long (" + str(current_line) + "> 120) | violation on line: " +
                              str(b.blockNumber() + 1))

    def newFile(self):
        """This is a wrapper for the function defined in Main"""

        self.new_action = QAction("New")
        self.new_action.triggered.connect(self.parent.parent.newFile)

    def lineNumberAreaWidth(self):
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        space = 10 + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor("#434343")
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)
        self.check()
        return extraSelections

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)

        painter.fillRect(event.rect(), QColor("#303030"))

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        # Just to make sure I use the right font
        height = self.fontMetrics().height()

        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                painter.setPen(Qt.white)
                painter.drawText(0, top, self.lineNumberArea.width(), height, Qt.AlignCenter, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

    def openFile(self):

        self.open_action = QAction("Open")
        self.open_action.triggered.connect(self.parent.parent.openFileFromMenu)

    def runFile(self):

        self.run_action = QAction("Run")
        self.run_action.triggered.connect(self.parent.parent.execute_file)

    def textUnderCursor(self):
        textCursor = self.textCursor()
        textCursor.select(QTextCursor.WordUnderCursor)

        return textCursor.selectedText()

    def moveCursorPosBack(self):
        textCursor = self.textCursor()
        textCursorPos = textCursor.position()

        textCursor.setPosition(textCursorPos - 1)
        self.setTextCursor(textCursor)

    def mouseMoveEvent(self, QMouseEvent):

        # font = textCursor.block().charFormat().font()
        # metrics = QFontMetrics(font)
        #
        # b = self.document().findBlockByLineNumber(0)
        #
        # cursor = QTextCursor(b)
        #
        # cursor.select(QTextCursor.BlockUnderCursor)
        #
        # cursor.removeSelectedText()
        #
        # height = metrics.height() + 2
        # y = QMouseEvent.pos().y()
        #print(y, height)
        #print(y/height)
        cursor_main = self.cursorForPosition(QMouseEvent.pos())
        if QApplication.queryKeyboardModifiers() == Qt.ControlModifier:

            cursor_main.select(QTextCursor.WordUnderCursor)
            text = cursor_main.selectedText()
            self.text = text
            if self.text is not None:
                url = "https://docs.python.org/3/library/functions.html#" + self.text
                word = self.text
                # self.parent.parent.showBrowser(url, word)

                if self.check_func(word):
                    extraSelections = self.highlightCurrentLine()
                    selection = QTextEdit.ExtraSelection()
                    selection.format.setFontUnderline(True)
                    selection.format.setUnderlineColor(QColor("#00d2ff"))
                    selection.format.setForeground(QColor("#00d2ff"))
                    selection.format.setProperty(QTextFormat.FullWidthSelection, True)
                    selection.cursor = self.cursorForPosition(QMouseEvent.pos())
                    selection.cursor.select(QTextCursor.WordUnderCursor)
                    extraSelections.append(selection)
                    self.setExtraSelections(extraSelections)
                    cursor = QCursor(Qt.PointingHandCursor)
                    # tooltip = QToolTip()
                    QToolTip.setFont(QFont(editor["ToolTipFont"], editor["ToolTipFontSize"]))
                    word_shown = eval(word).__doc__

                    if len(word_shown) > 2000:
                        word_shown = word_shown[:2000]

                    QToolTip.showText(QCursor.pos(), "{}".format(word_shown))
                    QApplication.setOverrideCursor(cursor)
                    QApplication.changeOverrideCursor(cursor)
                else:
                    self.returnCursorToNormal()
            else:

                pass
        else:
            self.returnCursorToNormal()
            extraSelections = self.highlightCurrentLine()
            self.setExtraSelections(extraSelections)

        super().mouseMoveEvent(QMouseEvent)

    def returnCursorToNormal(self):
        cursor = QCursor(Qt.ArrowCursor)
        QApplication.setOverrideCursor(cursor)
        QApplication.changeOverrideCursor(cursor)

    def mousePressEvent(self, e):

        self.check()
        if QApplication.queryKeyboardModifiers() == Qt.ControlModifier:

            super().mousePressEvent(e)
            self.text = self.textUnderCursor()
            if self.text is not None:
                word = self.text
                # self.parent.parent.showBrowser(url, word)

                if self.check_func(self.textUnderCursor(), True):
                    extraSelections = self.highlightCurrentLine()
                    selection = QTextEdit.ExtraSelection()
                    selection.format.setFontUnderline(True)
                    selection.format.setUnderlineColor(QColor("#00d2ff"))
                    selection.format.setForeground(QColor("#00d2ff"))
                    selection.format.setProperty(QTextFormat.FullWidthSelection, True)
                    selection.cursor = self.textCursor()
                    selection.cursor.clearSelection()
                    selection.cursor.select(QTextCursor.WordUnderCursor)
                    extraSelections.append(selection)
                    self.setExtraSelections(extraSelections)
                    self.text = self.textUnderCursor()

                    # cursor = QCursor(Qt.PointingHandCursor)

                    # QApplication.setOverrideCursor(cursor)
                    # QApplication.changeOverrideCursor(cursor)

                else:
                    self.text = None
        else:
            super().mousePressEvent(e)
        QApplication.restoreOverrideCursor()
        # super().mousePressEvent(e)

    def check_func(self, word, clicked=False):
        funcs = [
            "abs", "all", "any", "ascii", "bin", "bool", "breakpoint", "bytearray", "bytes", "callable",
            "chr", "classmethod",
            "compile", "complex",
            "delattr", "dict", "dir", "divmod", "enumerate", "eval", "exec", "filter", "float",
            "format",
            "frozenset",
            "getattr", "globals", "hasattr", "hash",
            "help", "hex", "id", "input", "int", "isinstance", "issubclass", "iter", "len", "list",
            "locals", "map",
            "max", "memoryview", "min", "next", "object",
            "oct", "open", "ord", "pow", "print", "property", "range", "repr", "reversed", "round",
            "set", "setattr", "slice", "sorted", "staticmethod", "str", "sum",
            "super", "tuple", "type", "vars", "zip", "__import__"
        ]

        word_array = list(word)

        for wo in word_array:
            if wo in ["{", "}", "'", '"', "[", "]", "(", ")"]:
                word_array.remove(wo)
        for w in funcs:
            if w == "".join(word_array):
                if clicked:
                    if self.info_process.state() == 0:
                        self.info_process.start("pydoc {}".format(word))
                    else:
                        pass

                return True

    def get_pydoc_output(self):
        output = self.info_process.readAllStandardOutput().data().decode()
        self.parent.parent.open_documentation(output, self.info_process.arguments()[0])

    def contextMenuEvent(self, event):

        menu = QMenu()

        """Initializing actions"""
        self.newFile()
        self.openFile()
        self.runFile()
        menu.addAction(self.new_action)
        menu.addAction(self.open_action)
        menu.addAction(self.run_action)

        menu.setFont(self.menu_font)

        menu.exec(event.globalPos())


        del menu

    def mouseReleaseEvent(self, e):

        self.check()
        super().mouseReleaseEvent(e)

    def keyPressEvent(self, e):
        textCursor = self.textCursor()
        key = e.key()
        if e.modifiers() == Qt.ControlModifier and key == 16777217:  # that key code stands for tab
            self.parent.parent.switchTabs()

        isSearch = (e.modifiers() == Qt.ControlModifier and e.key() == Qt.Key_F)

        isDeleteLine = (e.modifiers() == Qt.ControlModifier and e.key() == 16777219)  # This is for MacOS (CMD+Delete)

        if isSearch:
            try:
                currentWidget = self.parent
                currentFile = currentWidget.fileName
                currentEditor = currentWidget.editor

                textCursor = currentEditor.textCursor()
                textCursorPos = textCursor.position()
                if currentWidget is not None:
                    text, okPressed = QInputDialog.getText(self, 'Find', 'Find what: ')
                    if okPressed:
                        if text == "":
                            text = " "
                            self.dialog.noMatch(text)
                        self.searchtext = text
                        try:
                            with open(currentFile, 'r') as file:
                                contents = file.read()
                                self.indexes = list(find_all(contents, text))
                                if len(self.indexes) == 0:
                                    self.dialog.noMatch(text)

                        except FileNotFoundError as E:
                            print(E, " on line 245 in the file Editor.py")

            except (AttributeError, UnboundLocalError) as E:
                print(E, " on line 228 in the file Editor.py")

        if isDeleteLine and platform.system() == "Darwin":  # Check if the os is MacOS
            textCursor.select(QTextCursor.LineUnderCursor)
            textCursor.removeSelectedText()

        if key == Qt.Key_QuoteDbl:
            self.insertPlainText('"')
            self.moveCursorPosBack()

        if e.modifiers() == Qt.ControlModifier and e.key() == 61:  # Press Ctrl+Equal key to make font bigger

            self.font.setPointSize(self.size + 1)
            self.font.setFamily(editor["editorFont"])
            self.setFont(self.font)
            self.size += 1

        if e.modifiers() == Qt.ControlModifier and e.key() == 16777217:
            return

        if e.modifiers() == Qt.ControlModifier and e.key() == 45:  # Press Ctrl+Minus key to make font smaller

            self.font.setPointSize(self.size - 1)

            self.font.setFamily(editor["editorFont"])
            self.setFont(self.font)
            self.size -= 1

        if key == Qt.Key_F3:
            try:
                index = self.indexes[0 + self.l]
                currentWidget = self.parent
                currentFile = currentWidget.fileName
                currentEditor = currentWidget.editor
                textCursor.setPosition(index)
                textCursor.movePosition(textCursor.Right, textCursor.KeepAnchor, len(self.searchtext))
                currentEditor.setTextCursor(textCursor)
                self.l += 1
            except IndexError:
                self.l = 0

        if key == 39:
            self.insertPlainText("'")
            self.moveCursorPosBack()

        if key == Qt.Key_BraceLeft:
            self.insertPlainText("}")
            self.moveCursorPosBack()

        if key == Qt.Key_BracketLeft:
            self.insertPlainText("]")
            self.moveCursorPosBack()

        if key == Qt.Key_ParenLeft:
            self.insertPlainText(")")
            self.moveCursorPosBack()

        if key == Qt.Key_ParenRight:
            textCursor = self.textCursor()
            textCursor.select(QTextCursor.WordUnderCursor)
            if textCursor.selectedText() == "()" or "()" in textCursor.selectedText():
                return

        if key == Qt.Key_BraceRight:
            textCursor = self.textCursor()
            textCursor.select(QTextCursor.WordUnderCursor)
            if textCursor.selectedText == "":
                return
        if key == 16777219:
            if self.textUnderCursor() in ['""', '()', '[]', "''", "{}"]:
                textCursor = self.textCursor()
                textCursorPos = textCursor.position()

                textCursor.setPosition(textCursorPos + 1)
                textCursor.deletePreviousChar()
                self.setTextCursor(textCursor)
        if key not in [16777217, 16777219, 16777220]:
            super().keyPressEvent(e)
            # print(self.textUnderCursor())
            if len(self.textUnderCursor()) == 3:
                pass
            return

        # e.accept()
        cursor = self.textCursor()
        if key == 16777217:  # and self.replace_tabs:
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
            if not len(string.strip()):  # if length is 0 which is binary for false
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


class Completer(QCompleter):
    insertText = pyqtSignal(str)

    def __init__(self, myKeywords=None, parent=None):
        self.wordList = wordList
        QCompleter.__init__(self, myKeywords, parent)

        self.activated.connect(self.changeCompletion)

    def changeCompletion(self, completion):

        self.insertText.emit(completion)
