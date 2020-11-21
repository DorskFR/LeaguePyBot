import cv2
import numpy as np
from mss import mss
from PIL import Image
import pytesseract
import time

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
gold_box = {'top': 1045, 'left': 1200, 'width': 90, 'height': 25}
sct = mss()
ratio = 1

def capture_window(bounding_box):
    sct_img = sct.grab(bounding_box)
    width = int(bounding_box['width']/ratio)
    height = int(bounding_box['height']/ratio)
    sct_img = cv2.resize(np.array(sct_img),(width,height))
    return sct_img


def check_gold():
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

    return number, sct_img


def main():
    loop_time = time.time()
    while True:
        gold, sct_img = check_gold()

        sct_img = cv2.resize(sct_img, (300, 50))
        cv2.imshow('sct_img', sct_img)

        print(f"I have {gold} gold! FPS {round(1 / (time.time() - loop_time), 2)}")
        loop_time = time.time()

        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
