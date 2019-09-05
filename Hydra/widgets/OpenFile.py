from PyQt5.QtCore import pyqtSignal, QThread

import os


class OpenFile(QThread):

    dataSignal = pyqtSignal(str)
    readAmountSignal = pyqtSignal(
        list
    )  # This signal is for when the user hasn't loaded the whole file and saves it. With this, no unloaded content will be lost
    EndOfFileSignal = pyqtSignal(list)
    readDone = pyqtSignal(bool)

    def __init__(self, parent=None):

        super(OpenFile, self).__init__()

        self.file = None
        self.parent = parent
        self.offset = 0
        self.exists = None
        self.amount = 5012
        self.read_amount = 0
        # self.file_name = self.parent.fileName

    def add_args(self, filename, file_exists):

        self.file = filename
        self.exists = file_exists

    def old_open(self):  # Deprecated
        if os.path.isfile(self.file):
            max_size = os.path.getsize(self.file)
        else:
            max_size = 0
        if self.exists:

            try:
                with open(self.file, "rb") as opened_file:
                    opened_file.seek(self.offset)
                    print("Sought to: {}".format(self.offset))
                    data = opened_file.read(self.amount)
                    self.read_amount += len(data)
                    # print(len(data), self.read_amount, type(len(data)), type(self.read_amount))
                    self.dataSignal.emit(data.decode())
                    print(self.read_amount, " - Read amount [in bytes]", len(data))

                    if self.read_amount == max_size:

                        # print("END OF FILE REACHED LMAOAOAOAOAAO")

                        self.EndOfFileSignal.emit([True, max_size])

                    self.readAmountSignal.emit([self.read_amount, max_size])

            except (UnicodeEncodeError, UnicodeDecodeError) as E:
                self.dataSignal.emit(str(E))
                print(E)

        else:
            pass

    def open(self):

        self.readDone.emit(False)
        with open(self.file, "rb") as file:

            data = file.read()

        self.readDone.emit(True)
        self.dataSignal.emit(data.decode())

    def change_offset(self, offset):
        self.offset = offset

    def change_read_amount(self, amount: int) -> None:

        self.amount = amount

    def run(self):
        # self.old_open() lazy load [not working]
        self.open()

    def our_start(self):
        # self.offset += 5012
        self.start()
