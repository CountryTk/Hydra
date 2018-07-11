from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QGridLayout, QCheckBox


from pypad import config


dialogs = []


class Error(QDialog):

    def __init__(self, *args):
        super().__init__()
        dialogs.append(self)

        layout = QVBoxLayout(self)

        message = ' '.join(args)
        label = QLabel(message)
        layout.addWidget(label)

        button = QPushButton('Quit')
        button.clicked.connect(self.closeEvent)
        layout.addWidget(button)

        self.exec_()  # pause main thread while dialog is open
        self.setWindowTitle("Error")
        self.show()

    def closeEvent(self, event):
        dialogs.remove(self)


class FatalError(Error):

    def closeEvent(self, event):
        QCoreApplication.instance().quit()


class Quit(QDialog):

    def __init__(self):
        super().__init__()

        if not config.config.get('window.quitPrompt'):
            QCoreApplication.instance().quit()

        dialogs.append(self)

        layout = QGridLayout(self)

        label = QLabel("Are you sure you want to quit?")
        layout.addWidget(label, 0, 0, 1, 2)

        self.checkbox = QCheckBox("Always prompt on quit")
        self.checkbox.setChecked(config.config.get('window.quitPrompt'))
        self.checkbox.stateChanged.connect(self.on_click)
        layout.addWidget(self.checkbox, 1, 0, 1, 2)

        yes = QPushButton('Yes')
        yes.clicked.connect(self.quit)
        layout.addWidget(yes, 2, 0)

        no = QPushButton('No')
        no.clicked.connect(self.closeEvent)
        layout.addWidget(no, 2, 1)

        self.exec_()  # pause main thread while dialog is open
        self.setWindowTitle("Quit")
        self.show()

    def on_click(self, int):
        config.config.set('window.quitPrompt', self.checkbox.isChecked())
        config.config.save()

    def closeEvent(self, event):
        dialogs.remove(self)
        self.hide()

    def quit(self):
        QCoreApplication.instance().quit()
