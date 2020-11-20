
import cv2
import numpy as np
from time import time
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

def draw_rectangles(img, rectangles):
        line_color = (0, 255, 0)
        line_type = cv2.LINE_4

        for (x, y, w, h) in rectangles:
            # determine the box positions
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            # draw the box
            cv2.rectangle(img, top_left, bottom_right, line_color, lineType=line_type)

        return img

def main():
    loop_time = time()

    while True:
        screenshot = capture_window()

        cascade_minion = cv2.CascadeClassifier('cascade/cascade.xml')
        rectangles = cascade_minion.detectMultiScale(screenshot)
        detection_image = draw_rectangles(screenshot, rectangles)

        cv2.imshow('matches', detection_image)

        print('FPS {}'.format(round(1 / (time() - loop_time), 2)))
        loop_time = time()

        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()