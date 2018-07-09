from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout

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