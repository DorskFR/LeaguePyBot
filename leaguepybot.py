import cv2
import numpy as np
from mss import mss
import time
import win32api, win32con, win32gui
import pydirectinput
from PIL import Image
import pytesseract
import concurrent.futures
import account_league
import threading
from pyWinhook import HookManager
import os
import gc
## PARAMETERS & CONSTANTS

pydirectinput.FAILSAFE = False
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Client
CLIENT_BOX = {'left': 320, 'top': 180, 'width': 1280, 'height': 720}
CLIENT_LOGIN_BOX = {'left': 480, 'top': 200, 'width': 100, 'height': 150}
CLIENT_PLAY_BOX = {'left': 330, 'top': 160, 'width': 200, 'height': 80}
CLIENT_MATCHMAKING_BOX = {'left': 730, 'top': 820, 'width': 250, 'height': 100}
CLIENT_CHAMPSELECT_BOX = {'left': 760, 'top': 230, 'width': 150, 'height': 80}
CLIENT_GGSCREEN_BOX = {'left': 800, 'top': 200, 'width': 300, 'height': 60}
CLIENT_GGNEXT_BOX = {'left': 920, 'top': 780, 'width': 100, 'height': 100}

# In-game
EOG_BOX = {'left': 860, 'top': 600, 'width': 200, 'height': 80}
FIGHT_BOX = {'left': 300, 'top': 0, 'width': 1620, 'height': 800}
START_BOX = {'left': 1000, 'top': 300, 'width': 600, 'height': 400}
SHOP_BOX = {'left': 350, 'top': 130, 'width': 730, 'height': 760}
SHOP_OPEN_BOX = {'left': 350, 'top': 775, 'width': 90, 'height': 95}
SHOP_CONSUMABLE_BOX = {'left': 375, 'top': 195, 'width': 45, 'height': 295}
SHOP_STARTER_BOX = {'left': 505, 'top': 330, 'width': 275, 'height': 60}
SHOP_BOOTS_BOX = {'left': 375, 'top': 530, 'width': 45, 'height': 215}
SHOP_BASIC_BOX = {'left': 500, 'top': 440, 'width': 500, 'height': 70}
SHOP_EPIC_BOX = {'left': 500, 'top': 560, 'width': 500, 'height': 145}
SHOP_LEGENDARY_BOX = {'left': 500, 'top': 750, 'width': 555, 'height': 70}
GOLD_BOX = {'left': 1200, 'top': 1045, 'width': 90, 'height': 22}
INVENTORY_BOX = {'left': 1130, 'top': 940, 'width': 190, 'height': 100}
MINIMAP_BOX = {'left': 1640, 'top': 800, 'width': 280, 'height': 280}
MINIMAP_CORNER_BOX = {'left': 1630, 'top': 790, 'width': 60, 'height': 60}
PLAYER_BOX = {'left': 660, 'top': 200, 'width': 600, 'height': 400}

MELEE_ITEMS = [{'name': 'doranblade', 'price': 450, 'bought': False, 'box': SHOP_STARTER_BOX, 'pos': (695,350)},
                {'name': 'healthpotion', 'price': 50, 'bought': False, 'box': SHOP_CONSUMABLE_BOX, 'pos': (400,215)},
                {'name': 'ward', 'price': 0, 'bought': False, 'box': SHOP_CONSUMABLE_BOX, 'pos': (400,290)},
                {'name': 'longsword', 'price': 350, 'bought': False, 'box': SHOP_BASIC_BOX, 'pos': (640,465)},
                {'name': 'rubycrystal', 'price': 400, 'bought': False, 'box': SHOP_BASIC_BOX, 'pos': (700,465)},
                {'name': 'phage', 'price': 350, 'bought': False, 'box': SHOP_EPIC_BOX, 'pos': (1030,585)},
                {'name': 'sheen', 'price': 700, 'bought': False, 'box': SHOP_EPIC_BOX, 'pos': (530,585)},
                {'name': 'rubycrystal', 'price': 400, 'bought': False, 'box': SHOP_BASIC_BOX, 'pos': (700,465)},
                {'name': 'kindledgem', 'price': 400, 'bought': False, 'box': SHOP_EPIC_BOX, 'pos': (695,585)},
                {'name': 'divine', 'price': 700, 'bought': False, 'box': SHOP_BOX, 'pos': (615,775)},
                {'name': 'boots', 'price': 300, 'bought': False, 'box': SHOP_BOOTS_BOX, 'pos': (400,555)},
                {'name': 'clotharmor', 'price': 300, 'bought': False, 'box': SHOP_BASIC_BOX, 'pos': (530,465)},
                {'name': 'platedboots', 'price': 500, 'bought': False, 'box': SHOP_BOOTS_BOX, 'pos': (400,700)},
                {'name': 'longsword', 'price': 350, 'bought': False, 'box': SHOP_BASIC_BOX, 'pos': (640,465)},
                {'name': 'rubycrystal', 'price': 400, 'bought': False, 'box': SHOP_BASIC_BOX, 'pos': (700,465)},
                {'name': 'phage', 'price': 350, 'bought': False, 'box': SHOP_EPIC_BOX, 'pos': (1030,585)},
                {'name': 'pickaxe', 'price': 875, 'bought': False, 'box': SHOP_BASIC_BOX, 'pos': (865,465)},
                {'name': 'rubycrystal', 'price': 400, 'bought': False, 'box': SHOP_BASIC_BOX, 'pos': (700,465)},
                {'name': 'sterak', 'price': 725, 'bought': False, 'box': SHOP_LEGENDARY_BOX, 'pos': (925,775)},
                {'name': 'pickaxe', 'price': 875, 'bought': False, 'box': SHOP_BASIC_BOX, 'pos': (865,465)},
                {'name': 'tiamat', 'price': 325, 'bought': False, 'box': SHOP_EPIC_BOX, 'pos': (640,655)},
                {'name': 'longsword', 'price': 350, 'bought': False, 'box': SHOP_BASIC_BOX, 'pos': (640,465)},
                {'name': 'vampscepter', 'price': 550, 'bought': False, 'box': SHOP_EPIC_BOX, 'pos': (810,585)},
                {'name': 'ravenous', 'price': 1200, 'bought': False, 'box': SHOP_LEGENDARY_BOX, 'pos': (1035,775)},
                {'name': 'hammer', 'price': 1100, 'bought': False, 'box': SHOP_EPIC_BOX, 'pos': (585,655)},
                {'name': 'deathdance', 'price': 200, 'bought': False, 'box': SHOP_LEGENDARY_BOX, 'pos': (865,775)}]

CASTER_ITEMS = [  {'name': 'doranring', 'price': 400, 'bought': False, 'box': SHOP_STARTER_BOX, 'pos': (695,350)},
                {'name': 'healthpotion', 'price': 50, 'bought': False, 'box': SHOP_CONSUMABLE_BOX, 'pos': (400,215)},
                {'name': 'healthpotion', 'price': 50, 'bought': False, 'box': SHOP_CONSUMABLE_BOX, 'pos': (400,215)},
                {'name': 'ward', 'price': 0, 'bought': False, 'box': SHOP_CONSUMABLE_BOX, 'pos': (400,290)},
                {'name': 'amplifyingtome', 'price': 435, 'bought': False, 'box': SHOP_BASIC_BOX, 'pos': (755,465)},
                {'name': 'amplifyingtome', 'price': 435, 'bought': False, 'box': SHOP_BASIC_BOX, 'pos': (755,465)},
                {'name': 'lostchapter', 'price': 430, 'bought': False, 'box': SHOP_EPIC_BOX, 'pos': (530,660)},
                {'name': 'blastingwand', 'price': 850, 'bought': False, 'box': SHOP_BASIC_BOX, 'pos': (925,465)},
                {'name': 'luden', 'price': 1250, 'bought': False, 'box': SHOP_BOX, 'pos': (550,400)},
                {'name': 'boots', 'price': 300, 'bought': False, 'box': SHOP_BOOTS_BOX, 'pos': (400,550)},
                {'name': 'sorcerershoes', 'price': 800, 'bought': False, 'box': SHOP_BOOTS_BOX, 'pos': (400,630)},
                {'name': 'amplifyingtome', 'price': 435, 'bought': False, 'box': SHOP_BASIC_BOX, 'pos': (755,465)},
                {'name': 'blastingwand', 'price': 850, 'bought': False, 'box': SHOP_BASIC_BOX, 'pos': (925,465)},
                {'name': 'akuma', 'price': 1715, 'bought': False, 'box': SHOP_BOX, 'pos': (550,775)},
                {'name': 'amplifyingtome', 'price': 435, 'bought': False, 'box': SHOP_BASIC_BOX, 'pos': (755,465)},
                {'name': 'armguard', 'price': 465, 'bought': False, 'box': SHOP_EPIC_BOX, 'pos': (811,580)},
                {'name': 'zhonya', 'price': 1600, 'bought': False, 'box': SHOP_LEGENDARY_BOX, 'pos': (700,775)},
                {'name': 'bansheeveil', 'price': 2500, 'bought': False, 'box': SHOP_LEGENDARY_BOX, 'pos': (755,775)}]


# Global variables

shop_list = MELEE_ITEMS
pick_rotation = ['jax', 'illaoi', 'ahri']
current_screen = 'unknown'
last_screen = 'unknown'
game_state = 'start'
sct = mss()
ratio = 1

## LOGGING


class Logger():
    def __init__(self, debug=False):
        self.create_log_folder()
        self.logfile = "logs/log-"+str(time.time())+".txt"
        self.debug = debug

    def create_log_folder(self):
        if not os.path.exists('logs'):
            os.makedirs('logs')

    def log_timestamp(self):
        timestamp = "["+time.strftime('%H:%M:%S')+"]"
        return timestamp

    def plog(self, message):
        if self.debug:
            print(f"{self.log_timestamp()} {message}")
        print(f"{self.log_timestamp()} {message}", file=open(self.logfile, 'a'))


## MOUSE AND KEYBOARD

# Move the mouse to coordinates
def move_mouse(x, y):
    try:
        win32api.SetCursorPos((x,y))
    except:
        logger.plog(f"Couldn't lock mouse, 10s sleep...")
        time.sleep(10)

# Left click
def left_click(x, y):
    move_mouse(x, y)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(0.1)

# Right click
def right_click(x, y):
    move_mouse(x, y)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)
    time.sleep(0.1)

# Write chars one by one
def keyboard_write(message):
    for letter in message:
        if letter.isupper():
            pydirectinput.keyDown('shift')
            pydirectinput.press(letter.lower())
            pydirectinput.keyUp('shift')
        else:
            pydirectinput.press(letter)

# Global hotkey class to quit the script ('k')
class Keystroke_Watcher(object):
    def __init__(self):
        self.hm = HookManager()
        self.hm.KeyDown = self.on_keyboard_event
        self.hm.HookKeyboard()

    def on_keyboard_event(self, event):
        try:
            if event.KeyID  == 75: #k
                self.stop_script()
        finally:
            return True

    def stop_script(self):
        logger.plog(f"Exiting script...")
        os.system("taskkill /IM python.exe /f") # lol bruteforce

    def shutdown(self):
        win32gui.PostQuitMessage(0)
        self.hm.UnhookKeyboard()

# Object listening to global hotkey
def listen_k():
    watcher = Keystroke_Watcher()
    win32gui.PumpMessages()


## VISION

# Screenshots
def capture_window(bounding_box):
    sct_img = sct.grab(bounding_box)
    width = int(bounding_box['width']/ratio)
    height = int(bounding_box['height']/ratio)
    sct_img_resized = cv2.resize(np.array(sct_img),(width,height))
    del sct_img
    gc.collect()
    return sct_img_resized

# Lookup and return x, y coordinates
def lookup(bounding_box, template):
    sct_img = capture_window(bounding_box)
    x, y, *_ = template_match(sct_img, template)
    del sct_img
    gc.collect()
    return (x, y)

# Lookup specific to the multithread loop inside farm_lane
def lookup_thread(bounding_box, template):
    sct_img = capture_window(bounding_box)
    x, y, name, loc, width, height = template_match(sct_img, template)
    return name, loc, width, height, sct_img, bounding_box['left'], bounding_box['top']

# Infinite loop to look for a pattern until found
def look_for(bounding_box, template, retries=0):
    while True:
        retries -= 1 # an initial value of 0 means infinite loop
        x, y = lookup(bounding_box, template)
        if x != 0 and y != 0:
            break
        if retries == 0:
            break

    return int(x+bounding_box['left']), int(y+bounding_box['top'])

# Matching template to the screenshot taken
def template_match(img_bgr, template_img):
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(template_img, 0)
    name = template_img.split('/')[-1].split('.')[0]
    width = int(template.shape[1]/ratio)
    height = int(template.shape[0]/ratio)
    # template = cv2.resize(template, (width,height))
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.90
    if name == 'minion': threshold = 0.99
    if 'tower' in name: threshold = 0.85
    if 'shop' in template_img: threshold = 0.95
    if 'inventory' in template_img: threshold = 0.85
    if name == 'start' or name == 'ward': threshold = 0.80
    loc = np.where(res > threshold)
    x = 0
    y = 0
    for pt in zip(*loc[::-1]):
        x += pt[0]
        y += pt[1]
        break
    if x != 0 and y != 0:
        x += width * ratio / 2
        y += height * ratio / 2

    del img_bgr
    del img_gray
    del template
    del res
    gc.collect()
    
    return int(x), int(y), name, loc, width, height

# Pixel color on a match to understand if ally (blue), enemy (red) or self (yellow)
def mark_the_spot(sct_img, pt, width, height, name):
    x = 0
    y = 0
    side = None
    if pt[0] != 0 and pt[1] != 0:
        x += int((width * ratio / 2) + pt[0])
        y += int((height * ratio / 2) + pt[1])
        color = tuple(int(x) for x in sct_img[y][x])
        if color[0] > 120 and color[2] < 120: side = "ally"
        elif color[2] > 120 and color[0] < 120: side = "enemy"
        else: side = "neutral"
        if name == 'low':
            offset = 0
            yellow_pixels = []
            while offset < 25:
                color = tuple(int(x) for x in sct_img[y][pt[0]-offset])
                if color[0] < 100 and color[1] > 150 and color[2] > 150:
                    logger.plog(f"Low life pixel color match {color} at position ({y},{pt[0]-offset}) and offset {offset}...")
                    yellow_pixels.append(color)
                offset += 1
            if len(yellow_pixels) == 0:
                x = 0
                y = 0

    del sct_img
    gc.collect()

    return x, y, side

# Watch the screen and update the current_screen global variable with the latest perceived screen
def screen_watcher():
    global current_screen
    global last_screen

    while True:
        if current_screen != 'unknown':
            if current_screen != last_screen: logger.plog(f"Current screen is: {current_screen}, last screen is {last_screen}") #)
            last_screen = current_screen
        if lookup(CLIENT_LOGIN_BOX, 'patterns/client/login.png') != (0,0):
            current_screen = 'login'
        elif lookup(CLIENT_PLAY_BOX, 'patterns/client/play.png') != (0,0):
            current_screen = 'play'
        elif lookup(CLIENT_MATCHMAKING_BOX, 'patterns/client/matchmaking.png') != (0,0):
            current_screen = 'matchmaking'
        elif lookup(CLIENT_CHAMPSELECT_BOX, 'patterns/client/champselect.png') != (0,0):
            current_screen = 'champselect'
        elif lookup(MINIMAP_CORNER_BOX, 'patterns/minimap/corner.png') != (0,0):
            current_screen = 'ingame'
        elif lookup(EOG_BOX, 'patterns/client/endofgame.png') != (0,0):
            current_screen = 'endofgame'
        elif lookup(CLIENT_GGSCREEN_BOX, 'patterns/client/ggscreen.png') != (0,0):
            current_screen = 'postmatch'
        else:
            current_screen = 'unknown'


## CLIENT MENU

# Login sequence
def login():
    left_click(x=400, y=420)
    counter = 1
    while True:
        if counter == 1:
            logger.plog(f"Typing login...")
            keyboard_write(account_league.login)
        elif counter == 2:
            logger.plog(f"Typing password...")
            keyboard_write(account_league.password)
        elif counter == 7:
            logger.plog(f"Logging in...")
            pydirectinput.press('enter')
            time.sleep(5)
        elif counter == 8:
            logger.plog(f"Starting game")
            pydirectinput.press('enter')
            break
        pydirectinput.press('tab')
        counter += 1

# Click sequence for menus
def screen_sequence(path, steps):
    for step in steps:
        logger.plog(f"Next click is {step}")
        left_click(*look_for(CLIENT_BOX, path+step+'.png'))
        time.sleep(0.1)
        left_click(1070,710) # Accept key fragment reward
        time.sleep(0.1)

# Click the menus to go to the correct matchmaking
def play(practice=False):
    if practice: screen_sequence(path='patterns/client/', steps=['play', 'training', 'practice', 'confirm', 'gamestart'])
    else: screen_sequence(path='patterns/client/', steps=['play', 'ai', 'beginner', 'confirm'])

# Queue for matchmaking and pick a champ
def matchup():
    global shop_list
    global game_state

    while True:

        if current_screen == 'matchmaking':
            left_click(*look_for(CLIENT_BOX, 'patterns/client/matchmaking.png', retries=1))

        if lookup(CLIENT_BOX, 'patterns/client/accept.png') != (0,0):
            logger.plog(f" Found accept!...")
            left_click(955, 750)

        elif lookup(CLIENT_BOX, 'patterns/client/pickerror.png') != (0,0):
            logger.plog(f" Found pickerror!...")
            left_click(960, 550)

        elif current_screen == 'champselect':
            logger.plog(f"Sequence Champselect...")
            for pick in pick_rotation:
                logger.plog(f"Looking for patterns/champselect/{pick}.png...")
                x, y = look_for(CLIENT_BOX, 'patterns/champselect/' + pick + '.png', retries=1)
                if (x, y) != (0, 0): left_click(x, y)
                time.sleep(0.1)
                x, y = look_for(CLIENT_BOX, 'patterns/client/lock.png', retries=1)
                if (x, y) != (0, 0): left_click(x, y)
                time.sleep(0.1)

        elif lookup(CLIENT_BOX, 'patterns/champselect/illaoipicked.png') != (0,0):
            logger.plog(f"Locked Illaoi...")
            shop_list = MELEE_ITEMS

        elif lookup(CLIENT_BOX, 'patterns/champselect/jaxpicked.png') != (0,0):
            logger.plog(f"Locked Jax...")
            shop_list = MELEE_ITEMS

        elif lookup(CLIENT_BOX, 'patterns/champselect/ahripicked.png') != (0,0):
            logger.plog(f"Locked Ahri...")
            shop_list = CASTER_ITEMS

        elif last_screen == 'ingame':
            logger.plog(f"Game has started...")
            game_state = 'start'
            break

# Postmatch and rematch
def postmatch():
    global shop_list
    global game_state

    for item in shop_list:
        item['bought'] = False
    
    game_state = 'stop'

    time.sleep(5)

    while True:
        if lookup(CLIENT_GGNEXT_BOX, 'patterns/client/ggnext.png') != (0,0):
            logger.plog(f"GG someone...")
            left_click(590,550)
        elif lookup(CLIENT_BOX, 'patterns/client/ok.png') != (0,0):
            logger.plog(f"Found a post end game OK button to click...")
            pydirectinput.press('space')
        elif lookup(CLIENT_BOX, 'patterns/client/rematch.png') != (0,0):
            logger.plog(f"Found the rematch button to click, exiting loop...")
            left_click(765,855)
            break
        else: # Lazy method to pick a champ reward
            logger.plog(f"Just clicking at 1385, 570...")
            left_click(1385,570)
        time.sleep(1)

## GAMEPLAY

# Run on game start to level 3rd spell and to start shopping only after 15sc
def game_start():
    time.sleep(10)
    logger.plog(f"Level up E spell")
    pydirectinput.keyDown('ctrl')
    pydirectinput.press('e')
    pydirectinput.keyUp('ctrl')
    time.sleep(5)
    if last_screen == 'ingame':
        buy_from_shop(shop_list)

# OCR to read the gold
def check_number(box):
    conf = r'--oem 3 --psm 6 outputbase digits'
    sct_img = capture_window(GOLD_BOX)
    sct_img = cv2.cvtColor(sct_img, cv2.COLOR_BGR2GRAY)
    sct_img = 0 - sct_img
    ksize = (3,3)
    sct_img = cv2.blur(sct_img, ksize)
    sct_img[sct_img < 100] = 0
    sct_img[sct_img > 200] = 255
    pil_img = Image.fromarray(cv2.cvtColor(sct_img, cv2.COLOR_BGR2RGB))
    text = pytesseract.image_to_string(pil_img, config=conf)
    try:
        number = 0
        number += int(text)
    except:
        number = 0
    return number

# Loop to buy a list of items from shop
def buy_from_shop(items):
    time.sleep(2)
    pydirectinput.press('p')
    for item in items:
        if item['bought'] == True:
            continue
        elif item['bought'] == False and check_number(GOLD_BOX) >= item['price']:
            buy_item(item)
        else:
            logger.plog(f"Not enough gold for {item['name']}")
            break
    pydirectinput.press('p')
    if last_screen == 'ingame':
        go_toplane()

# Buy one item from shop
def buy_item(item):
    retries = 3
    while retries > 0:
        if lookup(SHOP_OPEN_BOX, 'patterns/shop/open.png') == (0,0):
            logger.plog(f"Opening shop..")
            pydirectinput.press('p')
        left_click(755,155)
        logger.plog(f"Buying {item['name']}")
        if item['name'] in ['akuma', 'luden', 'divine']:
            left_click(545,155)
            time.sleep(0.5)
            right_click(*look_for(SHOP_BOX, 'patterns/shop/' + item['name'] + '.png", retries=1))
            time.sleep(0.5)
        else:
            right_click(*item['pos'])
        left_click(755,155)
        if last_screen != 'ingame':
            break
        elif lookup(INVENTORY_BOX, 'patterns/inventory/'+item['name']+'.png') != (0,0):
            logger.plog(f"Bought {item['name']}")
            item['bought'] = True
            break
        elif lookup(INVENTORY_BOX, 'patterns/inventory/empty.png') == (0,0):
            logger.plog(f"Inventory full")
            break
        elif item['price'] > check_number(GOLD_BOX):
            logger.plog(f"Insufficient gold for {item['price']}")
            break
        else:
            logger.plog(f"Retrying to buy {item['name']} {retries} more time")
            retries -= 1

# Go back to lane, check if camera lock is on
def go_toplane():
    pydirectinput.keyDown('shift')
    right_click(1675, 890)
    pydirectinput.keyUp('shift')
    logger.plog(f"Going toplane...")
    logger.plog(f"Sleep 25sc while walking...")
    time.sleep(15)
    if lookup(PLAYER_BOX, 'patterns/unit/player.png') == (0,0) and last_screen == 'ingame':
        logger.plog(f"Can't see player, lock camera")
        pydirectinput.press('y')
    time.sleep(10)
    if last_screen == 'ingame':
        farm_lane()

# Level up abilities at the beginning of each farm_lane cycle
def level_up_abilities():
    pydirectinput.keyUp('shift')
    pydirectinput.keyDown('ctrl')
    pydirectinput.press('r')
    time.sleep(0.1)
    pydirectinput.press('w')
    time.sleep(0.1)
    pydirectinput.press('q')
    time.sleep(0.1)
    pydirectinput.press('e')
    pydirectinput.keyUp('ctrl')
    pydirectinput.keyUp('ctrl')

# Go back to base and shop
def back_and_recall():
    pydirectinput.keyUp('shift')
    pydirectinput.press('f')
    pydirectinput.press('g')
    pydirectinput.press('s')
    right_click(1665, 1060)
    time.sleep(10) 
    pydirectinput.press('b')
    time.sleep(10)
    buy_from_shop(shop_list)

# Retreat
def fall_back(x=1680, y=890, timer=0):
    pydirectinput.keyUp('shift')
    pydirectinput.press('s')
    right_click(x, y)
    time.sleep(timer)

# Attack
def attack_position(x, y, q=False, w=True, e=False, r=False, target_champion=False, spelltarget=(0,0)):
    pydirectinput.keyDown('shift')
    if target_champion: pydirectinput.keyDown('c')
    right_click(x, y)
    if target_champion: pydirectinput.keyUp('c')
    pydirectinput.keyUp('shift')
    if spelltarget == (0,0): spelltarget = (x, y)
    left_click(spelltarget[0], spelltarget[1])
    if e: pydirectinput.press('e')
    if r: pydirectinput.press('r')
    if w: pydirectinput.press('w')
    if q: pydirectinput.press('q')


# Needed to calculate the average position of a group of units
def average_tuple_list(tuple_list):
    length = len(tuple_list)
    first = sum(v[0] for v in tuple_list)
    second = sum(v[1] for v in tuple_list)
    average_tuple = (int(first/length), int(second/length))
    logger.plog(f"average_tuple: {average_tuple}")
    return average_tuple

# What to do when game ends
def end_of_game():
    logger.plog(f'End of game button')
    time.sleep(1)
    left_click(960, 640)

# Main loop to look for patterns and decide how to fight
def farm_lane():

    patterns = [{'box': PLAYER_BOX, 'pattern': 'patterns/unit/low.png'},
                {'box': START_BOX, 'pattern': 'patterns/shop/start.png'},
                {'box': FIGHT_BOX, 'pattern': 'patterns/unit/minion.png'},
                {'box': FIGHT_BOX, 'pattern': 'patterns/unit/champion.png'},
                {'box': FIGHT_BOX, 'pattern': 'patterns/unit/tower.png'},
                {'box': FIGHT_BOX, 'pattern': 'patterns/unit/tower2.png'}]

    loop_time = time.time()

    while True:
        
        low_life = False
        start_point = False
        nb_enemy_minion = 0
        pos_enemy_minion = []
        pos_closest_enemy_minion = (960,540)
        nb_enemy_champion = 0
        pos_enemy_champion = (0, 0)
        nb_enemy_tower = 0
        nb_ally_tower = 0
        nb_ally_minion = 0
        pos_ally_minion = []
        pos_safer_ally_minion = (960,540)
        pos_riskier_ally_minion = (960,540)
        pos_safe_player = (960,540)
        pos_median_enemy_minion = (960,540)

        level_up_abilities()

        # Start pattern matching threads
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = [executor.submit(lookup_thread, *(pattern['box'], pattern['pattern'])) for pattern in patterns]
            for f in concurrent.futures.as_completed(results):
                name, loc, width, height, sct_img, left, top = f.result()

                for pt in zip(*loc[::-1]):
                    x, y, side = mark_the_spot(sct_img, pt, width, height, name)

                    if (x, y) != (0, 0):
                        x = x + left
                        y = y + top
                        pass
                    else:
                        continue

                    if name == 'start': start_point = True
                    if name == 'low': low_life = True
                    if name == 'minion' and side == 'enemy': 
                        nb_enemy_minion += 1
                        pos_enemy_minion.append((x, y))
                    if name == 'champion' and side == 'enemy':
                        nb_enemy_champion += 1
                        pos_enemy_champion = (x, y)
                    if 'tower' in name and side == 'enemy':
                        nb_enemy_tower += 1
                    if 'tower' in name and side == 'ally':
                        nb_ally_tower += 1
                    if name == 'minion' and side == 'ally': 
                        nb_ally_minion += 1
                        pos_ally_minion.append((x, y))

                del sct_img
                del loc
                gc.collect()

        # Calculating positions
        if nb_ally_minion > 0:
            pos_safer_ally_minion = min(pos_ally_minion,key=lambda item:item[0])
            logger.plog(f"pos_safer_ally_minion: {pos_safer_ally_minion}")
            # pos_riskier_ally_minion = max(pos_ally_minion,key=lambda item:item[0])
            risky_minions = []
            for pos_one_ally in pos_ally_minion:
                pos_x = int((pos_one_ally[0] / 1920)*100)
                pos_y = 100 - int((pos_one_ally[1] / 1080)*100)
                risky_minions.append(int((pos_x + pos_y) / 2))
            # max(enumerate(a), key=lambda x: x[1])[0]
            pos_riskier_ally_minion = pos_ally_minion[risky_minions.index(max(risky_minions))]
            logger.plog(f"pos_riskier_ally_minion: {pos_riskier_ally_minion}")
            pos_safe_player = (max(pos_safer_ally_minion[0]-50, 0), min(pos_safer_ally_minion[1]+50, 1080))
            logger.plog(f"pos_safe_player: {pos_safe_player}")
        if nb_enemy_minion > 0:
            pos_closest_enemy_minion = min(pos_enemy_minion,key=lambda item:item[0])
            pos_median_enemy_minion = average_tuple_list(pos_enemy_minion)
            logger.plog(f"pos_median_enemy_minion: {pos_median_enemy_minion} and type: {type(pos_median_enemy_minion)}")

        # Logging
        logger.plog(f"low_life: {low_life} | start_point: {start_point}")
        logger.plog(f"nb_enemy_minion: {nb_enemy_minion} | pos_enemy_minion: {pos_enemy_minion}")
        logger.plog(f"nb_enemy_champion: {nb_enemy_champion} | pos_enemy_champion: {pos_enemy_champion}")
        logger.plog(f"nb_enemy_tower: {nb_enemy_tower} | nb_ally_tower: {nb_ally_tower}")
        logger.plog(f"nb_ally_minion: {nb_ally_minion} | pos_ally_minion: {pos_ally_minion}")

        # Priority conditions
        if current_screen == 'endofgame':
            end_of_game()
            break
        elif last_screen != 'ingame':
            break
        elif low_life:
            logger.plog(f"low life")
            back_and_recall()
            break
        elif start_point:
            logger.plog(f"back at the shop")
            buy_from_shop(shop_list)
            break

        # fight sequences
        if nb_enemy_minion > 0 or nb_enemy_champion > 0:

            # fall back if no allies or 2- minions + a tower or if tower + champion or too many enemies
            # if nb_ally_minion == 0  or (nb_ally_minion <= 2 and nb_enemy_tower > 0) or (nb_enemy_tower > 0 and nb_enemy_champion > 0) or nb_enemy_champion > 3: # more aggressive
            if nb_ally_minion == 0  or (nb_ally_minion <= 5 and nb_enemy_tower > 0) or (nb_enemy_tower > 0 and nb_enemy_champion > 0) or nb_enemy_champion > 2: # more defensive
                logger.plog(f"falling back")
                fall_back(timer=2)
                attack_position(960, 540)

            # primarily attack champions
            elif nb_enemy_champion > 0:
                logger.plog(f"attack enemy champion")
                if (nb_enemy_minion > nb_ally_minion and nb_ally_tower == 0):
                    fall_back(1)
                attack_position(*pos_enemy_champion, q=True, e=True, r=True, target_champion=True)

            # normal attack sequence
            else:
                logger.plog(f"fight, back if lower numbers")
                if nb_enemy_minion > nb_ally_minion and nb_ally_tower == 0:
                    fall_back()
                attack_position(*pos_closest_enemy_minion, spelltarget=pos_median_enemy_minion, q=True)

        # if no enemies follow minions
        elif nb_ally_minion > 0 and (pos_riskier_ally_minion[0] > 960 or pos_riskier_ally_minion[1] < 450):
            logger.plog(f"follow ally minions")
            pydirectinput.keyDown('shift')
            right_click(*pos_riskier_ally_minion)
            pydirectinput.keyUp('shift')

        # no one around, might be lost go back to lane tower
        else:
            logger.plog(f"I feel lost... walking to top tower...")
            fall_back()

        logger.plog(f"FPS {round(1 /(time.time() - loop_time), 2)}\n")
        loop_time = time.time()


# Main program loop
def main():
    logger.plog(f"Main script starting in 5 seconds...")
    time.sleep(5)
    global game_state

    while True:
        if current_screen == 'login': login()
        if current_screen == 'play': play()
        if current_screen == 'matchmaking': matchup()
        if current_screen == 'champselect': matchup()
        if current_screen == 'ingame' and game_state == 'start': 
            game_start()
            game_state = 'playing'
        if current_screen == 'postmatch': postmatch()


# Start the program and different threads
if __name__ == '__main__':
    logger = Logger(debug=True)
    threads = []
    threads.append(threading.Thread(target=listen_k))
    threads.append(threading.Thread(target=main))
    threads.append(threading.Thread(target=screen_watcher))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()