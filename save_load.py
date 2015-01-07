from PySide import QtCore, QtGui
import json
import sys, os

def save_model(model, filename):
    print "hello"
    with open(filename[0], 'w') as fout:
        items = []
        for item_index in range(model.item_count()):
            item = {"name":model.data(item_index,"name"), "x_pos":model.data(item_index, "position").x(), "y_pos":model.data(item_index, "position").y()}
            items.append([item])
        json.dump(items, fout)
    fout.close()

def open_model(model, filename):
    with open(filename[0], 'r') as f:
        file = json.load(f)
        for item_index in range(len(file)):
            item_name = file[item_index][0]["name"]
            item_position_x = file[item_index][0]["x_pos"]
            item_position_y = file[item_index][0]["y_pos"]
            model.set_data(item_index, "name", item_name)
            new_coords = QtCore.QPoint(item_position_x, item_position_y)
            model.set_data(item_index, "position", new_coords)
    f.close()
    return model
