import csv
from PIL import Image
from dataclasses import dataclass
import random
import json
import numpy
from blend_modes import screen

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


description = "This is a description"
layers = ["Background",
          "Bed",
          "Pillow",
          "Skin Color",
          "Head",
          "Expression",
          "Sheet",
          "Arms & Body",
          "Device",
          "Topfixed"]  # From bottom to top, should match category in csv
components = []


def read_csv(filename):
    with open(filename, "r") as fp:
        reader = csv.reader(fp)
        next(reader, None)  # skip the headers
        data_read = [row for row in reader]
        return data_read


def main():
    global components
    global description
    csv_filename = "data.csv"
    csv_data = read_csv(csv_filename)
    components = [component_from_csv_row(row) for row in csv_data]
    generate_count = 3
    generate_dir = "./generated/"
    filter_count = sum(x.count for x in list(filter(lambda component: component.limit != '' and component.count > 0, components)))
    token_id = range(generate_count)
    random.shuffle(token_id)
    for token_id_idx in range(filter_count):
        result_stack = [None] * len(layers)
        components_with_filter = list(filter(lambda component: component.limit != '' and component.count > 0, components))
        random_component = random.choice(components_with_filter)
        layer_index = layer.index(random_component.category)
        result_stack[layer_index] = random_component
        random_component.count = random_component.count - 1
        current_limit = random_component.limit
        current_layer = random_component.category
        components_with_mark = list(filter(lambda component: component.mark == current_limit and component.category != current_layer and component.count > 0, components))
        limited_layers = list(set([x.category for x in components_with_mark]))
        for layer in limited_layers:
            components_with_mark_layer = list(filter(lambda component: component.mark == current_limit and component.category == layer and component.count > 0, components))
            random_component = random.choice(components_with_mark_layer)
            layer_index = layer.index(random_component.category)
            result_stack[layer_index] = random_component
            random_component.count = random_component.count - 1
        
        for idx, layer in enumerate(result_stack):
            if layer is None:
                current_layer = layers[idx]
                components_layer = list(filter(lambda component: component.category == layer and component.count > 0, components))
                random_component = random.choice(components_layer)
                layer_index = layer.index(random_component.category)
                result_stack[layer_index] = random_component
                random_component.count = random_component.count - 1
        
        image = None
        attributes = []
        for component in result_stack:
            attributes.append({"trait_type": component.type_json, "value": component.value_json})
            # foreground = Image.open(component.filepath)
            # image = add_png(foreground, image, component.mode)
        current_token_id = token_id[token_id_idx]
        # image.save(generate_dir + str(current_token_id) + ".png", format="PNG")
        data = {
            "name": "Whatever #" + str(current_token_id),
            "image": "images/" + str(current_token_id) + ".png",
            "attributes": attributes
        }
        # with open(generate_dir + str(current_token_id), "w") as f:
        #     json.dump(data, f, ensure_ascii=False)
        print(token_id, " generated. ", data)
    
    remaining_count = generate_count - filter_count
    for token_id_idx in range(remaining_count):
        result_stack = [None] * len(layers)
        for idx, layer in enumerate(result_stack):
            if layer is None:
                current_layer = layers[idx]
                components_layer = list(filter(lambda component: component.category == layer and component.count > 0, components))
                random_component = random.choice(components_layer)
                layer_index = layer.index(random_component.category)
                result_stack[layer_index] = random_component
                random_component.count = random_component.count - 1

        image = None
        attributes = []
        for component in result_stack:
            attributes.append({"trait_type": component.type_json, "value": component.value_json})
            # foreground = Image.open(component.filepath)
            # image = add_png(foreground, image, component.mode)
        current_token_id = token_id[filter_count + token_id_idx]
        # image.save(generate_dir + str(current_token_id) + ".png", format="PNG")
        data = {
            "name": "Whatever #" + str(current_token_id),
            "image": "images/" + str(current_token_id) + ".png",
            "attributes": attributes
        }
        # with open(generate_dir + str(current_token_id), "w") as f:
        #     json.dump(data, f, ensure_ascii=False)
        print(token_id, " generated. ", data)



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


def get_component(category):
    items = filter(lambda component: component.category == category and component.count > 0, components)
    items = list(items)
    result = random.choice(items)
    return result


def add_png(foreground, background, mode=None):
    foreground = foreground.convert('RGBA')
    if background is None:
        output = Image.new('RGBA', foreground.size)
        output = Image.alpha_composite(output, foreground)
        return output
    background = background.convert('RGBA')
    output = Image.new('RGBA', background.size)
    output = Image.alpha_composite(output, background)
    if mode == 'screen':
        current_background = numpy.array(output)
        current_background = current_background.astype(float)
        current_foreground = numpy.array(foreground)
        current_foreground = current_foreground.astype(float)
        screen_result = screen(current_background, current_foreground, 1.0)
        screen_result = numpy.uint8(screen_result)
        output = Image.fromarray(screen_result)
    else:
        output = Image.alpha_composite(output, foreground)
    return output


if __name__ == '__main__':
    main()
