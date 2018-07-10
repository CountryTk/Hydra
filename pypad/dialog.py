from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QGridLayout

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
        dialogs.append(self)

        layout = QGridLayout(self)

        label = QLabel("Are you sure you want to quit?")
        layout.addWidget(label, 0, 0, 1, 2)

        yes = QPushButton('Yes')
        yes.clicked.connect(self.quit)
        layout.addWidget(yes, 1, 0)

        no = QPushButton('No')
        no.clicked.connect(self.closeEvent)
        layout.addWidget(no, 1, 1)

        self.setWindowTitle("Quit")
        self.show()

    def closeEvent(self, event):
        dialogs.remove(self)

    def quit(self):
        QCoreApplication.instance().quit()
