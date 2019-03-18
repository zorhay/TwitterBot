import json


def save_dict_list(dict_list, out_file='outh_data.json'):
    with open(out_file, 'a') as f:
        json.dump(dict_list, f)
        f.write('\n')


def read_dict_list(out_file='outh_data.json'):
    with open(out_file, 'r') as f:
        rd = f.readlines()
    dict_list = []
    for dicts in rd:
        dict_list += json.loads(dicts)
    return dict_list


def make_whole_json_file(file):
    dict_list = read_dict_list(file)
    with open(file, 'w') as f:
        json.dump(dict_list, f)
