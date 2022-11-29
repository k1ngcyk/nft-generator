import json
import os
from pathlib import Path
from dataclasses import dataclass
import csv


@dataclass
class Component:
    category = None
    item = None
    count = 0
    filepath = None
    type_json = None
    value_json = None
    mark = None
    limit = None
    mode = None


def read_csv(filename):
    with open(filename, "r") as fp:
        reader = csv.reader(fp)
        next(reader, None)  # skip the headers
        data_read = [row for row in reader]
        return data_read


def get_components_and_layer_names(csv_data):
    components = []
    layers = []
    for row in csv_data:
        component = component_from_csv_row(row)
        if component.category not in layers:
            layers.append(component.category)
        components.append(component)
    return components, layers


def component_from_csv_row(row):
    component = Component()
    component.category = row[0]
    component.item = row[1]
    component.count = int(row[2])
    component.filepath = row[3]
    component.type_json = row[4]
    component.value_json = row[5]
    component.mark = row[6]
    component.limit = row[7]
    component.mode = row[8]
    return component


def main():
    csv_filename = "data.csv"
    csv_data = read_csv(csv_filename)
    components, layer_names = get_components_and_layer_names(csv_data)
    files = [x.filepath for x in components]
    for path in files:
        try:
            f = open(path, "r")
            f.close()
        except:
            print(path)


if __name__ == '__main__':
    main()
