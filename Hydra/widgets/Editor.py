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
    QStyleOptionViewItem,
    QStyle,
)
from PyQt5.QtGui import (
    QFont,
    QTextCursor,
    QTextOption,
    QColor,
    QTextCharFormat,
    QCursor,
    QTextFormat,
    QPainter,
    QTextLayout,
    QTextBlock,
    QPaintEvent,
    QMouseEvent,
    QFontMetricsF,
)
from PyQt5.QtCore import (
    Qt,
    QPoint,
    QSize,
    QProcess,
    QRect,
    pyqtSignal,
    QRegExp,
    QMimeData,
    QRectF,
    QPointF,
)
from Hydra.utils.config import config_reader, LOCATION
from Hydra.utils.completer_utility import tokenize
from Hydra.utils.find_utility import find_all
from Hydra.utils.completer_utility import wordList
from Hydra.widgets.Pythonhighlighter import PyHighlighter
from Hydra.widgets.Messagebox import MessageBox, NoMatch
from Hydra.widgets.OpenFile import OpenFile
from Hydra.widgets.SaveFile import SaveFile
import platform
from PyQt5.QtTest import QTest
import os


configs = [config_reader(0), config_reader(1), config_reader(2)]

with open(LOCATION + "default.json") as choice:
    choiceIndex = int(choice.read())

editor = configs[choiceIndex]["editor"]


class Editor(QPlainTextEdit):
    def __init__(self, parent, isReadOnly=False):
        super().__init__(parent)

        self.setReadOnly(isReadOnly)
        self.parent = parent

        self.font = QFont()
        self.size = 12
        self.setUpdatesEnabled(True)
        self.worldList = wordList
        self.menuFont = QFont()
        self.menuFont.setFamily(editor["menuFont"])
        self.menuFont.setPointSize(editor["menuFontSize"])
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
        self.currentlyVisibleBlocks: list = []
        self.foldableBlocks = []
        self.indexes = None
        self.setMouseTracking(True)
        self.completer = None

        self.setTabStopDistance(QFontMetricsF(self.font).width(" ") * 4)

        self.ignoreLength = None

        self.foldableLines: list = []

        self.info_process = QProcess()

        self.setTabStopWidth(editor["TabWidth"])
        self.createStandardContextMenu()
        self.setWordWrapMode(QTextOption.NoWrap)

        self.info_process.readyReadStandardOutput.connect(self.get_pydoc_output)

    def getTextCursor(self):
        textCursor = self.textCursor()
        textCursorPos = textCursor.position()

        return textCursor, textCursorPos

    def setFoldLines(self, lines: list):
        self.foldableLines = lines

    def visibleBlocks(self):

        self.currentlyVisibleBlocks = []

        block: QTextBlock = self.firstVisibleBlock()
        height: int = self.height()
        blockTop: float = self.blockBoundingGeometry(block).translated(
            self.contentOffset()
        ).top()
        blockBottom: float = self.blockBoundingGeometry(block).height() + blockTop

        while block.isValid():

            if not blockBottom <= height:
                break

            if block.isVisible():
                self.currentlyVisibleBlocks.append([blockTop, block])

            block: QTextBlock = block.next()
            blockTop: float = blockBottom
            blockBottom: float = blockTop + self.blockBoundingRect(block).height()

    def getFoldableBlocks(self, block: QTextBlock) -> list:
        rootIndentation: int = len(block.text()) - len(block.text().strip())
        nextBlock: QTextBlock = block.next()
        foldableBlocks: list = []
        lastBlock = None
        while nextBlock.isValid():
            strippedText = nextBlock.text().strip()

            currentBlockIndentation: int = len(nextBlock.text()) - len(strippedText)

            if currentBlockIndentation <= rootIndentation:

                if (
                    len(strippedText) != 0
                ):  # This evaluates to true when we we reach a block that is not in our scope to fold
                    break

            if (
                len(strippedText) != 0
            ):  # Last block with actual code in it, no white space contained
                lastBlock = nextBlock

            foldableBlocks.append(nextBlock)
            nextBlock = nextBlock.next()

        for index, foldableBlock in enumerate(foldableBlocks):

            if foldableBlocks[index] == lastBlock:

                return foldableBlocks[: index + 1]

    def paintEvent(self, e: QPaintEvent):
        self.visibleBlocks()
        super().paintEvent(e)

    def totalLines(self):
        return self.blockCount()

    def is_modified(self):
        return self.document().isModified()

    def iterate(self):
        it = self.document().begin()
        while it != self.document().end():
            it = it.next()
            print(it.text())

    def check(self):

        cursor = self.textCursor()
        block = cursor.block()
        expression = QRegExp("\\w{120,}\\b")
        if len(block.text()) > 120:
            index = 0  # expression.indexIn(block.text())
            layout = block.layout()
            ranges = layout.formats()
            format = QTextCharFormat()
            format.setUnderlineStyle(QTextCharFormat.WaveUnderline)
            format.setUnderlineColor(QColor("#FF0000"))

            # while index >= 0:
            length = len(block.text())  # expression.matchedLength()
            formatrange = QTextLayout.FormatRange()

            formatrange.format = format
            formatrange.length = length
            formatrange.start = index

            ranges.append(formatrange)

            layout.setFormats(ranges)
            self.document().markContentsDirty(block.position(), block.length())
            QToolTip.showText(
                QCursor.pos(), "Line too long: {} > 120".format(len(block.text()))
            )

    def newFile(self):
        """This is a wrapper for the function defined in Main: """

        self.new_action = QAction("New")
        self.new_action.triggered.connect(self.parent.parent.newFile)

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
        # self.check()
        return extraSelections

    def openFile(self):

        self.open_action = QAction("Open")
        self.open_action.triggered.connect(self.parent.parent.openFileFromMenu)

    def runFile(self):

        self.run_action = QAction("Run")
        self.run_action.triggered.connect(self.parent.parent.execute_file)

    def insert(self):
        self.insertAction = QAction("Bubblesort")
        self.insertAction.triggered.connect(self.bubblesort)

    def insertClass(self):
        self.insertClassAction = QAction("Create a class")
        self.insertClassAction.triggered.connect(self.createClass)
    def insertConcentricCircle(self):
        self.insertConcentricCircleAction = QAction("Concentric circle")
        self.insertConcentricCircleAction.triggered.connect(self.concentricCircle)

    def concentricCircle(self):

        self.insertPlainText("""import turtle
turtle.penup()
for i in range(1, 500, 50):
    turtle.right(90)    # Face South
    turtle.forward(i)   # Move one radius
    turtle.right(270)   # Back to start heading
    turtle.pendown()    # Put the pen back down
    turtle.circle(i)    # Draw a circle
    turtle.penup()      # Pen up while we go home
    turtle.home()  
        """)

    def createClass(self):
        self.insertPlainText(
            """class Placeholder:
            
    def __init__(self):
        self.solve()
        
    def solve(self):
        pass"""
        )

    def bubblesort(self):

        self.insertPlainText(
            """def bubbleSort(array: list):
    for i in range(len(array) - 1, 0, -1):
        for j in range(i):
            if array[j] > array[j+1]:
                temp = array[j]
                array[j] = array[j+1]
                array[j+1] = temp"""
        )

    def textUnderCursor(self):
        textCursor = self.textCursor()
        pos: int = textCursor.position()

        textCursor.setPosition(pos - 1)
        textCursor.select(QTextCursor.WordUnderCursor)

        return textCursor.selectedText()

    def moveCursorPosBack(self):
        textCursor = self.textCursor()
        textCursorPos = textCursor.position()

        textCursor.setPosition(textCursorPos - 1)
        self.setTextCursor(textCursor)

    def mouseMoveEvent(self, QMouseEvent):
        # TODO: finish
        cursor: QCursor = QCursor(Qt.IBeamCursor)
        QApplication.setOverrideCursor(cursor)
        QApplication.changeOverrideCursor(cursor)
        super().mouseMoveEvent(QMouseEvent)

    def returnCursorToNormal(self):
        cursor = QCursor(Qt.ArrowCursor)
        QApplication.setOverrideCursor(cursor)
        QApplication.changeOverrideCursor(cursor)

    def getBlockUnderCursor(self, event: QMouseEvent) -> QTextBlock:
        height = self.fontMetrics().height()
        y = event.pos().y()
        for array in self.currentlyVisibleBlocks:
            if array[0] < y < height + array[0]:
                return array[1]
        emptyBlock: QTextBlock = QTextBlock()
        return emptyBlock

    def mousePressEvent(self, e: QMouseEvent):
        super().mousePressEvent(e)
        return
        # self.check()
        if QApplication.queryKeyboardModifiers() == Qt.ControlModifier:

            super().mousePressEvent(e)
            self.text = self.textUnderCursor()
            if self.text is not None:
                word = self.text
                # self.parent.parent.showBrowser(url, word)

                # tag = self.jump_to_def(word)
                # print(tag[0])
                # if tag[0]:
                # print("INFO INFO INFO")
                # print(tag[1])

                # self.parent.jumpToDef(tag[1])

                # if self.check_func(self.textUnderCursor(), True):
                #     extraSelections = self.highlightCurrentLine()
                #     selection = QTextEdit.ExtraSelection()
                #     selection.format.setFontUnderline(True)
                #     selection.format.setUnderlineColor(QColor("#00d2ff"))
                #     selection.format.setForeground(QColor("#00d2ff"))
                #     selection.format.setProperty(QTextFormat.FullWidthSelection, True)
                #     selection.cursor = self.textCursor()
                #     selection.cursor.clearSelection()
                #     selection.cursor.select(QTextCursor.WordUnderCursor)
                #     extraSelections.append(selection)
                #     self.setExtraSelections(extraSelections)
                #     self.text = self.textUnderCursor()
                #
                #     # cursor = QCursor(Qt.PointingHandCursor)
                #
                #     # QApplication.setOverrideCursor(cursor)
                #     # QApplication.changeOverrideCursor(cursor)
                #
                # else:
                #     self.text = None
        else:
            super().mousePressEvent(e)
        QApplication.restoreOverrideCursor()
        # super().mousePressEvent(e)

    def check_func(self, word, clicked=False):
        funcs = [
            "abs",
            "all",
            "any",
            "ascii",
            "bin",
            "bool",
            "breakpoint",
            "bytearray",
            "bytes",
            "callable",
            "chr",
            "classmethod",
            "compile",
            "complex",
            "delattr",
            "dict",
            "dir",
            "divmod",
            "enumerate",
            "eval",
            "exec",
            "filter",
            "float",
            "format",
            "frozenset",
            "getattr",
            "globals",
            "hasattr",
            "hash",
            "help",
            "hex",
            "id",
            "input",
            "int",
            "isinstance",
            "issubclass",
            "iter",
            "len",
            "list",
            "locals",
            "map",
            "max",
            "memoryview",
            "min",
            "next",
            "object",
            "oct",
            "open",
            "ord",
            "pow",
            "print",
            "property",
            "range",
            "repr",
            "reversed",
            "round",
            "set",
            "setattr",
            "slice",
            "sorted",
            "staticmethod",
            "str",
            "sum",
            "super",
            "tuple",
            "type",
            "vars",
            "zip",
            "__import__",
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

    def jump_to_def(self, word):

        # from Hydra.test import getTags
        return False
        # lol = getTags()
        # tag = lol.get(word, None)

        # if tag:
        #  return True, tag

        # else:
        # return False, ""

    def get_pydoc_output(self):
        output = self.info_process.readAllStandardOutput().data().decode()
        self.parent.parent.open_documentation(output, self.info_process.arguments()[0])

    def insertFromMimeData(self, source: QMimeData) -> None:
        print(source)
        self.insertPlainText(source.text())
        print(self.textCursor().blockNumber())

    def contextMenuEvent(self, event):

        menu = QMenu()

        """Initializing actions"""
        self.newFile()
        self.openFile()
        self.runFile()
        self.insert()
        self.insertClass()
        self.insertConcentricCircle()
        menu.addAction(self.new_action)
        menu.addAction(self.open_action)
        menu.addAction(self.run_action)


        insertMenu = menu.addMenu("Insert")
        insertMenu.addAction(self.insertAction)
        insertMenu.addAction(self.insertClassAction)
        insertMenu.addAction(self.insertConcentricCircleAction)
        menu.setFont(self.menuFont)
        insertMenu.setFont(self.menuFont)

        menu.exec(event.globalPos())

        del menu

    def mouseReleaseEvent(self, e):

        # self.check()
        super().mouseReleaseEvent(e)

    def onlySpaces(self, word: str) -> bool:

        for char in word:

            if char != " ":
                return False
        return True

    def keyPressEvent(self, e):

        textCursor = self.textCursor()
        key = e.key()
        if (
            e.modifiers() == Qt.ControlModifier and key == 16777217
        ):  # that key code stands for tab
            self.parent.parent.switchTabs()

        isSearch = e.modifiers() == Qt.ControlModifier and e.key() == Qt.Key_F

        isDeleteLine = (
            e.modifiers() == Qt.ControlModifier and e.key() == 16777219
        )  # This is for MacOS (CMD+Delete)

        if isSearch:
            try:
                currentWidget = self.parent
                currentFile = currentWidget.fileName
                currentEditor = currentWidget.editor

                textCursor = currentEditor.textCursor()
                textCursorPos = textCursor.position()
                if currentWidget is not None:
                    text, okPressed = QInputDialog.getText(self, "Find", "Find what: ")
                    if okPressed:
                        if text == "":
                            text = " "
                            self.not_found = NoMatch(text)

                        self.searchtext = text

                        try:
                            with open(currentFile, "r") as file:
                                contents = file.read()
                                self.indexes = list(find_all(contents, text))
                                if len(self.indexes) == 0:
                                    self.not_found = NoMatch(text)

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

        if (
            e.modifiers() == Qt.ControlModifier and e.key() == 61
        ):  # Press Ctrl+Equal key to make font bigger

            self.font.setPointSize(self.size + 1)
            self.font.setFamily(editor["editorFont"])
            self.setFont(self.font)
            self.size += 1

        if e.modifiers() == Qt.ControlModifier and e.key() == 16777217:
            return

        if (
            e.modifiers() == Qt.ControlModifier and e.key() == 45
        ):  # Press Ctrl+Minus key to make font smaller

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
                textCursor.movePosition(
                    textCursor.Right, textCursor.KeepAnchor, len(self.searchtext)
                )
                currentEditor.setTextCursor(textCursor)
                self.l += 1
            except IndexError:
                self.l = 0

        if key == 16777220:

            currentText: str = self.textCursor().block().text()
            space: str = " "

            if self.textUnderCursor().endswith(":"):
                spaces: int = 0

                for index, i in enumerate(currentText):

                    if i != " ":
                        if index % 4 == 0:

                            super().keyPressEvent(e)
                            self.insertPlainText(space * (index + 4))

                            return

                if spaces == 0:

                    super().keyPressEvent(e)
                    self.insertPlainText(space * 4)
                    return
            else:

                for index, i in enumerate(currentText):

                    if i != " ":

                        if index % 4 == 0 and index != 0:
                            super().keyPressEvent(e)
                            self.insertPlainText(space * index)

                            return
                        break
                    else:

                        if len(currentText) % 4 == 0 and self.onlySpaces(currentText):
                            super().keyPressEvent(e)
                            self.insertPlainText(space * len(currentText))
                            return

        super().keyPressEvent(e)


class Completer(QCompleter):
    insertText = pyqtSignal(str)

    def __init__(self, myKeywords=None, parent=None):
        self.wordList = wordList
        QCompleter.__init__(self, myKeywords, parent)

        self.activated.connect(self.changeCompletion)

    def changeCompletion(self, completion):
        self.insertText.emit(completion)
