__author__ = 'ben'

from PySide import QtGui, QtCore

from pyflow.model import FlowModel
from pyflow.view.scene import FlowScene

import pyflow


class SampleProxy(QtGui.QAbstractProxyModel):
    def __init__(self, index):
        QtGui.QAbstractProxyModel.__init__(self)
        self.parent_index = index
        self.setSourceModel(self.parent_index.model())

    def index(self, row, column, parent):
        #print "index called"
        return self.createIndex(row, column, QtCore.QModelIndex())

    def parent(self, index):
        return QtCore.QModelIndex()

    def rowCount(self, parent):
        #print "rowCount called"
        print parent
        if parent.isValid():
            return 0
        #print "returning %d" % self.sourceModel().rowCount(self.parent_index)
        return self.sourceModel().rowCount(self.parent_index)

    def columnCount(self, parent):
        #print "columnCount called"
        if parent.isValid():
            return 0
        return 2

    def hasChildren(self, parent):
        #print "hasChildren called"
        if parent.isValid():
            # we want to display a flat list so no item has children
            return False
        # null parent refers to the entire list so return True if the source
        # list has entries in it
        return self.sourceModel.rowCount(self.parent_index) > 0

    def mapToSource(self, proxy_index):
        #print "mapToSource called %s" % proxy_index
        return self.sourceModel().index(proxy_index.row(), proxy_index.column(), self.parent_index)

    def mapFromSource(self, source_index):
        #print "mapFromSource called %s" % source_index
        if source_index.parent() == self.parent_index:
            return self.createIndex(source_index.row(), source_index.column(), QtCore.QModelIndex)
        else:
            return QtCore.QModelIndex()

import sys
if __name__ == "__main__":
    pyflow.set_colour_for_type(1, QtCore.Qt.magenta)
    my_app = QtGui.QApplication(sys.argv)

    main_window = QtGui.QMainWindow()

    main_window.resize(400, 400)
    main_window.setWindowTitle("MRS GUI tool v0.1")

    # create a standard QTreeView to display the model
    tree_view = QtGui.QTreeView()

    # create an empty model
    model = FlowModel()
    flow_scene = FlowScene()
    flow_scene.set_model(model)
    # rows with a blank index are top level items (Steps)
    model.insertRow(0, QtCore.QModelIndex())
    # get the index of the newly created step
    step_index = model.index(0, 0)
    # set some data about that step
    # model.index with just a row and a column, no parent gets
    # the step at row and the data for that step in the column
    # name is the 0th column, position is the 1st
    model.setData(model.index(0, 0), "TWIX")
    model.setData(model.index(0, 1), QtCore.QPointF(100.0, 50.0))
    # steps have two child rows, outputs and inputs
    # calling model.index() with the step as a parent allows us
    # to access the steps children. row one means the inputs, column
    # is ignored in this case
    input_list_index = model.index(1, 0, step_index)
    # add an input to the list by inserting a row
    model.insertRow(0, input_list_index)
    # get the reference to that input
    input_index = model.index(0, 0, input_list_index)
    # set the information for that input
    model.setData(input_index, "Example Very Long Input")
    model.setData(model.index(0, 1, input_list_index), 1)
    first_step_outputs = model.index(0, 0, step_index)
    model.insertRow(0, first_step_outputs)
    # now insert a second new step
    model.insertRow(1)
    # get the index to the step and then to its output list child
    second_step_index = model.index(1, 0)
    second_step_outputs = model.index(0, 0, second_step_index)
    # add an output
    model.insertRow(0, second_step_outputs)
    # get the index of the new output
    output_index = model.index(0, 0, second_step_outputs)
    # add a new connection and connect it to our previous reference to
    # the input above. this automatically creates a connection on the
    # input index pointing back to this output
    model.insertRow(0, output_index)
    model.setData(model.index(0, 0, output_index), input_index)
    # delete the connection on the input, this will automatically remove
    # the connection on the output index as well
    #model.removeRow(0, input_index)
    #model.removeRow(0)

    model.insertRow(1, input_list_index)
    model.insertRow(0, second_step_outputs)

    # redirect the connection to a different output without disconnecting first
    model.setData(model.index(0, 0, output_index), model.index(1, 0, input_list_index))

    flow_view = QtGui.QGraphicsView()
    flow_view.setBackgroundBrush(QtCore.Qt.gray)
    flow_view.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
    flow_view.setScene(flow_scene)

    proxy_model = SampleProxy(QtCore.QPersistentModelIndex(second_step_outputs))
    proxy_model.setSourceModel(model)

    tree_view.setModel(model)
    table_view = QtGui.QTableView()
    table_view.setModel(proxy_model)

    main_window.setCentralWidget(flow_view)

    main_window.show()

    tree_view.show()
    table_view.show()

    sys.exit(my_app.exec_())
