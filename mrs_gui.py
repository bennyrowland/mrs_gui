__author__ = 'ben'

from PySide import QtGui
import sys

if __name__ == "__main__":
    my_app = QtGui.QApplication(sys.argv)

    main_window = QtGui.QMainWindow()

    main_window.show()
    sys.exit(my_app.exec_())