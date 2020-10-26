import json
import os

def test():
    alignment_path = os.path.join('data', 'results', 'output', 'alignment', 'test.json')
    with open(alignment_path, 'r', encoding='utf-8') as f:
        json_string = f.read()[1:-1]
        test_json = json.load(json_string)
        print(test_json)
        # json_file = json.load(f)
        # test_json = json.load(json_file)
        # print(test_json)


if __name__ == '__main__':
    test()