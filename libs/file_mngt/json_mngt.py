import json

def json_reader():
    with open('data/data.json', 'r', encoding="utf-8") as f:
        data = json.load(f)
    return data

def json_writer(data):
    with open('data/data.json', 'w', encoding="utf-8") as f:
        json.dump(data.to_dict(), f, ensure_ascii=False, indent=4)

