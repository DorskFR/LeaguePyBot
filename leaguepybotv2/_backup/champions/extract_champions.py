import json

champions = {}


def read_json():
    with open("leaguepybotv2/champions/champions.json") as f:
        data = json.load(f)
        for name, champion_data in data.get("data").items():
            champions[name.lower()] = int(champion_data.get("key"))


def write_json():
    with open("leaguepybotv2/champions/champions_dict.json", "w+") as f:
        data = json.dumps(champions)
        f.write(data)


read_json()
write_json()
