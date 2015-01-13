__author__ = 'ben'

from PySide import QtGui, QtCore

from pyflow.model import FlowModel

import sys
if __name__ == "__main__":
    my_app = QtGui.QApplication(sys.argv)

    main_window = QtGui.QMainWindow()

    main_window.resize(400, 400)
    main_window.setWindowTitle("MRS GUI tool v0.1")

    # create a standard QTreeView to display the model
    tree_view = QtGui.QTreeView()

    # create an empty model
    model = FlowModel()
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
    model.setData(input_index, "Example Input")

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
    model.removeRow(0, input_index)

    tree_view.setModel(model)

    main_window.setCentralWidget(tree_view)

    main_window.show()

    sys.exit(my_app.exec_())
