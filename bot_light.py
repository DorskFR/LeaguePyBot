import cv2
import numpy as np
from mss import mss
import time
import win32api, win32con
import pydirectinput
from PIL import Image
import pytesseract
import concurrent.futures

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


client_box = {'left': 320, 'top': 180, 'width': 1280, 'height': 720}
game_box = {'left': 0, 'top': 0, 'width': 1920, 'height': 1080}
start_box = {'left': 1000, 'top': 300, 'width': 600, 'height': 400}
shop_box = {'left': 350, 'top': 130, 'width': 730, 'height': 760}
gold_box = {'left': 1200, 'top': 1045, 'width': 90, 'height': 22}
inventory_box = {'left': 1130, 'top': 940, 'width': 190, 'height': 100}
# legendary_box = {'left': 490, 'top': 750, 'width': 590, 'height': 75}
minimap_box = {'left': 1640, 'top': 800, 'width': 280, 'height': 280}
fight_box = {'left': 150, 'top': 100, 'width': 1770, 'height': 700}
right_fight_box = {'left': 960, 'top': 100, 'width': 960, 'height': 700}
player_box = {'left': 660, 'top': 200, 'width': 600, 'height': 400}
eog_box = {'left': 860, 'top': 600, 'width': 200, 'height': 80}
shop_open_box = {'left': 350, 'top': 775, 'width': 90, 'height': 95}
# life_box = {'left': 820, 'top': 1030, 'width': 200, 'height': 17}
# level_box = {'left': 620, 'top': 1045, 'width': 20, 'height': 15}


ahri_items = [  {'name': 'doranring', 'price': 400, 'bought': False},
                {'name': 'healthpotion', 'price': 50, 'bought': False},
                {'name': 'healthpotion', 'price': 50, 'bought': False},
                {'name': 'ward', 'price': 0, 'bought': False},
                {'name': 'boots', 'price': 300, 'bought': False},
                {'name': 'sorcerershoes', 'price': 800, 'bought': False},
                {'name': 'amplifyingtome', 'price': 435, 'bought': False},
                {'name': 'blightingjewel', 'price': 815, 'bought': False},
                {'name': 'blastingwand', 'price': 850, 'bought': False},
                {'name': 'voidstaff', 'price': 400, 'bought': False},
                {'name': 'amplifyingtome', 'price': 435, 'bought': False},
                {'name': 'oblivionorb', 'price': 365, 'bought': False},
                {'name': 'blastingwand', 'price': 850, 'bought': False},
                {'name': 'morellonomicon', 'price': 850, 'bought': False},
                {'name': 'amplifyingtome', 'price': 435, 'bought': False},
                {'name': 'armguard', 'price': 465, 'bought': False},
                {'name': 'zhonya', 'price': 1600, 'bought': False},
                {'name': 'bansheeveil', 'price': 2500, 'bought': False}]

logfile = "logs/log-"+str(time.time())+".txt"
shop_list = ahri_items
ratio = 1
sct = mss()


def log_timestamp():
    timestamp = "["+time.strftime('%H:%M:%S')+"]"
    return timestamp


def capture_window(bounding_box):
    sct_img = sct.grab(bounding_box)
    width = int(bounding_box['width']/ratio)
    height = int(bounding_box['height']/ratio)
    sct_img = cv2.resize(np.array(sct_img),(width,height))
    return sct_img


def template_match(img_bgr, template_img):
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    template = cv2.imread(template_img, 0)
    name = template_img.split('/')[-1].split('.')[0]

    # w, h = template.shape[::-1]
    width = int(template.shape[1]/ratio)
    height = int(template.shape[0]/ratio)
    template = cv2.resize(template, (width,height))

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.90
    if name == 'minion': threshold = 0.99
    if 'shop' in template_img: threshold = 0.85
    if 'inventory' in template_img: threshold = 0.85
    if name == 'start' or name == 'ward' or 'matchmaking' in name: threshold = 0.80
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

    return int(x), int(y), name, loc, width, height


def lookup(bounding_box, template):
    sct_img = capture_window(bounding_box)
    x, y, *_ = template_match(sct_img, template)
    return x, y


def lookup_thread(bounding_box, template, sct_img):
    x, y, name, loc, width, height = template_match(sct_img, template)
    return x, y, name, loc, width, height


def look_for(bounding_box, template):
    while True:
        x, y = lookup(bounding_box, template)
        if x != 0 and y != 0:
            break
    return int(x+bounding_box['left']), int(y+bounding_box['top'])


def mark_the_spot(sct_img, pt, width, height, name):
    x = 0
    y = 0
    side = None
    if pt[0] != 0 and pt[1] != 0:
        x += int((width * ratio / 2) + pt[0])
        y += int((height * ratio / 2) + pt[1])
        color = tuple(int(x) for x in sct_img[y][x])
        if color[0] > 120: side = "ally"
        elif color[2] > 120: side = "enemy"
        else: side = "neutral"

        if name == 'half' or name == 'low':
            color = tuple(int(x) for x in sct_img[y][pt[0]-25])
            print(f"{log_timestamp()} color for {name} is {color}") #, file=open(logfile, 'a'))
            if color[1] > 100 and color[2] > 100:
                pass
            else:
                x = 0
                y = 0

    return x, y, side


def move_mouse(x, y):
    try:
        win32api.SetCursorPos((x,y))
    except:
        print(f"{log_timestamp()} Couldn't lock mouse, 10s sleep...") #, file=open(logfile, 'a'))
        time.sleep(10)


def left_click(x, y):
    move_mouse(x, y)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(0.3)


def right_click(x, y):
    move_mouse(x, y)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)
    time.sleep(0.3)


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
            print(f"{log_timestamp()} Typing login...") #, file=open(logfile, 'a'))
            keyboard_write("FioraJapan3015")
        elif counter == 2:
            print(f"{log_timestamp()} Typing password...") #, file=open(logfile, 'a'))
            keyboard_write("fiorajapan3015")
        elif counter == 7:
            print(f"{log_timestamp()} Logging in...") #, file=open(logfile, 'a'))
            pydirectinput.press('enter')
            time.sleep(5)
        elif counter == 8:
            print(f"{log_timestamp()} Starting game") #, file=open(logfile, 'a'))
            pydirectinput.press('enter')
            break
        pydirectinput.press('tab')
        counter += 1
    time.sleep(20)


def screen_sequence(path, steps):
    for step in steps:
        left_click(*look_for(client_box, path+step+'.png'))


def go_toplane():
    pydirectinput.keyDown('shift')
    right_click(1675, 890)
    pydirectinput.keyUp('shift')
    print(f"{log_timestamp()} Going toplane...") #, file=open(logfile, 'a'))
    print(f"{log_timestamp()} Sleep 30sc while walking...") #, file=open(logfile, 'a'))
    time.sleep(30)
    farm_lane()


def check_number(box):
    conf = r'--oem 3 --psm 6 outputbase digits'
    sct_img = capture_window(box)
    gray_img = cv2.cvtColor(sct_img, cv2.COLOR_BGR2RGB)
    # gray_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # gray_img = cv2.medianBlur(gray_img, 3)
    pil_image = Image.fromarray(gray_img)
    text = pytesseract.image_to_string(pil_image, config=conf)
    try:
        number = 0
        number += int(text)
    except:
        number = 0
    return number


def buy_item(item):
    while True:
        if lookup(shop_open_box, 'patterns/shop/open.png') == (0,0):
            print(f"{log_timestamp()} Opening shop..") #, file=open(logfile, 'a'))
            pydirectinput.press('p')
        left_click(1280, 155)
        print(f"{log_timestamp()} Buying {item['name']}") #, file=open(logfile, 'a'))
        right_click(*look_for(shop_box, 'patterns/shop/'+item['name']+'.png'))
        left_click(1280, 155)
        if lookup(eog_box, 'patterns/matchmaking/endofgame.png') != (0,0):
            print(f'{log_timestamp()} end of game') #, file=open(logfile, 'a'))
            left_click(960, 640)
            main(postmatch=True)
            break
        elif lookup(inventory_box, 'patterns/inventory/'+item['name']+'.png') != (0,0):
            print(f"{log_timestamp()} Bought {item['name']}") #, file=open(logfile, 'a'))
            item['bought'] = True
            break
        elif lookup(inventory_box, 'patterns/inventory/empty.png') == (0,0):
            print(f"{log_timestamp()} Inventory full") #, file=open(logfile, 'a'))
            break
        elif item['price'] > check_number(gold_box):
            print(f"{log_timestamp()} Insufficient gold for {item['price']}") #, file=open(logfile, 'a'))
            break
        else:
            print(f"{log_timestamp()} Retrying to buy {item['name']}") #, file=open(logfile, 'a'))


def buy_from_shop(items):
    pydirectinput.press('p')
    gold = max(check_number(gold_box), check_number(gold_box), check_number(gold_box))
    time.sleep(0.5)
    for item in items:
        if item['bought'] == True:
            continue
        elif item['bought'] == False and gold > item['price']:
            buy_item(item)
        else:
            print(f"{log_timestamp()} Not enough gold for {item['name']}") #, file=open(logfile, 'a'))
    time.sleep(0.5)
    pydirectinput.press('p')

    go_toplane()


def level_up_abilities():
    pydirectinput.keyUp('shift')
    pydirectinput.keyDown('ctrl')
    pydirectinput.press('r')
    pydirectinput.press('q')
    pydirectinput.press('w')
    pydirectinput.press('e')
    pydirectinput.keyUp('ctrl')
    pydirectinput.keyUp('ctrl')


def back_and_recall():
    pydirectinput.keyUp('shift')
    right_click(1665, 1060)
    pydirectinput.press('f')
    pydirectinput.press('g')
    time.sleep(10) 
    pydirectinput.press('b')
    time.sleep(10)
    buy_from_shop(shop_list)


def fall_back(x=1680, y=890):
    pydirectinput.keyUp('shift')
    right_click(x, y)
    time.sleep(1)
    pydirectinput.press('h')


def attack_position(x, y, nospells=False):
    pydirectinput.keyDown('shift')
    right_click(x+5, y+5)
    right_click(x-5, y-5)
    right_click(x, y)
    pydirectinput.keyUp('shift')
    if nospells == False:
        time.sleep(2)
        pydirectinput.press('r')
        pydirectinput.press('q')
        pydirectinput.press('w')
        pydirectinput.press('e')


def average_tuple_list(tuple_list):
    length = len(tuple_list)
    first = sum(v[0] for v in tuple_list)
    second = sum(v[1] for v in tuple_list)
    average_tuple = (int(first/length), int(second/length))
    print(f"{log_timestamp()} average_tuple: {average_tuple}") #, file=open(logfile, 'a'))
    return average_tuple


def vector_adjust(x1, y1, x2, y2, x3, y3):
    # vector_adjust(*pos_enemy_champion, *pos_safe_player, *pos_player)
    # we want the new coordinates of (x1, y1) after repositioning (x3, y3) to (x2, y2) coordinates.
    dx = x3 - x2
    dy = y3 - y2
    rx = x1 + dx
    ry = y1 + dy

    if rx > 1900 or rx < 100 or ry > 1000 or ry < 100 or x1 == 0 or y1 == 0 or x2 == 0 or y2 == 0: 
        rx = x1
        ry = y1
        return (rx, ry)
    
    print(f"{log_timestamp()} Enemy was at ({x1},{y1})") #, file=open(logfile, 'a'))
    print(f"{log_timestamp()} (x3,y3) - (x2,y2) is ({x3},{y3}) - ({x2},{y2}) and gives (dx,dy) = ({dx},{dy})") #, file=open(logfile, 'a'))
    print(f"{log_timestamp()} new adjusted position ({rx},{ry}) from ({x1},{y1})") #, file=open(logfile, 'a'))

    return (rx, ry)


# average_tuple: (1206, 552)
# pos_median_enemy_minion: (1206, 552) and type: <class 'tuple'>
# end_of_game: False | low_life: False | half_life: False | start_point: False
# pos_player: (919, 389)
# nb_enemy_minion: 5 | pos_enemy_minion: [(1073, 488), (1321, 517), (981, 564), (1369, 590), (1288, 605)] | nb_enemy_champion: 0 | pos_enemy_champion: (0, 0)
# nb_ally_minion: 4 | pos_ally_minion: [(995, 483), (575, 739), (344, 878), (126, 991)] | nb_ally_champion: 0 | pos_ally_champion: (0, 0)
# inferiority or equality or half life or tower
# pos_median_enemy_minion: (1206, 552) and type: <class 'tuple'>
# Enemy was at (1206,552)
# (x3,y3) - (x2,y2) is (919,389) - (76,1041) and gives (dx,dy) = (843,-652)
# new adjusted position (2049,-100) from (1206,552)


def farm_lane():

    patterns = [
                    {'box': player_box, 'pattern': 'patterns/player/low.png'},
                    {'box': start_box, 'pattern': 'patterns/shop/start.png'},
                    {'box': fight_box, 'pattern': 'patterns/unit/minion.png'},
                    {'box': eog_box, 'pattern': 'patterns/matchmaking/endofgame.png'}
                ]

    loop_time = time.time()

    while True:
        
        end_of_game = False
        low_life = False
        start_point = False

        pos_player = (0,0)

        nb_enemy_minion = 0
        pos_enemy_minion = []

        nb_ally_minion = 0
        pos_ally_minion = []

        pos_safer_ally_minion = (960,540)
        pos_riskier_ally_minion = (960,540)
        pos_safe_player = (960,540) #(1675, 890)
        pos_median_enemy_minion = (960,540)

        # level_up_abilities()
        sct_img = capture_window(game_box)

        # Start pattern matching threads
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = [executor.submit(lookup_thread, *(pattern['box'], pattern['pattern'], sct_img)) for pattern in patterns]
            for result in results:
                x, y, name, loc, width, height = result.result()
            # for f in concurrent.futures.as_completed(results):
            #     x, y, name, loc, width, height = f.result()

                for pt in zip(*loc[::-1]):
                    x, y, side = mark_the_spot(sct_img, pt, width, height, name)

                    if (x, y) != (0, 0):
                        pass
                    else:
                        continue

                    if name == 'endofgame': end_of_game = True
                    if name == 'start': start_point = True
                    if name == 'low': low_life = True

                    if name == 'player':
                        pos_player = (x, y)
                    if name == 'minion' and side == 'enemy': 
                        nb_enemy_minion += 1
                        pos_enemy_minion.append((x, y))
                    if name == 'minion' and side == 'ally': 
                        nb_ally_minion += 1
                        pos_ally_minion.append((x, y))


        # Exited the threading

        # Calculating positions
        if nb_ally_minion > 0:
            pos_safer_ally_minion = min(pos_ally_minion,key=lambda item:item[0])
            print(f"{log_timestamp()} pos_safer_ally_minion: {pos_safer_ally_minion}") #, file=open(logfile, 'a'))
            pos_riskier_ally_minion = max(pos_ally_minion,key=lambda item:item[0])
            print(f"{log_timestamp()} pos_riskier_ally_minion: {pos_riskier_ally_minion}") #, file=open(logfile, 'a'))
            pos_safe_player = (max(pos_safer_ally_minion[0]-50, 0), min(pos_safer_ally_minion[1]+50, 1080))
            print(f"{log_timestamp()} pos_safe_player: {pos_safe_player}") #, file=open(logfile, 'a'))
        if nb_enemy_minion > 0:
            pos_median_enemy_minion = average_tuple_list(pos_enemy_minion)
            print(f"{log_timestamp()} pos_median_enemy_minion: {pos_median_enemy_minion} and type: {type(pos_median_enemy_minion)}") #, file=open(logfile, 'a'))

        # Logging
        # print(f"{log_timestamp()} end_of_game: {end_of_game} | low_life: {low_life} | start_point: {start_point}") #, file=open(logfile, 'a'))
        # print(f"{log_timestamp()} pos_player: {pos_player}") #, file=open(logfile, 'a'))
        # print(f"{log_timestamp()} nb_enemy_minion: {nb_enemy_minion} | pos_enemy_minion: {pos_enemy_minion}") #, file=open(logfile, 'a'))
        # print(f"{log_timestamp()} nb_ally_minion: {nb_ally_minion} | pos_ally_minion: {pos_ally_minion}") #, file=open(logfile, 'a'))

        # # Priority conditions
        # if end_of_game:
        #     print(f'{log_timestamp()} end of game') #, file=open(logfile, 'a'))
        #     left_click(960, 640)
        #     main(postmatch=True)
        #     break
        # elif low_life:
        #     print(f'{log_timestamp()} low life') #, file=open(logfile, 'a'))
        #     back_and_recall()
        #     break
        # elif start_point:
        #     print(f'{log_timestamp()} back at the shop') #, file=open(logfile, 'a'))
        #     buy_from_shop(shop_list)
        #     break

        # # fight sequences

        # if nb_enemy_minion > 0:

        #     # no ally minions or tower => fall back # ignore ally champions
        #     if nb_ally_minion == 0:
        #         print(f'{log_timestamp()} falling back') #, file=open(logfile, 'a'))
        #         fall_back()
        #         fall_back()

        #     # inferiority or equality => position behind ally, attack
        #     elif nb_ally_minion > 0:
        #         print(f'{log_timestamp()} inferior or equal or tower or half-life') #, file=open(logfile, 'a'))
        #         fall_back()
        #         attack_position(*pos_median_enemy_minion)

        # # if no enemies follow minions
        # elif nb_enemy_minion == 0 and nb_ally_minion > 0 and (pos_riskier_ally_minion[0] > 960 or pos_riskier_ally_minion[1] < 450):
        #     print(f'{log_timestamp()} follow ally minions') #, file=open(logfile, 'a'))
        #     pydirectinput.keyDown('shift')
        #     right_click(*pos_riskier_ally_minion)
        #     pydirectinput.keyUp('shift')

        # # no one around, might be lost
        # else:
        #     print(f"{log_timestamp()} I feel lost... walking to top tower...") #, file=open(logfile, 'a'))
        #     fall_back()

        print(f'{log_timestamp()} FPS {round(1 /(time.time() - loop_time), 2)}\n') #, file=open(logfile, 'a'))
        loop_time = time.time()


def main(postmatch=False):

    if postmatch:
        time.sleep(5)
        left_click(590,550) #to give GG to someone
        #if lookup(p) ok screen (960, 860)
        # hero_reward (1385, 570)
        for item in shop_list:
            item['bought'] = False
        screen_sequence(path='patterns/matchmaking/', steps=['rematch', 'matchmaking', 'accept'])

    else:
        print(f"{log_timestamp()} Script starting in 5 seconds...")
        time.sleep(3)
        left_click(500,500)
        time.sleep(2)
        login()
        # screen_sequence(path='patterns/matchmaking/', steps=['play', 'ai', 'beginner', 'confirm', 'matchmaking', 'accept'])
        screen_sequence(path='patterns/matchmaking/', steps=['play', 'training', 'practice', 'confirm', 'gamestart'])

    screen_sequence(path='patterns/champselect/', steps=['ahri', 'lock'])
    # if 'ahripicked' == False
    time.sleep(20)
    look_for(game_box, 'patterns/shop/start.png')
    time.sleep(10)
    pydirectinput.press('y')
    time.sleep(5)
    buy_from_shop(shop_list)


if __name__ == '__main__':
    farm_lane()
