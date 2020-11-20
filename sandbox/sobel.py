import time
import cv2
import numpy as np
from mss import mss
import win32gui

bounding_box = {'left': 0, 'top': 0, 'width': 1920, 'height': 1080}
ratio = 1
sct = mss()

def capture_window():
    sct_img = sct.grab(bounding_box)
    width = int(bounding_box['width']/ratio)
    height = int(bounding_box['height']/ratio)
    sct_img = cv2.resize(np.array(sct_img),(width,height))
    return sct_img

def apply_sobel(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)
    grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    return grad

def main():
    loop_time = time.time()

    while True:
        sct_img = capture_window()

        grad = apply_sobel(sct_img)
        contoured = find_coun

        cv2.imshow('sobel', cv2.resize(grad, (960, 540)))

        print('FPS {}'.format(round(1 / (time.time() - loop_time), 2)))
        loop_time = time.time()

        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
