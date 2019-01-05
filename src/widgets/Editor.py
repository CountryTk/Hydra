from builtins import print
from PyQt5.QtWidgets import QPlainTextEdit, QAction, QMenu, QInputDialog, QTextEdit, QWidget
from PyQt5.QtCore import Qt, QRect, QSize
from PyQt5.QtGui import QFont, QTextOption, QTextCursor, QTextFormat, QPainter, QColor
from utils.find_all import find_all
from widgets.Messagebox import MessageBox
from utils.config import config_choice

editor = config_choice("default.json")['editor']


class QLineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)
        

class Editor(QPlainTextEdit):

    def __init__(self, parent):
        super().__init__(parent)
        self.lineNumberArea = QLineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateLineNumberAreaWidth(0)
        self.parent = parent
        self.font = QFont()
        self.size = 12
        self.dialog = MessageBox()
        self.menu_font = QFont()
        self.menu_font.setFamily("Iosevka")
        self.menu_font.setPointSize(10)
        self.font.setFamily(editor["editorFont"])
        self.font.setPointSize(editor["editorFontSize"])
        self.focused = None

        self.replace_tabs = 4
        self.setWordWrapMode(4)
        self.setFont(self.font)
        self.l = 0
        self.highlightingRules = []
        self.indexes = None

        self.setTabStopWidth(editor["TabWidth"])
        self.createStandardContextMenu()
        self.setWordWrapMode(QTextOption.NoWrap)

    def newFile(self):
        """This and most of the functions below will just be wrappers for the functions defined in Main"""
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

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)

        painter.fillRect(event.rect(), QColor("#303030"))

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber() - 1
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
        self.run_action.triggered.connect(self.parent.parent.terminal)

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

    def moveCursorPosBack(self):
        textCursor = self.textCursor()
        textCursorPos = textCursor.position()

        textCursor.setPosition(textCursorPos - 1)
        self.setTextCursor(textCursor)

    def keyPressEvent(self, e):
        textCursor = self.textCursor()
        key = e.key()

        if key == Qt.Key_H:
            # self.parent.completer.wordList
            # TODO: implement dynamic completion
            pass

        textCursorPos = textCursor.position()
        isSearch = (e.modifiers() == Qt.ControlModifier and e.key() == Qt.Key_F)

        if isSearch:
            try:
                currentWidget = self.parent
                currentFile =  currentWidget.fileName
                currentEditor = currentWidget.editor

                textCursor = currentEditor.textCursor()
                textCursorPos = textCursor.position()

            except (AttributeError, UnboundLocalError) as E:
                print(E)

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
                        print(E)

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
                currentFile =  currentWidget.fileName
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

        if key not in [16777217, 16777219, 16777220]:

            super().keyPressEvent(e)
            return

        e.accept()
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
            if not len(string.strip()): # if length is 0 which is binary for false
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
