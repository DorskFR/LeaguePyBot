import pyautogui
import pydirectinput
import time
import cv2

pyautogui.PAUSE = 0.05
ITEM_CYCLE = [['doranring', 'ward', 'healthpotion', 'healthpotion'], ['boots'], ['bootsupgrade']]
next = 0

print("Script starting in 5sc...")
time.sleep(5)


def keyboard_write(message):
    for letter in message:
        if letter.isupper():
            pydirectinput.keyDown('shift')
            pydirectinput.press(letter.lower())
            pydirectinput.keyUp('shift')
        else:
            pydirectinput.press(letter)


def login():
    pyautogui.click(x=400, y=420, clicks=1, interval=1, button='left')
    counter = 1
    while True:
        if counter == 1:
            print("Typing login...")
            keyboard_write("FioraJapan3015")
        elif counter == 2:
            print("Typing password...")
            keyboard_write("fiorajapan3015")
        elif counter == 7:
            print("Logging in...")
            pydirectinput.press('enter')
            time.sleep(10)
        elif counter == 8:
            print("Starting game")
            pydirectinput.press('enter')
            break
        print(f"Pressing tab...#{counter}")
        pydirectinput.press('tab')
        counter += 1
    #queue_ai_game()
    start_practice_tool()


def queue_ai_game():
    path = 'patterns/matchmaking/'
    screens = ['play', 'ai', 'beginner', 'confirm', 'matchmaking', 'accept']
    for screen in screens:
        try_to_click(path+screen+'.png', True)
    champ_select()


def start_practice_tool():
    path = 'patterns/matchmaking/'
    screens = ['play', 'training', 'practice', 'confirm', 'gamestart']
    for screen in screens:
        try_to_click(path+screen+'.png', True)
    print("Sleep 10s before champ select...")
    time.sleep(10)
    champ_select()


def champ_select():
    path = 'patterns/champselect/'
    champions = ['ahri', 'mf', 'morgana', 'sona']
    picked = False

    for champion in champions:
        if picked:
            break
        if try_to_click(path+champion+'.png'):
            print(f"{champion} was selected!")
            if try_to_click(path+'confirm.png'):
                if try_to_click(path+champion+'picked.png', nb_clicks=0):
                    print(f"{champion} was locked!")
                    picked = True
                else:
                    print(f"Could not lock {champion}")
            else:
                print(f"Could not pick {champion}")

    print("Sleeping 60sc until game loads...")
    time.sleep(60)
    buy_from_shop(ITEM_CYCLE[next])


def buy_from_shop(items):
    global next
    path = 'patterns/shop/'
    if try_to_click('patterns/location/start.png', retry=True, nb_clicks=0):
        print("Game has loaded...I'm at the shop...")
        pydirectinput.press('p')
        for item in items:
            while True:
                try_to_click(path+item+'.png', nb_clicks=1, button='right')
                if try_to_click('patterns/inventory/'+item+'.png', nb_clicks=0):
                    print(f"bought {item}")
                    break
                else:
                    print(f"could not buy {item}, retrying...")
    pydirectinput.press('p')
    print(f"Finished buying items...{items}")
    if next < 2:
        next += 1
    go_toplane()


def go_toplane():
    x, y = 1695, 837
    pyautogui.moveTo(x, y, pyautogui.easeOutQuad)
    pyautogui.click(x, y, 1, interval=1, button='right')
    # pydirectinput.press('enter')
    # keyboard_write('Going toplane')
    # pydirectinput.press('enter')
    print("Going toplane...")
    print("Sleep 30sc while walking...")
    time.sleep(30)
    farm_lane()


def farm_lane():
    path = 'patterns/'
    global next
    while True:
        pydirectinput.keyDown('ctrl')
        pydirectinput.press('r')
        pydirectinput.press('q')
        pydirectinput.press('w')
        pydirectinput.press('e')
        pydirectinput.keyUp('ctrl')
        if try_to_click(path+'enemy/minion.png', nb_clicks=0, button='right', confidence=0.95):
            print("Found minions to attack but do I have allies?...")
            if pyautogui.locateCenterOnScreen(path+'ally/minion.png', grayscale=False, confidence=0.95, region=(960, 0, 960, 1080)):
                print("I have allies on the right part of the screen, let's fight!...")
                pydirectinput.keyDown('shift')
                try_to_click(path+'enemy/minion.png', button='right', confidence=0.95)
                pydirectinput.keyUp('shift')
                print("Casting spells...")
                pydirectinput.press('q')
                pydirectinput.press('w')
                pydirectinput.press('e')
                pydirectinput.press('r')
            else:
                print("No allies found, let's back a bit...")
                pyautogui.moveTo(420, 550, pyautogui.easeOutQuad)
                pyautogui.click(clicks=3, button='right')
        else:
            print("Found no minions to attack...")
            if try_to_click(path+'location/start.png', nb_clicks=0):
                print("I'm back at the shop...")
                buy_from_shop(ITEM_CYCLE[next])
            else:
                if pyautogui.locateCenterOnScreen(path+'ally/minion.png', grayscale=False, confidence=0.95, region=(960, 0, 960, 1080)):
                    print("I have allies on the right part of the screen, let's walk a bit...")
                    pyautogui.moveTo(1300, 500, pyautogui.easeOutQuad)
                    pyautogui.click(clicks=3, button='right')
                else:
                    print("Waiting for allies...")

    # where am I?
        # If I'm back at start point
            # Spend all gold in shop
            # go back to lane
        # If I'm in lane
            # Am I low in health ?
                # Yes = back and recall
            # attack what's in front of me in priority
                # Am I low in mana ?
                    #Yes = back and recall
                # Cast whatever spell is available

def try_to_click(pattern, retry=False, button='left', nb_clicks=1, confidence=.8):
    while True:
        try:
            x, y = pyautogui.locateCenterOnScreen(pattern, grayscale=False, confidence=confidence)
            print(f"found {pattern}")
            print(f"Moving to {x}, {y}")
            pyautogui.moveTo(x, y, pyautogui.easeOutQuad)
            print(f"Clicking {nb_clicks} times")
            pyautogui.click(x, y, clicks=nb_clicks, button=button)
            break
        except TypeError:
            if retry:
                print(f"{pattern} not found retrying in 5sc...")
                time.sleep(5)
            else:
                print(f"{pattern} not found and not retrying")
                return False
    return True

# login()
# queue_ai_game()
start_practice_tool()
# champ_select()
# buy_from_shop(ITEM_CYCLE[next])
# go_toplane()
# farm_lane()

# counter = 0

# while True:
#     counter += 1
#     print(pyautogui.position())
#     image = pyautogui.screenshot()
#     image.save(f'testing{counter}.png')
#     time.sleep(3)

# def lookup(pattern):
#     try:
#         x, y = pyautogui.locateCenterOnScreen(pattern)
#         print(f"found pattern at {x}, {y}")
#     except TypeError:
#         print("Not found, taking a screenshot")
#         image = pyautogui.screenshot()
#         image.save(f"{pattern}win.png")






# pre-match
    # 2642, 686 = accept match
    # 2400, 326 = first champ
    # 2500, 326 = second champ
    # 2637, 733 = ready check

# loading screen
    # 2640, 905 = % loading

# shop
    # 2316, 360 = first item starter
    # 2217, 316 = ward
    # 2216, 261 = potion

# map
    # 3189, 734 = minimap toplane
    # 3253, 808 = minimap midlane
    # 3323, 870 = minimap botlane

# post game
    # 2369, 509 = GG
    # 3039, 528 = choose reward hero
    # 2639, 804 = OK