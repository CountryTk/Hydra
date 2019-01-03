from utils.config import config_reader
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QDesktopWidget, QLabel, \
    QVBoxLayout, QComboBox
from PyQt5.QtGui import QFont, QIcon, QPixmap, QPalette, QColor
from PyQt5.QtCore import Qt
from widgets.Messagebox import MessageBox
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


class Customize(QWidget):
    def __init__(self, app=None, palette=None):
        super().__init__()
        self.app = app
        self.palette = palette
        self.setFixedSize(800, 600)
        with open("default.json", "r") as selectedIndex:
            self.index = selectedIndex.read()
            if self.index == "":
                self.index = 0

            selectedIndex.close()
        self.conf = MessageBox()
        self.opened = False
        self.vbox = QVBoxLayout(self)  # Creating the layout

        self.setWindowIcon(QIcon('resources/Python-logo-notext.svg_.png'))

        self.initUI()

    def initUI(self):

        self.LayoutImage = QLabel(self)
        self.LayoutText = QLabel(self)

        self.hbox = QHBoxLayout()

        editor = config0['editor']

        self.font = QFont()
        self.font.setFamily(editor["editorFont"])
        self.font.setPointSize(editor["editorFontSize"])

        self.combo = QComboBox(self)
        self.combo.addItem("Theme 1")
        self.combo.addItem("Theme 2")
        self.combo.addItem("Theme 3")
        self.combo.currentIndexChanged.connect(self.themes)
        self.combo.setFont(self.font)

        self.theme1 = QPixmap('resources/layout1.png')  # These are the pictures of themes
        self.theme2 = QPixmap('resources/layout1.png')
        self.theme3 = QPixmap('resources/layout1.png')

        self.vbox.addWidget(self.combo)  # Adding Combobox to vertical boxlayout so it would look better

        self.LayoutText.setFont(self.font)

        self.hbox.addWidget(self.LayoutText)
        self.hbox.addWidget(self.LayoutImage)

        self.LayoutImage.setPixmap(self.theme1)  # This is the "main" theme
        self.LayoutImage.resize(415, 287)

        self.LayoutText.setText("Dark theme")

        self.vbox.addLayout(self.hbox)

        self.selector = QPushButton(self)
        self.selector.setFixedSize(100, 30)
        self.selector.setLayoutDirection(Qt.RightToLeft)
        self.selector.setText("Select")
        self.selector.setFont(self.font)

        self.vbox.addWidget(self.selector)
        self.setLayout(self.vbox)

    def run(self):
        self.show()

    def themes(self, index):

        if index == 0:
            self.LayoutImage.setPixmap(self.theme1)
            self.LayoutText.setText("Dark theme")

        elif index == 1:

            self.LayoutImage.setPixmap(self.theme3)
            self.LayoutText.setText("Fancy theme")

        elif index == 2:

            self.LayoutImage.setPixmap(self.theme2)
            self.LayoutText.setText("Light theme")

        else:
            pass

    def test(self):
        index = self.combo.currentIndex()
        self.index = str(index)
        self.conf.confirmation(index+1)
        with open("default.json", "w+") as write:
            write.write(str(self.index))
            write.close()
        if index == 0 and self.app is not None and self.palette is not None:
            editor = config0['editor']
            self.palette.setColor(QPalette.Window, QColor(editor["windowColor"]))
            self.palette.setColor(QPalette.WindowText, QColor(editor["windowText"]))
            self.palette.setColor(QPalette.Base, QColor(editor["editorColor"]))
            self.palette.setColor(QPalette.AlternateBase, QColor(editor["alternateBase"]))
            self.palette.setColor(QPalette.ToolTipBase, QColor(editor["ToolTipBase"]))
            self.palette.setColor(QPalette.ToolTipText, QColor(editor["ToolTipText"]))
            self.palette.setColor(QPalette.Text, QColor(editor["editorText"]))
            self.palette.setColor(QPalette.Button, QColor(editor["buttonColor"]))
            self.palette.setColor(QPalette.ButtonText, QColor(editor["buttonTextColor"]))
            self.palette.setColor(QPalette.Highlight, QColor(editor["HighlightColor"]).lighter())
            self.palette.setColor(QPalette.HighlightedText, QColor(editor["HighlightedTextColor"]))

        elif index == 1 and self.app is not None and self.palette is not None:
            editor = config1['editor']
            self.palette.setColor(QPalette.Window, QColor(editor["windowColor"]))
            self.palette.setColor(QPalette.WindowText, QColor(editor["windowText"]))
            self.palette.setColor(QPalette.Base, QColor(editor["editorColor"]))
            self.palette.setColor(QPalette.AlternateBase, QColor(editor["alternateBase"]))
            self.palette.setColor(QPalette.ToolTipBase, QColor(editor["ToolTipBase"]))
            self.palette.setColor(QPalette.ToolTipText, QColor(editor["ToolTipText"]))
            self.palette.setColor(QPalette.Text, QColor(editor["editorText"]))
            self.palette.setColor(QPalette.Button, QColor(editor["buttonColor"]))
            self.palette.setColor(QPalette.ButtonText, QColor(editor["buttonTextColor"]))
            self.palette.setColor(QPalette.Highlight, QColor(editor["HighlightColor"]).lighter())
            self.palette.setColor(QPalette.HighlightedText, QColor(editor["HighlightedTextColor"]))

        elif index == 2 and self.app is not None or self.palette is not None:
            editor = config2['editor']
            self.palette.setColor(QPalette.Window, QColor(editor["windowColor"]))
            self.palette.setColor(QPalette.WindowText, QColor(editor["windowText"]))
            self.palette.setColor(QPalette.Base, QColor(editor["editorColor"]))
            self.palette.setColor(QPalette.AlternateBase, QColor(editor["alternateBase"]))
            self.palette.setColor(QPalette.ToolTipBase, QColor(editor["ToolTipBase"]))
            self.palette.setColor(QPalette.ToolTipText, QColor(editor["ToolTipText"]))
            self.palette.setColor(QPalette.Text, QColor(editor["editorText"]))
            self.palette.setColor(QPalette.Button, QColor(editor["buttonColor"]))
            self.palette.setColor(QPalette.ButtonText, QColor(editor["buttonTextColor"]))
            self.palette.setColor(QPalette.Highlight, QColor(editor["HighlightColor"]).lighter())
            self.palette.setColor(QPalette.HighlightedText, QColor(editor["HighlightedTextColor"]))

        self.app.setPalette(self.palette)
