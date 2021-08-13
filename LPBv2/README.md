# LeaguePyBot [BETA, macos only, windows broken]

Working on v2

Documentation: https://github.com/DorskFR/LeaguePyBot/wiki

Alpha footage: https://youtu.be/cwilX5sMFpA

Beta footage:

- Garen: https://youtu.be/negOli1mS7M
- Brand: https://youtu.be/RSgxkZgNVTc
- Ezreal: https://youtu.be/rx0AiieW6w8

### Features:

- **Client API** to deal with the League Client using LCU API

  - [x] Create lobby (custom, coop, normal, ranked)
  - [x] Start Matchmaking and accept Ready Check
  - [x] Champ select show intent
  - [x] Champ select list of ban targets according to role
  - [x] Champ select list of pick targets according to role
  - [x] Command random player
  - [x] Command all players (probably does not _really_ work)
  - [x] Report all players
  - [x] Dismiss all notifications (level up, missions, honor, etc.)
  - [ ] Auto accept rewards
  - [x] Chain games
  - [x] Retrieve basic account information such as level
  - [ ] Login and rotation over multiple accounts
  - [x] Load hotkeys and patch quickbinds
  - [x] Patch game settings (_backup yours before_)

- **Game API** to use the in-game API to retrieve live game info

  - [x] PlayerInfo: level, HP, gold, etc.
  - [x] PlayerStats: AttackDamage, AttackSpeed, etc.
  - [x] PlayerScore: CS, etc. (although not used for anything yet)
  - [x] Members of the current game
  - [x] Items, consumables and their slots
  - [x] Game events, game timer

- **Vision**

  - [x] Mapping of the main zones (towers, shop, nexus) for both sides
  - [x] Mapping of neutral units
  - [x] Mapping of neutral locations (middle of lanes, rivers, etc.)
  - [x] Computer Vision on the minimap to localize all 10 players on the map and remember close to which zone they were last seen
  - [x] Computer Vision on 80% of the screen to identify units (minions, champions, buildings) and their team.
  - [ ] Load champion minimap icon from assets API or data dragon dynamically and resize to correct dimension

- **Bot Logic**

  - [x] Different conditions required to attack minions, champions or buildings
  - [x] Watches health and can use healing items and spells
  - [x] Watches health and can recall if low life
  - [x] Watches gold and can recall if rich enough

- **Build**

  - [x] Retrieve data dragon item info per region/locale
  - [ ] Load builds from online resources depending on champion
  - [ ] Change recursive buy function to allow breaking out when no money (instead of buying all cheap items and filling inventory)

- **Actions**

  - [x] Added basic movements: fall_back, go_to_lane, follow_allies, recall
  - [x] Added basic combat: attack [safest, average, riskiest] position of [minion, champion, building]
  - [x] Use of abilities based on target and mana / resource level
  - [x] Use of consumable items, summoner spells
  - [x] Buy from shop a recommended build

- **Controller**

  - [x] Cross platform control of keyboard and mouse
  - [x] Global killswitch to stop the program

- **NetInterface**
  - [ ] Allow remote control
  - [ ] Allow deferring the template matching on the screenshots to a server

### Other ideas :

- headless client
- helper tools for loot
- retrieve data dragon info per champ and load spell cooldowns

### Notes

Personal project that I use to learn developing in Python.
Initially using only Computer Vision with OpenCV, I am now trying to use the existing APIs to communicate with the client and the game.

Some potential use cases:

- Level up an account to a certain level with coop games.
- Track where the enemy jungler is and remember last position.
- Never miss a ready check no matter how many times people dodge.
- Report everyone in a game without clicking 45 times.
- Get perma banned for using an unauthorized 3rd party tool.
- Ideally one day, play against the bot to practice specific scenarii.

### Disclaimer

LeaguePyBot isn’t endorsed by Riot Games and doesn’t reflect the views or opinions of Riot Games or anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.
