import sys
import os
import json

from PySide import QtGui, QtCore

from pyflow.view import FlowScene
from pyflow.model import FlowModel
from save_load import *


# code borrowed from: http://www.dreamincode.net/forums/topic/261282-a-basic-pyqt-tutorial-notepad/

class mrs_gui(QtGui.QMainWindow):
    def __init__(self):
        super(mrs_gui, self).__init__()
        self.__model = FlowModel()
        self.initUI()

    def initUI(self):
        newAction = QtGui.QAction('New', self)
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('Create new file')
        newAction.triggered.connect(self.newFile)

        saveAction = QtGui.QAction('Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save current file')
        saveAction.triggered.connect(self.saveFile)

        openAction = QtGui.QAction('Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open a file')
        openAction.triggered.connect(self.openFile)

        closeAction = QtGui.QAction('Close', self)
        closeAction.setShortcut('Ctrl+Q')
        closeAction.setStatusTip('Close Notepad')
        closeAction.triggered.connect(self.close)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(closeAction)

        self.resize(400, 400)
        self.setWindowTitle("MRS GUI tool v0.1")

        flow_scene = FlowScene()
        flow_view = QtGui.QGraphicsView()
        flow_view.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        flow_view.setScene(flow_scene)
        flow_view.setBackgroundBrush(QtCore.Qt.black)

        self.setCentralWidget(flow_view)

        self.__model.add_item()

        flow_scene.set_model(self.__model)

        self.__model.add_item()
        self.__model.set_data(0, "name", "Hello")
        self.__model.set_data(0, "position", QtCore.QPoint(500, 50))

        self.__model.add_item()
        self.__model.set_data(1, "name", "World")
        self.__model.set_data(1, "position", QtCore.QPoint(500, 100))

        self.__model.add_item()
        self.__model.set_data(2, "name", "!!!!!")
        self.__model.set_data(2, "position", QtCore.QPoint(500, 150))

        flow_view.fitInView(flow_scene.sceneRect(), QtCore.Qt.KeepAspectRatio)
        self.show()

    def newFile(self):
        self.text.clear()

    def saveFile(self):
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File', os.getenv('HOME'))
        save_model(self.__model, filename)


    def openFile(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'))
        self.__model = open_model(self.__model, filename)

def main():
    app = QtGui.QApplication(sys.argv)
    mrs = mrs_gui()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
