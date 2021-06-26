Working on v2 [Currently not functional, but soon]

Alpha footage: https://youtu.be/cwilX5sMFpA

Features are :

- **Client API** to deal with the League Client using LCU API (locale agnostic)

  - [x] Create lobby (custom, coop, normal, ranked)
  - [x] Start Matchmaking and accept Ready Check
  - [x] Champ select show intent
  - [x] Champ select list of ban targets according to role
  - [x] Champ select list of pick targets according to role
  - [x] Command random player
  - [x] Command all players (probably does not _really_ work)
  - [x] Report all players
  - [ ] Auto accept / dismiss all notifications (level up, missions, honor, etc.)
  - [ ] Auto accept rewards
  - [x] Chain games
  - [x] Retrieve basic account information such as level
  - [ ] Login and rotation over multiple accounts

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

- **Bot Logic**

  - [x] Different conditions required to attack minions, champions or buildings
  - [x] Watches health and can use healing items and spells
  - [x] Watches health and can recall if low life
  - [x] Watches gold and can recall if rich enough

- **Actions**

  - [x] Added basic movements: fall_back, go_to_lane, follow_allies, recall
  - [x] Added basic combat: attack [safest, average, riskiest] position of [minion, champion, building]
  - [x] Use of abilities based on target and mana / resource level
  - [x] Use of consumable items, summoner spells
  - [ ] Actually understands what summoner spells do
  - [x] Cross platform control of keyboard and mouse
  - [ ] Buy from shop a recommended build

- **Controller**

  - [x] Cross platform control of keyboard and mouse
  - [x] Global killswitch to stop the program
  - [ ] Load hotkeys and settings from the game config files

- **NetInterface**
  - [ ] Allow remote control
  - [ ] Allow deferring the template matching on the screenshots to a server

Secondary ideas :

- headless client
- helper tools for loot
- load builds from online resources depending on champion
- retrieve data dragon info per champ and load spell cooldowns
- load item builds from online resources
- retrieve data dragon item info
