Working on v2

Primary goals are :

- **LeagueClient** to deal with the Client using LCU API

  - Create lobby / Get in queue
  - Start Matchmaking and accept Ready Check
  - Champ select instant intent, ban, pick
  - Command/Report at end of game
  - Chain games
  - Retrieve basic account information such as level
  - Login and rotation over multiple accounts

- **GameWatcher** to use the in-game API to retrieve live game info

  - PlayerInfo: level, HP, gold, etc.
  - PlayerStats: AttackDamage, AttackSpeed, etc.
  - Items and their slots
  - Game events, game timer

- **ScreenWatcher**

  - Take fast screenshots of predefined zones
  - Analyze the screenshots to determine actions

- **Keyboard and Mouse**

  - Control keyboard and mouse to execute actions

- **NetInterface**
  - Allow remote control
  - Allow remote analysis of the screenshots

Secondary ideas :

- headless client
- helper tools for loot
- load builds from online resources depending on champion
- play on any lane
