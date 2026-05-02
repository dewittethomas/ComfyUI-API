import json

def load_json_file(path: str) -> list:
    with open(path) as f:
        return json.load(f)