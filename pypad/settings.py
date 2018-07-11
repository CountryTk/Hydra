from PyQt5.QtWidgets import QDialog, QPushButton, QGridLayout, QTableWidget, QTableWidgetItem, QHeaderView


from pypad import config


dialogs = []


class Settings(QDialog):

    def __init__(self):
        super().__init__()
        dialogs.append(self)

        layout = QGridLayout(self)

        self.table = QTableWidget()
        self.table.setRowCount(len(config.config.flat()))
        self.table.setColumnCount(2)

        count = 0
        for key, value in config.config.flat().items():
            name = QTableWidgetItem(key)
            setting = QTableWidgetItem(value)
            self.table.setItem(count, 0, name)
            self.table.setItem(count, 1, setting)
            count += 1

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)

        layout.addWidget(self.table, 0, 0, 1, 4)

        save = QPushButton('Save')
        save.clicked.connect(config.config.save)
        layout.addWidget(save, 1, 1)

        cancel = QPushButton('Cancel')
        cancel.clicked.connect(self.closeEvent)
        layout.addWidget(cancel, 1, 2)

        close = QPushButton('Close')
        close.clicked.connect(self.quit)
        layout.addWidget(close, 1, 3)

        self.setWindowTitle("Settings")
        self.resize(600, 700)
        self.show()

    def closeEvent(self, event):
        dialogs.remove(self)
        self.hide()

    def quit(self):
        config.config.save()
        dialogs.remove(self)
        self.close()
