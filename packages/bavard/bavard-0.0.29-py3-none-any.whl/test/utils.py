import json


def load_json_file(path):
    with open(path) as f:
        return json.load(f)


def deep_equal_json(a: object, b: object) -> bool:
    return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
