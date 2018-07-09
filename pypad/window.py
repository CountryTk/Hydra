from PyQt5.QtWidgets import QWidget, QMainWindow, QHBoxLayout


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout(self)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.main_widget = MainWidget()
        self.setCentralWidget(self.main_widget)


main_window = MainWindow()
