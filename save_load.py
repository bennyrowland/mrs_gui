from PySide import QtCore, QtGui
import json
import sys, os

from pyflow.model import FlowModel


def save_model(model, filename):
    print "hello"
    with open(filename[0], 'w') as fout:
        items = []
        for item_index in range(model.item_count()):
            item = {"name":model.data(item_index,"name"), "x_pos":model.data(item_index, "position").x(), "y_pos":model.data(item_index, "position").y()}
            items.append([item])
        json.dump(items, fout)
    fout.close()


def open_model(filename):
    with open(filename[0], 'r') as fin:
        model = FlowModel()
        f = json.load(fin)
        for item_index in range(len(f)):
            model.add_item()
            item_name = f[item_index][0]["name"]
            item_position_x = f[item_index][0]["x_pos"]
            item_position_y = f[item_index][0]["y_pos"]
            model.set_data(item_index, "name", item_name)
            new_coords = QtCore.QPoint(item_position_x, item_position_y)
            model.set_data(item_index, "position", new_coords)
    fin.close()
    return model
