import time
import concurrent.futures
import cv2
import numpy as np
from mss import mss
import pyautogui
import win32gui


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
            'patterns/unit/towerattack.png'
            # 'patterns/minimap/ahri.png',
            # 'patterns/minimap/ahri2.png',
            # 'patterns/minimap/ahri3.png',
            # 'patterns/shop/open.png'
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
    threshold = 0.85
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
        # cv2.rectangle(sct_img, pt, (x, y), (0,255,255), 1)
        # color = win32gui.GetPixel(win32gui.GetDC(win32gui.GetActiveWindow()), x, y)
        # color = rgbint2bgrtuple(color)
        color = tuple(int(x) for x in sct_img[y][x])
        # cv2.circle(sct_img, (pt[0], pt[1]), 0, color, 3)
        cv2.circle(sct_img, (pt[0]-25, y), 10, (255,255,0), 3)
        # if color[0] > 120: #blue
        #     cv2.putText(sct_img, name, (pt[0], pt[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,0), 4)
        #     cv2.putText(sct_img, name, (pt[0], pt[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
        # elif color[2] > 120: #red
        #     cv2.putText(sct_img, name, (pt[0], pt[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,0), 4)
        #     cv2.putText(sct_img, name, (pt[0], pt[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (26,13,247), 2)
        # else:
        #     cv2.putText(sct_img, name, (pt[0], pt[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,0), 4)
        #     cv2.putText(sct_img, name, (pt[0], pt[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    print(f"({pt[0]}, {pt[1]}) and center ({x},{y})")

    return sct_img


def main():
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
        time.sleep(1)

        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()

