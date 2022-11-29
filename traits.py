import json
import os
from pathlib import Path


def main():
    total_count = 0
    dir_to_check = "output"
    print("Checking {}:".format(dir_to_check))
    trait_dict = {}
    check_dir = "./{}/bubble-metadata/".format(dir_to_check)
    p = Path(check_dir).glob('**/*')
    files = [x.stem for x in p if x.is_file() and len(x.suffixes) == 0]
    file_count = len(files)
    total_count += file_count
    for filename in files:
        with open(check_dir + filename, "r") as f:
            try:
                data = json.load(f)
            except:
                print(filename)
            attributes = data["attributes"]
            for attr in attributes:
                type_json = attr["trait_type"]
                value_json = attr["value"]
                if type_json in trait_dict:
                    if value_json in trait_dict[type_json]:
                        trait_dict[type_json][value_json] += 1
                    else:
                        trait_dict[type_json][value_json] = 1
                else:
                    trait_dict[type_json] = { value_json: 1 }
    print(trait_dict)
    print("total count: {}".format(total_count))



if __name__ == '__main__':
    main()
