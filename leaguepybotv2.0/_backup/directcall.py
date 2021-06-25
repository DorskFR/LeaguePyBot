import requests
from leaguepybotv2.core.utils import atob

CONNECTION = {
    "riotclient-auth-token": "-AeK79eZqLfJjl2U--qyqA",
    "riotclient-app-port": "54888",
    "region": "JP",
    "locale": "ja_JP",
    "remoting-auth-token": "vPSpHAs_oPKd9rvaSSj99g",
    "app-port": "54911",
    "install-directory": "/Volumes/T7/Software/League of Legends.app/Contents/LoL",
    "app-name": "LeagueClient",
    "ux-name": "LeagueClientUx",
    "ux-helper-name": "LeagueClientUxHelper",
    "log-dir": "LeagueClient Logs",
    "crash-reporting": "",
    "crash-environment": "JP1",
    "app-log-file-path": "/Volumes/T7/Software/League of Legends.app/Contents/LoL/Logs/LeagueClient Logs/2021-06-12T13-21-49_11505_LeagueClient.log",
    "app-pid": "11505",
    "output-base-dir": "/Volumes/T7/Software/League of Legends.app/Contents/LoL",
}

credentials = "riot:q5oo1CpS27CMENk_55xsNA"


headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Basic {atob(credentials)}",
}

server = "https://127.0.0.1:55690"
url = "/lol-loot/v1/player-loot"

resp = requests.get(server + url, headers=headers, verify=False)
if resp.status_code == 200:
    print(resp.json())
