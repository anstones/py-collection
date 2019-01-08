import json, os

file = open('./new_json.txt', 'w+')


def read_write_json():
    with open('./oeasypic/58daojia.json', 'r') as f:
        for line in f:
            line = line[:-2]
            obj = json.loads(line)
            code = obj.get("id_code", "")
            name = obj.get("name", "")
            if code is not None and code.startswith('6'):
                file.write(line + ',\n')
            file.flush()


read_write_json()