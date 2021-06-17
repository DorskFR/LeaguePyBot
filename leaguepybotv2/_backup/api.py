import requests
import json

base = "https://127.0.0.1:2999"
summonerName = "MVPython"
urls = [
    "/liveclientdata/allgamedata",
    "/liveclientdata/activeplayer",
    "/liveclientdata/activeplayername",
    "/liveclientdata/activeplayerabilities",
    "/liveclientdata/activeplayerrunes",
    "/liveclientdata/playerlist",
    f"/liveclientdata/playerscores?summonerName={summonerName}",
    f"/liveclientdata/playersummonerspells?summonerName={summonerName}",
    f"/liveclientdata/playermainrunes?summonerName={summonerName}",
    f"/liveclientdata/playeritems?summonerName={summonerName}",
    "/liveclientdata/eventdata",
    "/liveclientdata/gamestats",
]


with open("leaguepybotv2/_backup/coop5.json", "w") as f:
    for url in urls:
        response = requests.get(base + url, verify=False)
        f.write(base + url + "\n\n")
        f.write(json.dumps(response.json()))
        f.write("\n\n\n\n")
