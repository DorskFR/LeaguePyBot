# LeaguePyBot

ps: activate colorblind mode, be careful of my weird hotkey settings especially key 's' which I use for potions but by default is the 'stop' action I believe.

Jax fight demo: https://youtu.be/R3r0Z8AKQqo  
Jax full game demo: https://youtu.be/MfHIMEUrEQw  
Ahri full game demo: https://youtu.be/pPfZ384IQIQ

An attempt at a computer vision bot for League Of Legends (vs AI).
Only works on Windows.
Patterns in the client match the Japanese language of the interface.
Made to play Ahri, Illaoi and Jax but not hard to modify for other champs

## Dependencies

- **Python 3.9**
- **OpenCV** for Computer Vision (Template Matching)
- **pytesseract** and Google Tesseract OCR to read gold amount
- **mss** for fast screenshots
- **win32api, gui, con** for native clicks, etc.
- **pydirectinput** for keyboard input that are detected in game
- **Thread pool** to make the template matching faster
- **pyWinhook** for a global hotkey to close the app ('k')

## Fight Sequence

- If there's no enemies:

  - If there's no allied minions: go to tower
  - If there's allied minions: follow them
  - Ignore allied champions

- If there's enemy minions or champions:
  - If there's no allied minions
  - If there's less than 2 allied minions and a tower
  - If there is both an enemy tower and an enemy champion
  - If there is more than 3 enemy champions
    - Fall back for 2 seconds and fight
  - If there's no enemy tower and we have the numerical advantage, stand ground and fight
  - Same situation but we do not have numerical advantage, reposition for 0-1sc and fight

## Main loop exit triggers

- being low life
- being back at the shop after dying
- game ending

## Many things could be improved:

- last hitting for better gold growth
- manage mana
- map the items from the in-game shop in an dictionary then define builds by calling from this dictionary
- ~~handle a champion rotation if for some reason someone (a faster bot) locks ahri~~ added illaoi and Jax
- ~~check and create the log folder if not existing~~ done
- recalculate the position of target after fall_back as otherwise it gets translated by as much as we moved
- ~~handle client popups (key fragment, rewards, etc.)~~ done
- ~~handle when the game finishes but we did not detect the end of game box in time~~ done
- add other languages (simply replace the screenshot files of the client menu items)
- accept command line arguments to customize the launch of the script without changing the code
- change lane, random lane, etc.
- detect who is the strongest ally and join him in fight to push one lane faster
- ~~fix some weird detections of lowlife (either enemy or even with no char around)~~ mostly done
- add emotes and spam master after kills
