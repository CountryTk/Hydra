from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QTabWidget, QSplitter, QShortcut, QStatusBar, QVBoxLayout
from PyQt5.QtGui import QFont, QKeySequence
from PyQt5.QtCore import Qt, pyqtSlot
from widgets.Messagebox import MessageBox
from widgets.Console import Console
from widgets.Terminal import Terminal
from widgets.Directory import Directory
from utils.config import config_reader
from widgets.Events import Events

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


class Tabs(QWidget):

    def __init__(self, callback, app, palette, parent=None):
        super().__init__()
        self.app = app
        self.parent = parent
        self.palette = palette
        self.terminal = Terminal(self, False)
        self.tool_layout = QVBoxLayout()
        self.tool_layout_bar = QHBoxLayout()
        self.layout = QVBoxLayout(self)
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.events = Events()
        self.tabs.setStyleSheet("""
           QTabWidget::pane { /* The tab widget frame */
                border-top: 0.5px solid #2c2c2c;
            }
            
            QTabWidget::tab-bar {
                
            }
            
            /* Style the tab using the tab sub-control. Note that
                it reads QTabBar _not_ QTabWidget */
            QTabBar::tab {
                background: #212121;
                border-bottom: 2px solid #303030;
                border-bottom-color: #434343;
                min-width: 8ex;
                margin-left: 10px;
                padding-left: 25px;
                padding-right: 20px;
                padding-top: 3px;
                padding-bottom: 3px;
            }
            
            QTabBar::tab:selected, QTabBar::tab:hover {
                background: #212121;
            }
            QToolTip {
                padding: 3px;
                font-family: \"Iosevka\";
                font-size: 14px; 
                color: #FFFFFF;
                background: #2c2c2c;
                
            }
            QTabBar::tab:selected {
                border-bottom-color: #FFFFFF; /* same as pane color */
            }
            """)
        font = QFont(editor['tabFont'])
        font.setPointSize(editor["tabFontSize"])  # This is the tab font and font size
        self.tabs.setFont(font)
        self.status = QStatusBar(self)
        self.dialog = MessageBox(self)
        self.tabs.usesScrollButtons()
        self.filelist = []

        self.tabSaved = False

        self.Console = Console(self)  # This is the terminal widget and the SECOND thread
        self.directory = Directory(callback, self.app, self.palette)  # TODO: This is top left
        self.directory.clearSelection()
        self.tabCounter = []
        # Add tabs
        self.tab_layout = QHBoxLayout()  # Create new layout for original tab layout
        self.tab_layout.addWidget(self.tabs)  # Add tab widget to tab layout
        self.search_layout = QHBoxLayout()

        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(editor['tabMovable'])  # Let's you make the tabs movable

        if editor['tabShape'] is True:  # If tab shape is true then they have this rounded look
            self.tabs.setTabShape(1)

        else:
            self.tabs.setTabShape(0)  # If false, it has this boxy look

        self.tabs.tabCloseRequested.connect(self.closeTab)

        # Build Layout
        self.layout.addLayout(self.tab_layout)  # Adds 'TOP' layout : tab + directory
        self.layout.addLayout(self.search_layout)

        # Creating horizontal splitter
        self.splitterH = QSplitter(Qt.Horizontal)

        # Creating vertical splitter
        self.splitterV = QSplitter(Qt.Vertical)

        self.splitterV2 = QSplitter(Qt.Vertical)

        self.splitterV.addWidget(self.splitterH)
        self.layout.addWidget(self.splitterV)
        self.splitterV.setSizes([400, 10])
        self.setLayout(self.layout)  # Sets layout of QWidget

        self.closeShortcut = QShortcut(QKeySequence(editor["closeTabShortcut"]), self)
        self.closeShortcut.activated.connect(self.closeTabShortcut)

        self.getAllOpenTabs = QShortcut(QKeySequence("Ctrl+Shift+W"), self)
        self.getAllOpenTabs.activated.connect(self.getAllOpenTabsFunc)

        currentTab = self.tabs.currentWidget()
        self.layout.addLayout(self.tool_layout)
        self.layout.addWidget(self.splitterV)
        self.hideDirectory()

    @pyqtSlot()
    def closeTabShortcut(self):
        self.index = self.tabs.currentIndex()
        self.closeTab(self.index)

    def getAllOpenTabsFunc(self):
        word = 'import'
        for tab in range(self.tabs.count()):
            file = self.tabs.widget(tab).fileName
            if file not in self.filelist:
                self.filelist.append(file)

        for file in self.filelist:
            openedFileContents = open(file, 'r').read()

    def closeTab(self, index):
        try:

            tab = self.tabs.widget(index)

            if tab.saved is True and tab.modified is False:
                tab.deleteLater()
                self.tabCounter.pop(index)
                self.filelist.pop(index)
                self.tabs.removeTab(index)

            elif tab.modified is True:
                self.dialog.saveMaybe(tab, self.tabCounter, self.tabs, index)

        except (AttributeError, IndexError) as E:
            try:
                tab.deleteLater()
                self.tabCounter.pop(index)
                self.filelist.pop(index)
                self.tabs.removeTab(index)
            except (AttributeError, IndexError) as E:
                print(E, " on line 175 in the file Tabs.py")

    def showDirectory(self):
        self.directory.setVisible(True)
        self.tab_layout.removeWidget(self.tabs)
        self.splitterV2.addWidget(self.directory)
        self.splitterV2.addWidget(self.events)
        self.splitterH.addWidget(self.splitterV2)
        self.splitterH.addWidget(self.tabs)  # Adding tabs, now the directory tree will be on the left

    def hideDirectory(self):
        self.tab_layout.removeWidget(self.directory)
        self.directory.setVisible(False)

    """
    Because the root layouts are set all you have to do now is just add/remove widgets from the parent layout associated
    This keeps the UI order set as intended as built above when initialized.
    """

    def hideConsole(self):
        self.splitterV.setSizes([0, 0])

    def showConsole(self):
        self.splitterV.addWidget(self.terminal)
        self.splitterV.setSizes([400, 10])
        self.terminal.clicked = False

    def hideFileExecuter(self):
        self.splitterV.setSizes([0, 0])

    def showFileExecuter(self):
        self.splitterV.addWidget(self.Console)
        self.splitterV.setSizes([400, 10])
        self.Console.clicked = False

    def currentTab(self):
        return self.tabs.currentWidget()
