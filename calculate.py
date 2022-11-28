import json
from collections import Counter
import csv


def main():
    values = []
    csv_dict = {}
    generate_count = 1185
    generate_dir = "./generated/"
    for token_id in range(generate_count):
        with open(generate_dir + str(token_id), "r") as f:
            data = json.load(f)
            attributes = data["attributes"]
            for attr in attributes:
                type_json = attr["trait_type"]
                value_json = attr["value"]
                values.append(type_json + "," + value_json)
    count_dict = dict(Counter(values))
    with open("data.csv", "r") as fp:
        reader = csv.reader(fp)
        next(reader, None)  # skip the headers
        for row in reader:
            csv_dict[(row[4] + "," + row[5])] = int(row[2])
    print(csv_dict)
    for k, v in count_dict.items():
        real_count = v
        target_count = csv_dict[k]
        print(k, real_count, target_count, real_count == target_count, sep='\t')



if __name__ == '__main__':
    main()
