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
from multiprocessing import Process
from pyWinhook import HookManager
import os
import gc


pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

client_box = {'left': 320, 'top': 180, 'width': 1280, 'height': 720}
game_box = {'left': 0, 'top': 0, 'width': 1920, 'height': 1080}
fight_box = {'left': 300, 'top': 0, 'width': 1620, 'height': 800}
start_box = {'left': 1000, 'top': 300, 'width': 600, 'height': 400}
shop_box = {'left': 350, 'top': 130, 'width': 730, 'height': 760}
shop_open_box = {'left': 350, 'top': 775, 'width': 90, 'height': 95}
shop_consumable_box = {'left': 375, 'top': 195, 'width': 45, 'height': 295}
shop_starter_box = {'left': 505, 'top': 330, 'width': 275, 'height': 60}
shop_boots_box = {'left': 375, 'top': 530, 'width': 45, 'height': 215}
shop_basic_box = {'left': 500, 'top': 440, 'width': 500, 'height': 70}
shop_epic_box = {'left': 500, 'top': 560, 'width': 500, 'height': 145}
shop_legendary_box = {'left': 500, 'top': 750, 'width': 555, 'height': 70}
gold_box = {'left': 1200, 'top': 1045, 'width': 90, 'height': 22}
inventory_box = {'left': 1130, 'top': 940, 'width': 190, 'height': 100}
minimap_box = {'left': 1640, 'top': 800, 'width': 280, 'height': 280}
player_box = {'left': 660, 'top': 200, 'width': 600, 'height': 400}
eog_box = {'left': 860, 'top': 600, 'width': 200, 'height': 80}
client_buttons_box = {'left': 1470, 'top': 162, 'width': 120, 'height': 25}
# life_box = {'left': 820, 'top': 1030, 'width': 200, 'height': 17}
# level_box = {'left': 620, 'top': 1045, 'width': 20, 'height': 15}

ahri_items = [  {'name': 'doranring', 'price': 400, 'bought': False, 'box': shop_starter_box, 'pos': (580,350)},
                {'name': 'healthpotion', 'price': 50, 'bought': False, 'box': shop_consumable_box, 'pos': (400,215)},
                {'name': 'healthpotion', 'price': 50, 'bought': False, 'box': shop_consumable_box, 'pos': (400,215)},
                {'name': 'ward', 'price': 0, 'bought': False, 'box': shop_consumable_box, 'pos': (400,290)},
                {'name': 'amplifyingtome', 'price': 435, 'bought': False, 'box': shop_basic_box, 'pos': (755,465)},
                {'name': 'amplifyingtome', 'price': 435, 'bought': False, 'box': shop_basic_box, 'pos': (755,465)},
                {'name': 'lostchapter', 'price': 430, 'bought': False, 'box': shop_epic_box, 'pos': (530,660)},
                {'name': 'blastingwand', 'price': 850, 'bought': False, 'box': shop_basic_box, 'pos': (925,465)},
                {'name': 'luden', 'price': 1250, 'bought': False, 'box': shop_box, 'pos': (550,400)},
                {'name': 'boots', 'price': 300, 'bought': False, 'box': shop_boots_box, 'pos': (400,550)},
                {'name': 'sorcerershoes', 'price': 800, 'bought': False, 'box': shop_boots_box, 'pos': (400,630)},
                {'name': 'amplifyingtome', 'price': 435, 'bought': False, 'box': shop_basic_box, 'pos': (755,465)},
                {'name': 'blastingwand', 'price': 850, 'bought': False, 'box': shop_basic_box, 'pos': (925,465)},
                {'name': 'akuma', 'price': 1715, 'bought': False, 'box': shop_basic_box, 'pos': (820,775)},
                {'name': 'amplifyingtome', 'price': 435, 'bought': False, 'box': shop_basic_box, 'pos': (755,465)},
                {'name': 'armguard', 'price': 465, 'bought': False, 'box': shop_epic_box, 'pos': (811,580)},
                {'name': 'zhonya', 'price': 1600, 'bought': False, 'box': shop_legendary_box, 'pos': (700,775)},
                {'name': 'bansheeveil', 'price': 2500, 'bought': False, 'box': shop_legendary_box, 'pos': (755,775)}]

logfile = "logs/log-"+str(time.time())+".txt"
shop_list = ahri_items
sct = mss()
ratio = 1


def log_timestamp():
    timestamp = "["+time.strftime('%H:%M:%S')+"]"
    return timestamp


def capture_window(bounding_box):
    sct_img = sct.grab(bounding_box)
    width = int(bounding_box['width']/ratio)
    height = int(bounding_box['height']/ratio)
    sct_img_resized = cv2.resize(np.array(sct_img),(width,height))
    del sct_img
    gc.collect()
    return sct_img_resized


def lookup(bounding_box, template):
    sct_img = capture_window(bounding_box)
    x, y, *_ = template_match(sct_img, template)
    del sct_img
    gc.collect()
    return (x, y)


def lookup_thread(bounding_box, template):
    sct_img = capture_window(bounding_box)
    x, y, name, loc, width, height = template_match(sct_img, template)
    return name, loc, width, height, sct_img, bounding_box['left'], bounding_box['top']


def look_for(bounding_box, template, once=False):
    while True:
        x, y = lookup(bounding_box, template)
        if x != 0 and y != 0:
            break
        if once:
            break
    return int(x+bounding_box['left']), int(y+bounding_box['top'])


def template_match(img_bgr, template_img):
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(template_img, 0)
    name = template_img.split('/')[-1].split('.')[0]
    width = int(template.shape[1]/ratio)
    height = int(template.shape[0]/ratio)
    # template = cv2.resize(template, (width,height))
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.85
    if name == 'minion' or 'lasthit': threshold = 0.99
    if 'tower' in name: threshold = 0.85
    if 'shop' in template_img: threshold = 0.95
    # if 'inventory' in template_img: threshold = 0.85
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
                    print(f"{log_timestamp()} Low life pixel color match {color} at position ({y},{pt[0]-offset}) and offset {offset}...", file=open(logfile, 'a'))
                    yellow_pixels.append(color)
                offset += 1
            if len(yellow_pixels) == 0:
                x = 0
                y = 0

    del sct_img
    gc.collect()

    return x, y, side


def move_mouse(x, y):
    try:
        win32api.SetCursorPos((x,y))
    except:
        print(f"{log_timestamp()} Couldn't lock mouse, 10s sleep...", file=open(logfile, 'a'))
        time.sleep(10)


def left_click(x, y):
    move_mouse(x, y)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(0.1)


def right_click(x, y):
    move_mouse(x, y)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)
    time.sleep(0.1)


def keyboard_write(message):
    for letter in message:
        if letter.isupper():
            pydirectinput.keyDown('shift')
            pydirectinput.press(letter.lower())
            pydirectinput.keyUp('shift')
        else:
            pydirectinput.press(letter)


def login():
    left_click(x=400, y=420)
    counter = 1
    while True:
        if counter == 1:
            print(f"{log_timestamp()} Typing login...", file=open(logfile, 'a'))
            keyboard_write(account_league.login)
        elif counter == 2:
            print(f"{log_timestamp()} Typing password...", file=open(logfile, 'a'))
            keyboard_write(account_league.password)
        elif counter == 7:
            print(f"{log_timestamp()} Logging in...", file=open(logfile, 'a'))
            pydirectinput.press('enter')
            time.sleep(5)
        elif counter == 8:
            print(f"{log_timestamp()} Starting game", file=open(logfile, 'a'))
            pydirectinput.press('enter')
            break
        pydirectinput.press('tab')
        counter += 1
    time.sleep(20)


def screen_sequence(path, steps):
    for step in steps:
        print(f"Next click is {step}", file=open(logfile, 'a'))
        left_click(*look_for(client_box, path+step+'.png'))
        time.sleep(0.1)


def go_toplane():
    pydirectinput.keyDown('shift')
    right_click(1675, 890)
    pydirectinput.keyUp('shift')
    print(f"{log_timestamp()} Going toplane...", file=open(logfile, 'a'))
    print(f"{log_timestamp()} Sleep 25sc while walking...", file=open(logfile, 'a'))
    time.sleep(5)
    if end_of_game() == False:
        time.sleep(10)
    if lookup(player_box, 'patterns/player/player.png') == (0,0) and end_of_game() == False:
        print(f"{log_timestamp()} Can't see player, lock camera", file=open(logfile, 'a'))
        pydirectinput.press('y')
    if end_of_game() == False:
        time.sleep(10)
    farm_lane()


def check_number(box):
    conf = r'--oem 3 --psm 6 outputbase digits'
    sct_img = capture_window(gold_box)
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


def buy_item(item):
    while True:
        if lookup(shop_open_box, 'patterns/shop/open.png') == (0,0):
            print(f"{log_timestamp()} Opening shop..", file=open(logfile, 'a'))
            pydirectinput.press('p')
        left_click(1280, 155)
        print(f"{log_timestamp()} Buying {item['name']}", file=open(logfile, 'a'))
        # right_click(*look_for(item['box'], 'patterns/shop/'+item['name']+'.png',retry=False))
        if item['name'] == 'akuma' or item['name'] == 'luden':
            left_click(545,155)
            time.sleep(0.5)
            right_click(*item['pos'])
            time.sleep(0.5)
            left_click(755,155)
        else:
            right_click(*item['pos'])
        left_click(1280, 155)
        if end_of_game():
            break
        elif lookup(inventory_box, 'patterns/inventory/'+item['name']+'.png') != (0,0):
            print(f"{log_timestamp()} Bought {item['name']}", file=open(logfile, 'a'))
            item['bought'] = True
            break
        elif lookup(inventory_box, 'patterns/inventory/empty.png') == (0,0):
            print(f"{log_timestamp()} Inventory full", file=open(logfile, 'a'))
            break
        elif item['price'] > check_number(gold_box):
            print(f"{log_timestamp()} Insufficient gold for {item['price']}", file=open(logfile, 'a'))
            break
        else:
            print(f"{log_timestamp()} Retrying to buy {item['name']}", file=open(logfile, 'a'))


def buy_from_shop(items):
    time.sleep(2)
    pydirectinput.press('p')
    for item in items:
        if item['bought'] == True:
            continue
        elif item['bought'] == False and check_number(gold_box) >= item['price']:
            buy_item(item)
        else:
            print(f"{log_timestamp()} Not enough gold for {item['name']}", file=open(logfile, 'a'))
            break
    pydirectinput.press('p')
    if end_of_game() == False:
        go_toplane()


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


def back_and_recall():
    pydirectinput.keyUp('shift')
    right_click(1665, 1060)
    pydirectinput.press('f')
    pydirectinput.press('g')
    pydirectinput.press('s')
    time.sleep(10) 
    pydirectinput.press('b')
    time.sleep(10)
    buy_from_shop(shop_list)


def fall_back(x=1680, y=890, timer=0):
    pydirectinput.keyUp('shift')
    pydirectinput.press('s')
    right_click(x, y)
    time.sleep(timer)


def attack_position(x, y, q=False, w=True, e=False, r=False, target_champion=False):
    pydirectinput.keyDown('shift')
    if target_champion: pydirectinput.keyDown('c')
    right_click(x, y)
    if target_champion: pydirectinput.keyUp('c')
    pydirectinput.keyUp('shift')
    if w: pydirectinput.press('w')
    if q: pydirectinput.press('q')
    if e: pydirectinput.press('e')
    if r: pydirectinput.press('r')


def average_tuple_list(tuple_list):
    length = len(tuple_list)
    first = sum(v[0] for v in tuple_list)
    second = sum(v[1] for v in tuple_list)
    average_tuple = (int(first/length), int(second/length))
    print(f"{log_timestamp()} average_tuple: {average_tuple}", file=open(logfile, 'a'))
    return average_tuple


def end_of_game():
    if lookup(eog_box, 'patterns/matchmaking/endofgame.png') != (0,0):
        print(f'{log_timestamp()} Found the end of game button', file=open(logfile, 'a'))
        left_click(960, 640)
        main(postmatch=True)
        return True
    if lookup(client_buttons_box, 'patterns/matchmaking/buttons.png') != (0,0):
        print(f'{log_timestamp()} Found the client interface, game must have ended...', file=open(logfile, 'a'))
        main(postmatch=True)
        return True
    return False


def farm_lane():

    patterns = [
                    {'box': player_box, 'pattern': 'patterns/player/low.png'},
                    {'box': start_box, 'pattern': 'patterns/shop/start.png'},
                    {'box': fight_box, 'pattern': 'patterns/unit/minion.png'},
                    {'box': fight_box, 'pattern': 'patterns/unit/champion.png'},
                    {'box': fight_box, 'pattern': 'patterns/unit/tower.png'},
                    {'box': fight_box, 'pattern': 'patterns/unit/tower2.png'},
                    {'box': eog_box, 'pattern': 'patterns/matchmaking/endofgame.png'}
                ]

    loop_time = time.time()

    while True:
        
        low_life = False
        start_point = False
        nb_enemy_minion = 0
        pos_enemy_minion = []
        nb_enemy_champion = 0
        pos_enemy_champion = (0, 0)
        nb_enemy_tower = 0
        nb_ally_tower = 0
        nb_ally_minion = 0
        pos_ally_minion = []
        pos_safer_ally_minion = (960,540)
        pos_riskier_ally_minion = (960,540)
        pos_safe_player = (960,540) #(1675, 890)
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
            print(f"{log_timestamp()} pos_safer_ally_minion: {pos_safer_ally_minion}", file=open(logfile, 'a'))
            pos_riskier_ally_minion = max(pos_ally_minion,key=lambda item:item[0])
            print(f"{log_timestamp()} pos_riskier_ally_minion: {pos_riskier_ally_minion}", file=open(logfile, 'a'))
            pos_safe_player = (max(pos_safer_ally_minion[0]-50, 0), min(pos_safer_ally_minion[1]+50, 1080))
            print(f"{log_timestamp()} pos_safe_player: {pos_safe_player}", file=open(logfile, 'a'))
        if nb_enemy_minion > 0:
            pos_median_enemy_minion = average_tuple_list(pos_enemy_minion)
            print(f"{log_timestamp()} pos_median_enemy_minion: {pos_median_enemy_minion} and type: {type(pos_median_enemy_minion)}", file=open(logfile, 'a'))

        # Logging
        print(f"{log_timestamp()} low_life: {low_life} | start_point: {start_point}", file=open(logfile, 'a'))
        print(f"{log_timestamp()} nb_enemy_minion: {nb_enemy_minion} | pos_enemy_minion: {pos_enemy_minion}", file=open(logfile, 'a'))
        print(f"{log_timestamp()} nb_enemy_champion: {nb_enemy_champion} | pos_enemy_champion: {pos_enemy_champion}", file=open(logfile, 'a'))
        print(f"{log_timestamp()} nb_enemy_tower: {nb_enemy_tower} | nb_ally_tower: {nb_ally_tower}", file=open(logfile, 'a'))
        print(f"{log_timestamp()} nb_ally_minion: {nb_ally_minion} | pos_ally_minion: {pos_ally_minion}", file=open(logfile, 'a'))

        # Priority conditions
        if end_of_game():
            break
        elif low_life:
            print(f'{log_timestamp()} low life', file=open(logfile, 'a'))
            back_and_recall()
            break
        elif start_point:
            print(f'{log_timestamp()} back at the shop', file=open(logfile, 'a'))
            buy_from_shop(shop_list)
            break

        # fight sequences
        if nb_enemy_minion > 0 or nb_enemy_champion > 0:

            # fall back if no allies or 2- minions + a tower or if tower + champion
            if nb_ally_minion == 0  or (nb_ally_minion <= 2 and nb_enemy_tower > 0) or (nb_enemy_tower > 0 and nb_enemy_champion > 0) or nb_enemy_champion > 3:
                print(f'{log_timestamp()} falling back', file=open(logfile, 'a'))
                fall_back(timer=2)
                attack_position(960, 540)

            # primarily attack champions
            elif nb_enemy_champion > 0:
                print(f'{log_timestamp()} attack enemy champion', file=open(logfile, 'a'))
                if (nb_enemy_minion > nb_ally_minion and nb_ally_tower == 0):
                    fall_back(1)
                attack_position(*pos_enemy_champion, q=True, e=True, r=True, target_champion=True)

            # position behind ally, attack
            else:
                print(f'{log_timestamp()} fight, back if lower numbers', file=open(logfile, 'a'))
                if nb_enemy_minion > nb_ally_minion and nb_ally_tower == 0:
                    fall_back()
                else:
                    attack_position(*pos_median_enemy_minion, q=True)
                

        # if no enemies follow minions
        elif nb_ally_minion > 0 and (pos_riskier_ally_minion[0] > 960 or pos_riskier_ally_minion[1] < 450):
            print(f'{log_timestamp()} follow ally minions', file=open(logfile, 'a'))
            pydirectinput.keyDown('shift')
            right_click(*pos_riskier_ally_minion)
            pydirectinput.keyUp('shift')

        # no one around, might be lost
        else:
            print(f"{log_timestamp()} I feel lost... walking to top tower...", file=open(logfile, 'a'))
            fall_back()

        print(f'{log_timestamp()} FPS {round(1 /(time.time() - loop_time), 2)}\n', file=open(logfile, 'a'))
        loop_time = time.time()


class Keystroke_Watcher(object):
    def __init__(self):
        self.hm = HookManager()
        self.hm.KeyDown = self.on_keyboard_event
        self.hm.HookKeyboard()

    def on_keyboard_event(self, event):
        try:
            if event.KeyID  == 75: #K
                self.stop_script()
        finally:
            return True

    def stop_script(self):
        print(f"{log_timestamp()} Exiting script...", file=open(logfile, 'a'))
        os.system("taskkill /IM python.exe /f") # lol bruteforce

    def shutdown(self):
        win32gui.PostQuitMessage(0)
        self.hm.UnhookKeyboard()


def listen_k():
    watcher = Keystroke_Watcher()
    win32gui.PumpMessages()


def main(postmatch=False):

    if postmatch:
        time.sleep(10)
        left_click(590,550) #to give GG to someone
        time.sleep(5)
        while True:
            if lookup(client_box, 'patterns/matchmaking/ok.png') != (0,0):
                print(f"{log_timestamp()} Found a post end game OK button to click...", file=open(logfile, 'a'))
                pydirectinput.press('space')
            elif lookup(client_box, 'patterns/matchmaking/rematch.png') != (0,0):
                print(f"{log_timestamp()} Found the rematch button to click, exiting loop...", file=open(logfile, 'a'))
                break
            else:
                print(f"{log_timestamp()} Just clicking at 1385, 570...", file=open(logfile, 'a'))
                left_click(1385,570)

        for item in shop_list:
            item['bought'] = False
        screen_sequence(path='patterns/matchmaking/', steps=['rematch', 'matchmaking', 'accept'])

    else:
        print(f"{log_timestamp()} Script starting in 5 seconds...")
        time.sleep(3)
        left_click(500,500)
        time.sleep(2)
        login()
        print(f"{log_timestamp()} Sequence Matchmaking...", file=open(logfile, 'a'))
        screen_sequence(path='patterns/matchmaking/', steps=['play', 'ai', 'beginner', 'confirm', 'matchmaking', 'accept'])
        # screen_sequence(path='patterns/matchmaking/', steps=['play', 'training', 'practice', 'confirm', 'gamestart'])

    while True:
        if lookup(client_box, 'patterns/matchmaking/accept.png') != (0,0):
            left_click(955, 750)
        elif lookup(client_box, 'patterns/champselect/ahri.png') != (0,0):
            print(f"{log_timestamp()} Sequence Champselect...", file=open(logfile, 'a'))
            x, y = look_for(client_box, 'patterns/champselect/ahri.png', once=True)
            if (x, y) != (0, 0):
                left_click(x, y)
        elif lookup(client_box, 'patterns/champselect/lock.png') != (0,0):
            x, y = look_for(client_box, 'patterns/champselect/lock.png', once=True)
            if (x, y) != (0, 0):
                left_click(x, y)
        elif lookup(start_box, 'patterns/shop/start.png') != (0,0):
            print(f"{log_timestamp()} Game has started, shopping in 15sc...", file=open(logfile, 'a'))
            break

    time.sleep(10)
    print(f"{log_timestamp()} Level up E spell", file=open(logfile, 'a'))
    pydirectinput.keyDown('ctrl')
    pydirectinput.press('e')
    pydirectinput.keyUp('ctrl')
    time.sleep(5)
    buy_from_shop(shop_list)


if __name__ == '__main__':
    p = Process(target=listen_k)
    k = Process(target=main)
    p.start()
    k.start()
