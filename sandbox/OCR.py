import cv2
import numpy as np
from mss import mss
from PIL import Image
import pytesseract

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
    pil_image = Image.fromarray(cv2.cvtColor(sct_img, cv2.COLOR_BGR2RGB))
    text = pytesseract.image_to_string(pil_image, config=conf)
    return int(text)

gold = check_gold()
if gold > 500:
    print(f"Of course I have more than 500 gold, I have {gold} gold!")