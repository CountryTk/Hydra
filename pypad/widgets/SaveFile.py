from PyQt5.QtCore import QThread, pyqtSignal


class SaveFile(QThread):

    readDone = pyqtSignal(bool)
    data = pyqtSignal(str)

    def __init__(self, parent):
        
        super(SaveFile, self).__init__()

        self.active_tab = None
        self.parent = parent

    def save(self, tab):
        file_name = tab.fileName
        data_to_write = tab.editor.toPlainText()
        self.parent.not_ready()
        for i in range(12030):
            print(i)
        # with open(file_name, "w+") as file:

            # file.write(data_to_write)

        self.readDone.emit(True)
        
    def run(self) -> None:
        self.save(self.active_tab)

    def add_args(self, tab):

        self.active_tab = tab