import sys
import os
import json

from PySide import QtGui, QtCore

from pyflow.view import FlowScene
from pyflow.model import FlowModel
from save_load import *
from output_pref import *


# code borrowed from: http://www.dreamincode.net/forums/topic/261282-a-basic-pyqt-tutorial-notepad/

class mrs_gui(QtGui.QMainWindow):
    def __init__(self):
        super(mrs_gui, self).__init__()
        self.filename = ""
        self.statusbar = QtGui.QMainWindow.statusBar(self)
        self.initUI()

    def initUI(self):
        # create new file action
        newAction = QtGui.QAction('New', self)
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('Create new file')
        newAction.triggered.connect(self.newFile)

        # create save file action
        saveAction = QtGui.QAction('Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save current file')
        saveAction.triggered.connect(self.saveFile)

        # create save as file action
        saveAsAction = QtGui.QAction('Save As...', self)
        saveAsAction.setShortcut('Ctrl+Shift+S')
        saveAsAction.setStatusTip('Save current file as new file')
        saveAsAction.triggered.connect(self.saveAsFile)

        # create open file action
        openAction = QtGui.QAction('Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open a file')
        openAction.triggered.connect(self.openFile)

        # create close file action
        closeAction = QtGui.QAction('Close', self)
        closeAction.setShortcut('Ctrl+Q')
        closeAction.setStatusTip('Close Notepad')
        closeAction.triggered.connect(self.close)

        # create menu bar
        menubar = self.menuBar()

        # create File menu, add actions
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addSeparator()
        fileMenu.addAction(saveAction)
        fileMenu.addAction(saveAsAction)
        fileMenu.addSeparator()
        fileMenu.addAction(closeAction)

        # create window
        self.resize(400, 400)
        self.setWindowTitle("New - MRS GUI tool v0.1")

        model = FlowModel()
        flow_scene = FlowScene()
        flow_view = QtGui.QGraphicsView()
        flow_view.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        flow_view.setScene(flow_scene)
        flow_view.setBackgroundBrush(QtCore.Qt.black)

        self.setCentralWidget(flow_view)

        # create model
        model.add_item()

        flow_scene.set_model(model)

        model.add_item()
        model.set_data(0, "name", "Hello")
        model.set_data(0, "position", QtCore.QPoint(500, 50))

        model.add_item()
        model.set_data(1, "name", "World")
        model.set_data(1, "position", QtCore.QPoint(500, 100))

        model.set_data(2, "name", "TWIX_EXAMPLE")
        model.set_data(2, "position", QtCore.QPoint(500, 150))

        aux_widget = QtGui.QWidget()
        aux_widget.setFixedSize(170, 60)
        button = QtGui.QPushButton("Edit")
        button.clicked.connect(self.edit_output_settings)
        button.setParent(aux_widget)

        model.set_data(2, "auxilliary", aux_widget)







        flow_view.fitInView(flow_scene.sceneRect(), QtCore.Qt.KeepAspectRatio)

        self.show()

    def newFile(self):
        self.centralWidget().scene().set_model(FlowModel())

    def saveFile(self):
        if self.filename:
            save_model(self.centralWidget().scene().model, self.filename)
            self.statusbar.showMessage("Saved")
            #save_model(self.__model, self.filename)
        else:
            self.saveAsFile()

    def saveAsFile(self):
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File', os.getenv('HOME'))
        save_model(self.centralWidget().scene().model, filename)
        self.filename = filename[0]
        self.setWindowTitle(str(self.filename) + " - MRS GUI tool v0.1")
        self.statusbar.showMessage("Saved")

    def openFile(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'))
        if filename[0]:
            self.centralWidget().scene().set_model(open_model(filename))
            self.filename = filename[0]

        self.setWindowTitle(str(self.filename) + " - MRS GUI tool v0.1")

    def edit_output_settings(self):
        run_settings()

        """settings_index = self.centralWidget().scene().model.add_item()
        aux_widget = QtGui.QWidget()
        aux_widget.setFixedSize(170, 60)
        button = QtGui.QPushButton("OK")
        button.clicked.connect(self.close)
        button.setParent(aux_widget)

        button1 = QtGui.QPushButton("Cancel")
        button1.clicked.connect(self.close)
        button1.setParent(aux_widget)

        button2 = QtGui.QPushButton("1234")
        button2.clicked.connect(self.close)
        button2.setParent(aux_widget)

        self.centralWidget().scene().model.set_data(settings_index, "auxilliary", aux_widget)"""
def main():
    app = QtGui.QApplication(sys.argv)
    mrs = mrs_gui()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
