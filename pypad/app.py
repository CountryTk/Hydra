#!/usr/bin/env python

import sys

from PyQt5.QtWidgets import QApplication


def main():
    """
    main function for starting PyPad
    """
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setCursorFlashTime(0)

    from pypad import palette, window

    app.setPalette(palette.Palette())

    window.main_window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
