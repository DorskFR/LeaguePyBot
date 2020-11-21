import time
import concurrent.futures
import cv2
import numpy as np
from mss import mss
import pyautogui
import win32gui
from multiprocessing import Process
import sys


# bounding_box ={'left': 350, 'top': 775, 'width': 90, 'height': 95}
bounding_box ={'left': 0, 'top': 0, 'width': 1920, 'height': 1080}
ratio = 1
sct = mss()
patterns = [
            # 'patterns/unit/champion.png',
            # 'patterns/unit/tower.png',
            # 'patterns/unit/tower2.png',
            # 'patterns/unit/building.png',
            # 'patterns/unit/minion.png',
            # 'patterns/player/player.png',
            # 'patterns/player/half.png',
            # 'patterns/player/low.png',
            # 'patterns/unit/towerattack.png'
            # 'patterns/minimap/ahri.png',
            # 'patterns/minimap/ahri2.png',
            # 'patterns/minimap/ahri3.png',
            # 'patterns/shop/start.png',
            # 'patterns/shop/open.png',
            # 'patterns/shop/blightingjewel.png'
            'patterns/matchmaking/ok.png'
            ]


def capture_window():
    sct_img = sct.grab(bounding_box)
    width = int(bounding_box['width']/ratio)
    height = int(bounding_box['height']/ratio)
    sct_img = cv2.resize(np.array(sct_img),(width,height))
    return sct_img


def template_match(img_bgr, pattern):
    img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(pattern, 0)
    name = pattern.split('/')[-1].split('.')[0]
    width = int(template.shape[1]/ratio)
    height = int(template.shape[0]/ratio)
    template = cv2.resize(template, (width,height))
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.90
    if name == 'minion': threshold = 0.99
    # if name == 'start': threshold = 0.80
    loc = np.where(res > threshold)
    return loc, width, height, name


def rgbint2bgrtuple(RGBint):
    red = RGBint & 255
    green = (RGBint >> 8) & 255
    blue = (RGBint >> 16) & 255
    return (blue, green, red)


def mark_the_spot(sct_img, pt, width, height, name):
    x = 0
    y = 0

    if pt[0] != 0 and pt[1] != 0:
        x += int((width * ratio / 2) + pt[0])
        y += int((height * ratio / 2) + pt[1])
        color = tuple(int(x) for x in sct_img[y][x])
        cv2.circle(sct_img, (pt[0], y), 10, (255,255,0), 3)
        # if color[0] > 120: #blue
        # elif color[2] > 120: #red
        if name == 'low':
            offset = 0
            yellow_pixels = []
            while offset < 25:
                color = tuple(int(x) for x in sct_img[y][pt[0]-offset])
                if color[1] > 100 and color[2] > 100:
                    yellow_pixels.append(color)
                offset += 1
            if len(yellow_pixels) > 0:
                print(f"I am low on life at offset {offset}, pt[0] is {pt[0]} color: {yellow_pixels}")
            else:
                x = 0
                y = 0

    # print(f"({pt[0]}, {pt[1]}) and center ({x},{y})")

    return sct_img


def main():
    p = Process(target=listen_k)
    p.start()
    p.join()
    loop_time = time.time()

    while True:
        sct_img = capture_window()
        pos_minion_list = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = [executor.submit(template_match, *(sct_img, pattern)) for pattern in patterns]
            for f in concurrent.futures.as_completed(results):
                loc, width, height, name = f.result()
                counter = 0
                for pt in zip(*loc[::-1]):
                    sct_img = mark_the_spot(sct_img, pt, width, height, name)
                    counter += 1
                    if name == 'minion':
                        pos_minion_list.append(pt)

                print(f"{counter} elts for {name}")
        
        print(f"minions position : {pos_minion_list}")
        # pos_safer_minion = min(pos_minion_list,key=lambda item:item[0])
        # pos_safe_player = (pos_safer_minion[0]-50, pos_safer_minion[1]+50) 
        # pos_danger_minion = max(pos_minion_list,key=lambda item:item[0])
        # print(f"safer: {pos_safer_minion}, danger: {pos_danger_minion}")

        # sct_img = cv2.resize(np.array(sct_img),(960,540))
        cv2.imshow('screen', sct_img)


        print('FPS {}'.format(round(1 / (time.time() - loop_time), 2)))
        loop_time = time.time()

        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break


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
        print(f'Exiting script...') #, file=open(logfile, 'a'))
        sys.exit("User has requested to exit the script")

    def shutdown(self):
        PostQuitMessage(0)
        self.hm.UnhookKeyboard()


def listen_k():
    watcher = Keystroke_Watcher()
    PumpMessages()


if __name__ == '__main__':
    main()

