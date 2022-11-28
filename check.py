import json
import os


def main():
    # dirs = ["3d-text", "blackhole", "bricks", "cluster", "glass-ball", "snipper", "sun-by-mountain"]
    dirs = ["blackhole", "bricks", "cluster", "glass-ball", "snipper", "sun-by-mountain"]
    total_count = 0
    total_repeat = 0
    for dir_to_check in dirs:
        print(dir_to_check, ":")
        values = []
        check_dir = "./generated/{}/".format(dir_to_check)
        file_count = len([name for name in os.listdir(check_dir)])
        total_count += file_count
        for token_id in range(file_count):
            with open(check_dir + str(token_id), "r") as f:
                data = json.load(f)
                attributes = data["attributes"]
                value_set = set(list(map(lambda attr: attr["value"], attributes)))
                if value_set in values:
                    print(token_id, 'repeat with', values.index(value_set), value_set)
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
