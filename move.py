import json
import os
from pathlib import Path
import random
import json
import shutil


def main():
    dirs = ["1of1", "3d-text", "blackhole", "bricks", "cluster", "glass-ball", "seal", "snipper", "sun-by-mountain"]
    total_count = 0
    for dir_to_check in dirs:
        check_dir = "./generated/{}/".format(dir_to_check)
        p = Path(check_dir).glob('**/*')
        files = [x.stem for x in p if x.is_file() and len(x.suffixes) == 0]
        file_count = len(files)
        total_count += file_count
    print("total count: {}".format(total_count))
    token_id = list(range(total_count))
    random.shuffle(token_id)
    final_dir = "./output/"
    for dir_to_check in dirs:
        print("Processing {}:".format(dir_to_check))
        check_dir = "./generated/{}/".format(dir_to_check)
        p = Path(check_dir).glob('**/*')
        files = [x for x in p if x.is_file() and len(x.suffixes) == 0]
        file_stems = [x.stem for x in files]
        for filename in file_stems:
            data = None
            with open(check_dir + filename, "r") as f:
                try:
                    data = json.load(f)
                except:
                    print(filename)
            attributes = data["attributes"]
            current_token_id = token_id.pop()
            new_data = {
                "name": "Bubble #" + str(current_token_id),
                "image": "images/" + str(current_token_id) + ".png",
                "attributes": attributes
            }
            with open(final_dir + str(current_token_id), "w") as f:
                json.dump(new_data, f, ensure_ascii=False)
            shutil.copy(check_dir + filename + ".png", final_dir + str(current_token_id) + ".png")
            print("{}/{} moved. Current id: {}, original is {}/{}, new data: {}".format(len(token_id), total_count, current_token_id, dir_to_check, filename, new_data))



if __name__ == '__main__':
    main()
