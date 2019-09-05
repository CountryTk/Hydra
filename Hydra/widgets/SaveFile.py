from PyQt5.QtCore import QThread, pyqtSignal
import os


class SaveFile(QThread):

    readDone = pyqtSignal(bool)
    data = pyqtSignal(str)
    updateOffset = pyqtSignal(int)

    def __init__(self, parent):

        super(SaveFile, self).__init__()

        self.active_tab = None
        self.parent = parent

    def old_save(self, tab):  # Deprecated
        file_name = tab.fileName

        data_to_write = tab.editor.toPlainText()
        # self.parent.not_ready()

        # if len(tab.editor.toPlainText().encode("utf-8")) > tab.start_from:
        #   print("wtf!!!!")
        #    tab.start_from = len(tab.editor.toPlainText().encode("utf-8"))
        # m = len(tab.editor.toPlainText().encode("utf-8"))
        # print("size of text: {}".format(len(tab.editor.toPlainText().encode("utf-8"))))
        # print("start from: {}".format(tab.start_from))
        # ok = m - tab.start_from
        # print(ok)

        print("ADASSADSA: ", tab.start_from)

        with open(file_name, "rb") as file:

            if tab.start_from != 0:
                file.seek(tab.start_from)
                data = file.read()
            else:
                data = b""

        with open(file_name, "w+") as save_file:
            save_file.write(data_to_write + data.decode())

        # print("#"*10)
        #
        # print(data.decode())
        #
        # print("#"*10)

        self.readDone.emit(True)

        # tab.start_from = len(tab.editor.toPlainText().encode("utf-8"))
        # print(tab.start_from, ": start from")
        # print("append: ", data.decode())
        # print("\n"*10)
        self.updateOffset.emit(tab.start_from)

    def save(self, tab):

        self.readDone.emit(False)
        file_name = tab.fileName
        data = tab.editor.toPlainText()

        with open(file_name, "wb") as file:

            file.write(data.encode())

        self.readDone.emit(True)

    def run(self) -> None:

        # self.old_save(self.active_tab) lazy load [not working]
        self.save(self.active_tab)

    def add_args(self, tab):

        self.active_tab = tab
