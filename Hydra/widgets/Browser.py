from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel

try:
    from PyQt5.QtWebEngineWidgets import QWebEngineView

    class Browser(QWebEngineView):
        def __init__(self, url):
            super().__init__()
            self.url = QUrl(url)

            self.load(QUrl(url))
            self.show()


except ModuleNotFoundError:

    class Browser(QWidget):
        def __init__(self, url):
            super().__init__()

            self.layout = QHBoxLayout()
            self.editor = QLabel()

            self.layout.addWidget(self.editor)
            self.editor.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
            self.editor.setText(
                """
                <h2> Sorry, support for Windows systems will come soon! </h2>
                <h2> Here are some links related to the issue:
            <a href=\"https://github.com/pyqt/python-qt5/issues/21\">https://github.com/pyqt/python-qt5/issues/21</a>
            </h2>
            """
            )
            self.editor.setTextFormat(Qt.RichText)
            self.editor.setTextInteractionFlags(Qt.TextBrowserInteraction)
            self.editor.setOpenExternalLinks(True)
            self.setLayout(self.layout)
            self.show()
