import json
import os
from pathlib import Path


def main():
    # dirs = ["3d-text", "blackhole", "bricks", "cluster", "glass-ball", "snipper", "sun-by-mountain"]
    dirs = ["1of1", "3d-text", "blackhole", "bricks", "cluster", "glass-ball", "seal", "snipper", "sun-by-mountain"]
    total_count = 0
    total_repeat = 0
    for dir_to_check in dirs:
        print("Checking {}:".format(dir_to_check))
        values = []
        check_dir = "./generated/{}/".format(dir_to_check)
        p = Path(check_dir).glob('**/*')
        files = [x for x in p if x.is_file()]
        for path in files:
            if str(path).lower().endswith(".json"):
                os.rename(path, path.with_suffix(""))
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
                value_set = set(list(map(lambda attr: attr["value"], attributes)))
                if value_set in values:
                    print(filename, 'repeat with', values.index(value_set), value_set)
                    values.append(None)
                else:
                    values.append(value_set)
        repeat = len(list(filter(lambda x: x is None, values)))
        print(repeat)
        total_repeat += repeat
    print("total repeat: {}".format(total_repeat))
    print("total count: {}".format(total_count))



if __name__ == '__main__':
    main()
