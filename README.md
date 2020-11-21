# LeaguePyBot

An attempt at a computer vision bot for League Of Legends (vs AI).
Only works on Windows.
Patterns in the client match the Japanese language of the interface.
Made to play Ahri only but not hard to modify for other champs

##### Dependencies

* _**Python 3.9**
* **OpenCV** for Computer Vision (Template Matching)
* **pytesseract** and Google Tesseract OCR to read gold amount
* **mss** for fast screenshots
* **win32api, gui, con** for native clicks, etc.
* **pydirectinput** for keyboard input that are detected in game
* **Thread pool** to make the template matching faster
* **pyWinhook** for a global hotkey to close the app ('k')_

##### Fight Sequence

* If there's no enemies:
    * If there's no allied minions: go to tower
    * If there's allied minions: follow them
    * Ignore allied champions

* If there's enemy minions or champions:
    * If there's less than 2 allied minions or if there is both an enemy tower and an enemy champion, fall back
    * If there's no enemy tower and we have the numerical advantage, stand ground and fight
    * Same situation but we do not have numerical advantage, reposition and fight

##### Main loop exit triggers

* being low life
* having more than 2500 gold
* being back at the shop after dying
* game ending

##### Many things could be improved:
- last hitting for better gold growth
- manage mana
- map the items from the in-game shop in an dictionary then define builds by calling from this dictionary
- handle a champion rotation if for some reason someone (a faster bot) locks ahri
- check and create the log folder if not existing
- recalculate the position of target after fall_back as otherwise it gets translated by as much as we moved
- handle client popups (key fragment, rewards, etc.)
- handle when the game finishes but we did not detect the end of game box in time
- add other languages (simply replace the screenshot files of the client menu items)
- accept command line arguments to customize the launch of the script without changing the code
- change lane, random lane, etc.
- detect who is the strongest ally and join him in fight to push one lane faster
- fix some weird detections of lowlife (either enemy or even with no char around)
- add emotes and spam master after kills