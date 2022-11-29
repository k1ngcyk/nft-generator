import csv
from PIL import Image
from dataclasses import dataclass
import random
import json
import numpy
from blend_modes import screen
import asyncio


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


def background(f):
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(None, f, *args, **kwargs)

    return wrapped


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


def main():
    global components
    global description
    csv_filename = "data.csv"
    csv_data = read_csv(csv_filename)
    components, layer_names = get_components_and_layer_names(csv_data)
    generate_count = sum(x.count for x in list(filter(lambda x: x.category == layer_names[0], components)))
    # generate_dir = "./generated/"
    generate_dir = "./generated/sun-by-mountain/"
    filter_count = sum(x.count for x in list(filter(lambda component: component.limit != '' and component.count > 0, components)))
    print("filter_items: {}".format(filter_count))
    retry_limit = 30
    current_index = 0
    result_array = []
    result_set_array = []
    retry_count = 0
    while current_index < filter_count:
        temp_result_stack = [None] * len(layer_names)
        components_with_filter = list(filter(lambda component: component.limit != '' and component.count > 0, components))
        filter_component = random.choice(components_with_filter)
        filter_component_layer_index = layer_names.index(filter_component.category)
        temp_result_stack[filter_component_layer_index] = filter_component

        current_limit = filter_component.limit
        current_layer = filter_component.category
        components_with_mark = list(filter(lambda component: component.mark == current_limit and component.category != current_layer and component.count > 0, components))
        limited_layers = list(set([x.category for x in components_with_mark]))
        for layer in limited_layers:
            components_with_mark_layer = list(filter(lambda component: component.mark == current_limit and component.category == layer and component.count > 0, components))
            random_component = random.choice(components_with_mark_layer)
            layer_index = layer_names.index(random_component.category)
            temp_result_stack[layer_index] = random_component
        
        for idx, layer in enumerate(temp_result_stack):
            if layer is None:
                current_layer = layer_names[idx]
                components_layer = list(filter(lambda component: component.category == current_layer and component.count > 0, components))
                random_component = random.choice(components_layer)
                layer_index = layer_names.index(random_component.category)
                temp_result_stack[layer_index] = random_component
        
        temp_result_set = set(list(map(lambda x: x.item, temp_result_stack)))
        if temp_result_set not in result_set_array:
            for component in temp_result_stack:
                # components[components.index(component)].count -= 1
                component.count -= 1
            result_set_array.append(temp_result_set)
            result_array.append(temp_result_stack)
            current_index += 1
            retry_count = 0
            if current_index % 10 == 0:
                print("{}/{}".format(current_index, filter_count))
        else:
            if retry_count > retry_limit:
                current_index += 1
                retry_count = 0
            else:
                retry_count += 1

    remaining_count = generate_count - filter_count
    print("remaining count: {}".format(remaining_count))
    current_index = 0
    retry_count = 0
    while current_index < remaining_count:
        temp_result_stack = [None] * len(layer_names)
        for idx, layer in enumerate(temp_result_stack):
            if layer is None:
                current_layer = layer_names[idx]
                components_layer = list(filter(lambda component: component.category == current_layer and component.count > 0, components))
                random_component = random.choice(components_layer)
                layer_index = layer_names.index(random_component.category)
                temp_result_stack[layer_index] = random_component
        
        temp_result_set = set(list(map(lambda x: x.item, temp_result_stack)))
        if temp_result_set not in result_set_array:
            for component in temp_result_stack:
                # components[components.index(component)].count -= 1
                component.count -= 1
            result_set_array.append(temp_result_set)
            result_array.append(temp_result_stack)
            current_index += 1
            retry_count = 0
            if current_index % 100 == 0:
                print("{}/{}".format(current_index, remaining_count))
        else:
            if retry_count > retry_limit:
                current_index += 1
                retry_count = 0
            else:
                retry_count += 1


    actual_gen_count = len(result_array)
    token_id = list(range(actual_gen_count))
    random.shuffle(token_id)

    @background
    def process_stack(idx, result_stack):
        image = None
        attributes = []
        for component in result_stack:
            attributes.append({"trait_type": component.type_json, "value": component.value_json})
            foreground = Image.open(component.filepath)
            image = add_png(foreground, image, component.mode)
        current_token_id = token_id[idx]
        image.save(generate_dir + str(current_token_id) + ".png", format="PNG")
        data = {
            "name": "Bubble #" + str(current_token_id),
            "image": "images/" + str(current_token_id) + ".png",
            "attributes": attributes
        }
        with open(generate_dir + str(current_token_id), "w") as f:
            json.dump(data, f, ensure_ascii=False)
        print(current_token_id, " generated. ", data)

    for idx, result_stack in enumerate(result_array):
        process_stack(idx, result_stack)

    print("actual generated: {} in a limit of {} retries.".format(actual_gen_count, retry_limit))




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
