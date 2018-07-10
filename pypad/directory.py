from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QHBoxLayout, QTreeView, QFileSystemModel


from pypad import tabs, window


class DirectoryTree(QTreeView):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout(self)

        self.model = QFileSystemModel()
        self.setModel(self.model)
        self.model.setRootPath(QDir.rootPath())

        self.setIndentation(10)
        self.setFixedWidth(200)

        for i in range(1, 4):
            self.hideColumn(i)

        self.doubleClicked.connect(self.double_click)

    def set_root(self, path):
        self.setRootIndex(self.model.index(path))

    def double_click(self, signal):
        file_path = self.model.filePath(signal)
        tabs.tabs.new_tab(file_path)


directory_tree = DirectoryTree()
