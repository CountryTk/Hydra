import sys
import json
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QColor, QPainter, QPalette
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QAction, \
    QVBoxLayout, QTabWidget, QFileDialog, QPlainTextEdit, QHBoxLayout


lineBarColor = QColor(53, 53, 53)
lineHighlightColor = QColor('#00FF04')


class NumberBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.editor = parent
        layout = QVBoxLayout(self)
        self.editor.blockCountChanged.connect(self.update_width)
        self.editor.updateRequest.connect(self.update_on_scroll)
        self.update_width('1')

    def mousePressEvent(self, QMouseEvent):
        print("class NumberBar(QWidget):mousePressEvent")

    def update_on_scroll(self, rect, scroll):
        if self.isVisible():
            if scroll:
                self.scroll(0, scroll)
            else:
                self.update()

    def update_width(self, string):
        width = self.fontMetrics().width(str(string)) + 10
        print("update_width:width:" + str(width))
        if self.width() != width:
            self.setFixedWidth(width)

    def paintEvent(self, event):
        if self.isVisible():
            block = self.editor.firstVisibleBlock()
            height = self.fontMetrics().height()
            number = block.blockNumber()
            painter = QPainter(self)
            painter.fillRect(event.rect(), lineBarColor)
            painter.drawRect(0, 0, event.rect().width() - 1, event.rect().height() - 1)
            font = painter.font()

            current_block = self.editor.textCursor().block().blockNumber() + 1

            while block.isValid():
                block_geometry = self.editor.blockBoundingGeometry(block)
                offset = self.editor.contentOffset()
                block_top = block_geometry.translated(offset).top()
                number += 1

                rect = QRect(0, block_top, self.width() - 5, height)

                if number == current_block:
                    font.setBold(True)
                else:
                    font.setBold(False)

                painter.setFont(font)
                painter.drawText(rect, Qt.AlignRight, '%i' % number)

                if block_top > event.rect().bottom():
                    break

                block = block.next()

            painter.end()


class Content(QWidget):
    def __init__(self, text, fileName):
        super(QWidget, self).__init__()
        self.editor = QPlainTextEdit()
        self.text = text
        self.fileName = fileName
        self.editor.setPlainText(text)
        # Create a layout for the line numbers

        self.hbox = QHBoxLayout(self)
        self.numbers = NumberBar(self.editor)
        self.hbox.addWidget(self.numbers)
        self.hbox.addWidget(self.editor)


class Tabs(QWidget):

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tabs.resize(300, 200)


        # Add tabs
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.closeTab)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def closeTab(self, index):
        tab = self.tabs.widget(index)
        tab.deleteLater()
        self.tabs.removeTab(index)


class Main(QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        # Initializing the main widget where text is displayed
        self.tab = Tabs()
        self.tabsOpen = []

        # initializing the functions to handle certain tasks
        self.new()
        self.open()
        self.save()
        self.saveAs()

        # Without this, the whole layout is broken
        self.setCentralWidget(self.tab)
        self.newFileCount = 0  # Tracking how many new files are opened
        self.files = None  # Tracking the current file that is open
        self.initUI()  # Main UI
        self.show()

    def initUI(self):
        self.statusBar()  # Initializing the status bar

        # Creating the menu bar

        menu = self.menuBar()

        # Creating the file menu

        fileMenu = menu.addMenu('File')

        # Adding options to the file menu

        fileMenu.addAction(self.newAct)
        fileMenu.addAction(self.openAct)
        fileMenu.addAction(self.saveAct)
        fileMenu.addAction(self.saveAsAct)

        self.resize(800, 600)

    def closeTab(self, index):
        tab = self.tabs.widget(index)
        tab.deleteLater()
        self.tab.removeTab(index)

    def buttonClicked(self):
        self.tab.addTab(Content("smalltext2"), "sadsad")

    def open(self):
        self.openAct = QAction('Open...', self)
        self.openAct.setShortcut('Ctrl+O')
        self.openAct.setStatusTip('Open a file')
        self.is_opened = False
        self.openAct.triggered.connect(self.openFile)

    def openFile(self):
        options = QFileDialog.Options()
        filenames, _ = QFileDialog.getOpenFileNames(
            self, 'Open a file', '',
            'All Files (*);;Python Files (*.py);;Text Files (*.txt)',
            options=options
        )
        tab_idx = len(self.tabsOpen)
        if filenames:  # If file is selected, we can open it
            for filename in filenames:
                with open(filename, 'r+') as file_o:
                    text = file_o.read()
                    self.is_opened = True
                    tab = Content(text, filename)  # Creating a tab object *IMPORTANT*
                    self.files = filename
                    self.tab.tabs.addTab(tab, tab.fileName)
                    self.tabsOpen.append(self.files)


    def new(self):
        self.newAct = QAction('New')
        self.newAct.setShortcut('Ctrl+N')
        self.newAct.setStatusTip('Create a new file')
        self.newAct.triggered.connect(self.newFile)

    def newFile(self):
        text = ""
        fileName = "Untitled.txt"
        self.is_opened = False
        # Creates a new blank file
        file = Content(text, fileName)
        self.tab.tabs.addTab(file, file.fileName)

    def save(self):
        self.saveAct = QAction('Save')
        self.saveAct.setShortcut('Ctrl+S')
        self.saveAct.setStatusTip('Save a file')
        self.saveAct.triggered.connect(self.saveFile)

    def saveFile(self):
        try:
            active_tab = self.tab.tabs.currentWidget()
            print(active_tab.fileName)
            if self.is_opened:  # If a file is already opened
                with open(active_tab.fileName, 'w+') as saveFile:
                    self.saved = True
                    print(self.tabsOpen)
                    saveFile.write(active_tab.editor.toPlainText())
                    print(active_tab.editor.toPlainText())
                    saveFile.close()
            else:
                options = QFileDialog.Options()
                name = QFileDialog.getSaveFileName(self, 'Save File', '',
                                                   'All Files (*);;Python Files (*.py);;Text Files (*.txt)',
                                                   options=options)
                fileName = name[0]
                with open(fileName, "w+") as saveFile:
                    self.saved = True
                    self.is_opened = True
                    self.tabsOpen.append(fileName)
                    saveFile.write(active_tab.editor.toPlainText())

                    saveFile.close()
        except AttributeError:
            print("No files open")

    def saveAs(self):
        self.saveAsAct = QAction('Save As...')
        self.saveAsAct.setShortcut('Ctrl+Shift+S')
        self.saveAsAct.setStatusTip('Save a file as')
        self.saveAsAct.triggered.connect(self.saveFileAs)

    def saveFileAs(self):
        try:
            active_tab = self.tab.tabs.currentWidget()
            if active_tab is not None:
                active_index = self.tab.tabs.currentIndex()

                options = QFileDialog.Options()
                name = QFileDialog.getSaveFileName(self, 'Save File', '',
                                                   'All Files (*);;Python Files (*.py);;Text Files (*.txt)',
                                                   options=options)
                fileName = name[0]
                with open(fileName, "w+") as saveFile:
                    self.saved = True
                    self.tabsOpen.append(fileName)
                    saveFile.write(active_tab.editor.toPlainText())
                    text = active_tab.editor.toPlainText()
                    newTab = Content(str(text), fileName)
                    self.tab.tabs.removeTab(active_index)  # When user changes the tab name we make sure we delete the old one
                    self.tab.tabs.addTab(newTab, newTab.fileName)  # And add the new one!
                    saveFile.close()
            else:
                print("No file opened")
        except FileNotFoundError:
            print("No file found")


if __name__ == '__main__':
    with open("../config.json", "r") as jsonFile:
        read = jsonFile.read()
        data = json.loads(read)
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(data["editor"][0]["windowColor"]))
        palette.setColor(QPalette.WindowText, QColor(data["editor"][0]["windowText"]))
        palette.setColor(QPalette.Base, QColor(data["editor"][0]["editorColor"]))
        palette.setColor(QPalette.AlternateBase, QColor(data["editor"][0]["alternateBase"]))
        palette.setColor(QPalette.ToolTipBase, QColor(data["editor"][0]["ToolTipBase"]))
        palette.setColor(QPalette.ToolTipText, QColor(data["editor"][0]["ToolTipText"]))
        palette.setColor(QPalette.Text, QColor(data["editor"][0]["editorText"]))
        palette.setColor(QPalette.Button, QColor(data["editor"][0]["buttonColor"]))
        palette.setColor(QPalette.ButtonText, QColor(data["editor"][0]["buttonTextColor"]))
        palette.setColor(QPalette.Highlight, QColor(data["editor"][0]["HighlightColor"]).lighter())
        palette.setColor(QPalette.HighlightedText, QColor(data["editor"][0]["HighlightedTextColor"]))
        app.setPalette(palette)

        ex = Main()
        sys.exit(app.exec_())
