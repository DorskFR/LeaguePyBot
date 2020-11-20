import time
import cv2
import numpy as np
from mss import mss


bounding_box ={'left': 0, 'top': 0, 'width': 1920, 'height': 1080}
ratio = 1
sct = mss()


def capture_window():
    sct_img = sct.grab(bounding_box)
    width = int(bounding_box['width']/ratio)
    height = int(bounding_box['height']/ratio)
    sct_img = cv2.resize(np.array(sct_img),(width,height))
    return sct_img
    

def template_match(img, pattern):
    # img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(pattern)
    template = template[:,:,0]
    # template = mono_colorize(template)
    # template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    name = pattern.split('/')[-1].split('.')[0]
    width = int(template.shape[1]/ratio)
    height = int(template.shape[0]/ratio)
    template = cv2.resize(template, (width,height))
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.95
    # if name == 'minion': threshold = 0.99
    loc = np.where(res > threshold)
    return loc, width, height, name


def mark_the_spot(sct_img, pt, width, height, name):
    x = 0
    y = 0
    zeros = np.zeros(sct_img.shape, np.uint8)
    sct_img = sct_img + zeros + zeros

    if pt[0] != 0 and pt[1] != 0:
        x += int((width * ratio / 2) + pt[0])
        y += int((height * ratio / 2) + pt[1])
        # color = tuple(int(x) for x in sct_img[y][x])
        cv2.circle(sct_img, (pt[0]-25, y), 10, (255,255,255), 3)
    # print(f"({pt[0]}, {pt[1]}) and center ({x},{y})")

    return sct_img


def mono_colorize(sct_img):
        # zeros = np.zeros(sct_img.shape, np.uint8)
        # out_mono = zeros
        # out_mono[:,:,0] = sct_img[:,:,0]
        # out_mono[out_mono < 180] = 0
        # out_mono[out_mono > 210] = 0
        # kernel = np.ones((5,5), 'uint8')
        # out_mono = cv2.dilate(out_mono, kernel)
        # out_bgr = out_mono + zeros + zeros
        # return out_bgr
        return sct_img[:,:,0]


def main():
    loop_time = time.time()

    while True:
        sct_img = capture_window()
        # out_bgr = mono_colorize(sct_img)
        out_bgr = sct_img[:,:,0]
        pattern = 'patterns/unit/minion.png'
        loc, width, height, name = template_match(out_bgr, pattern)
        counter = 0
        for pt in zip(*loc[::-1]):
            out_bgr = mark_the_spot(out_bgr, pt, width, height, name)
            counter += 1

        print(f"{counter} elements found.")

        cv2.imshow('monocolor', out_bgr)

        print('FPS {}'.format(round(1 / (time.time() - loop_time), 2)))
        loop_time = time.time()

        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()

