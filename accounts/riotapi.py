import requests
import json

KEY = "RGAPI-c928d461-5aca-4932-9932-3f06cc98ec18"

ACCOUNTS = [  # region, name, id, account_id, puuid, login
    {
        "region": "jp1",
        "name": "NotｰYourｰFriend",
        "login": "FioraJapan3001",
    },
    {
        "region": "jp1",
        "name": "soloplayer",
        "login": "FioraJapan3002",
    },
    {
        "region": "jp1",
        "name": "OnlySplit",
        "login": "FioraJapan3003",
    },
    {
        "region": "jp1",
        "name": "SlashーMuteーAll",
        "login": "FioraJapan3004",
    },
    {
        "region": "jp1",
        "name": "憤怒調節障害者",
        "login": "FioraJapan3005",
    },
    {
        "region": "jp1",
        "name": "通報しないで",
        "login": "FioraJapan3006",
    },
    {
        "region": "jp1",
        "name": "ThisServerIsHell",
        "login": "FioraJapan3007",
    },
    {
        "region": "jp1",
        "name": "MapUnawarePlayer",
        "login": "FioraJapan3008",
    },
    {
        "region": "jp1",
        "name": "少女終末旅行続",
        "login": "FioraJapan3009",
    },
    {
        "region": "jp1",
        "name": "試合後報告するよ",
        "login": "FioraJapan3010",
    },
    {
        "region": "jp1",
        "name": "沈黙は金 allmute",
        "login": "FioraJapan3011",
    },
    {
        "region": "jp1",
        "name": "Fiora1v9",
        "login": "FioraJapan3012",
    },
    {
        "region": "jp1",
        "name": "沈黙と無視1v9",
        "login": "FioraJapan3013",
    },
    {
        "region": "jp1",
        "name": "Fiora Bluesteel",
        "login": "FioraJapan3014",
    },
    {
        "region": "jp1",
        "name": "1v9JapanServer",
        "login": "FuckYouJapanVeryMuch",
    },
    {
        "region": "jp1",
        "name": "WinnieーTheーFlu",
        "login": "WinnieTheFluJP",
    },
    {
        "region": "jp1",
        "name": "ーMuteーAllー",
        "login": "RiotJapanSucks",
    },
    {
        "region": "jp1",
        "name": "ーTiltedFioraー",
        "login": "FioraTiltMaster",
    },
    {
        "region": "jp1",
        "name": "自転車で旅しよう",
        "login": "jrzlmcbr",
    },
    {
        "region": "jp1",
        "name": "蘇生完成フィオラ",
        "login": "DorskJapan",
    },
    {
        "region": "jp1",
        "name": "FKuJPserver",
        "login": "bunchoftardsriot",
    },
    {
        "region": "jp1",
        "name": "また停止フィオラ",
        "login": "fuckyouriotweakbans",
    },
    {
        "region": "jp1",
        "name": "永久停止フィオラ",
        "login": "CyberiaAlita99",
    },
    {
        "region": "jp1",
        "name": "フランスDSK",
        "login": "DorskFRinJP",
    },
    {
        "region": "euw1",
        "name": "DorskFR",
        "login": "DorskFR",
    },
    {
        "region": "euw1",
        "name": "DorskJP",
        "login": "DorskJP",
    },
    {
        "region": "eun1",
        "name": "Dorsk",
        "login": "Dorsk",
    },
    {
        "region": "na1",
        "name": "JapanServerSucks",
        "login": "FioraJapan",
    },
    {
        "region": "jp1",
        "name": "NextGame",
        "login": "FioraJapan3015",
        "status": "10min queue",
    },
    {
        "region": "jp1",
        "name": "MVPython",
        "login": "FioraJapan3016",
    },
    {
        "region": "jp1",
        "name": "Speedconda",
        "login": "FioraJapan3017",
    },
    {
        "region": "jp1",
        "name": "Dresden Black",
        "login": "leaguepybot001",
        "status": "Perma Banned",
    },
    {
        "region": "jp1",
        "name": "Bestagon",
        "login": "leaguepybot002",
        "status": "OK",
    },
    {"region": "jp1", "name": "名誉没有", "login": "leaguepybot003", "status": "OK"},
    {
        "region": "jp1",
        "name": "Jungle Is A Bot",
        "login": "leaguepybot004",
    },
    {
        "region": "jp1",
        "name": "S11 Fiora OTP",
        "login": "leaguepybot005",
    },
    {
        "region": "jp1",
        "name": "I Carry Or Feed",
        "login": "leaguepybot006",
    },
]


class LeagueAccount:
    def __init__(self):
        self.mastery = 0
        self.matches = 0
        try:
            with open("accounts.json", "r") as f:
                self.accounts = json.load(f)
        except:
            self.get_account_ids()

    def get_account_ids(self):
        for idx, account in enumerate(ACCOUNTS):

            # call 1
            url = f"https://{account.get('region')}.api.riotgames.com/"
            url += (
                f"lol/summoner/v4/summoners/by-name/{account.get('name')}?api_key={KEY}"
            )
            response = requests.get(url)
            r = response.json()
            ACCOUNTS[idx]["id"] = r.get("id")
            ACCOUNTS[idx]["account_id"] = r.get("accountId")
            ACCOUNTS[idx]["puuid"] = r.get("puuid")

            # call 2
            url = f"https://{account.get('region')}.api.riotgames.com/"
            url += f"lol/summoner/v4/summoners/by-puuid/{ACCOUNTS[idx].get('puuid')}?api_key={KEY}"
            response = requests.get(url)
            r = response.json()
            ACCOUNTS[idx]["summoner_level"] = r.get("summonerLevel")

        with open("accounts.json", "w") as f:
            f.write(json.dumps(ACCOUNTS, indent=4))
        self.accounts = ACCOUNTS

    def get_mastery_total(self, champion_id):
        self.mastery = 0
        mastery = []
        for account in self.accounts:
            url = f"https://{account.get('region')}.api.riotgames.com/"
            url += f"lol/champion-mastery/v4/champion-masteries/by-summoner/"
            url += f"{account.get('id')}/by-champion/{champion_id}?api_key={KEY}"
            response = requests.get(url)
            r = response.json()
            mastery.append(r)
            self.mastery += int(r.get("championPoints") or 0)
        with open("mastery.json", "w") as f:
            f.write(json.dumps(mastery, indent=4))

    def get_all_matches(self, champion_id, match_types=[420, 430]):
        matches = []
        for match_type in match_types:
            for account in self.accounts:
                url = f"https://{account.get('region')}.api.riotgames.com/"
                url += f"lol/match/v4/matchlists/by-account/{account.get('account_id')}"
                url += f"?champion={champion_id}&queue={match_type}&beginIndex=10000&api_key={KEY}"
                response = requests.get(url)
                r = response.json()
                self.matches += int(r.get("totalGames") or 0)
                matches.append(r)
            with open("matches.json", "w") as f:
                f.write(json.dumps(matches, indent=4))


lol = LeagueAccount()
lol.get_mastery_total(114)
print(lol.mastery)
lol.get_all_matches(114)
print(lol.matches)
