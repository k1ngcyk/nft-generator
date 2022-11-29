import json
import os
from pathlib import Path


def main():
    dirs = ["seal"]
    total_count = 0
    for dir_to_check in dirs:
        print("Checking {}:".format(dir_to_check))
        check_dir = "./generated/{}/".format(dir_to_check)
        p = Path(check_dir).glob('**/*')
        files = [x.stem for x in p if x.is_file() and len(x.suffixes) == 0]
        file_count = len(files)
        total_count += file_count
        for filename in files:
            data = None
            with open(check_dir + filename, "r") as f:
                try:
                    data = json.load(f)
                except:
                    print(filename)
            attributes = data["attributes"]
            new_attributes = []
            temp = None
            for attr in attributes:
                if attr["trait_type"] != "Ball":
                    new_attributes.append(attr)
                else:
                    temp = attr["value"]
                    new_attributes.append({"trait_type": "Ball", "value": "Seal"})
            new_attributes.append({"trait_type": "Seal Type", "value": temp})
            data["attributes"] = new_attributes
            with open(check_dir + filename, "w") as f:
                json.dump(data, f, ensure_ascii=False)
            print(filename, " checked. ", data)

    print("total count: {}".format(total_count))



if __name__ == '__main__':
    main()
