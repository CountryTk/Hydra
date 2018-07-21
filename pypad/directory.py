from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QHBoxLayout, QTreeView, QFileSystemModel


from pypad import tabs, window


class DirectoryTree(QTreeView):
    def __init__(self):
        """
        create directory tree
        """
        super().__init__()

        self.layout = QHBoxLayout(self)

        self.model = QFileSystemModel()
        self.setModel(self.model)
        self.model.setRootPath(QDir.rootPath())

        self.setIndentation(10)

        for i in range(1, 4):
            self.hideColumn(i)

        self.doubleClicked.connect(self.double_click)

    def set_root(self, path):
        """
        set the directory the tree should index
        :param path: directory to index
        """
        self.setRootIndex(self.model.index(path))

    def double_click(self, signal):
        """
        open a file when double clicked
        """
        file_path = self.model.filePath(signal)
        tabs.tabs.new_tab(file_path)


directory_tree = DirectoryTree()
