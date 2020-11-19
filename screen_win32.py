import numpy as np
import cv2
from mss import mss
from PIL import Image
from time import time
import pyautogui
import win32gui, win32ui, win32con

bounding_box = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}

sct = mss()

def window_capture():
    #hwnd = win32gui.FindWindow(None, windowname)
    width = 1920
    height = 1080
    hwnd = None
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(dcObj, width, height)
    cDC.SelectObject(bmp)
    cDC.BitBlt((0,0),(width,height),dcObj,(0,0),win32con.SRCCOPY)

    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (height, width, 4)

    # Free Resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(bmp.GetHandle())

    return img


loop_time = time()
while True:
    # pyautogui.screenshot() = 5FPS for 1080p
    # sct.grab(bounding_box) = 7 FPS for 1080p
    sct_img = window_capture()
    cv2.imshow('screen', np.array(sct_img))

    print('FPS {}'.format(1 /(time() - loop_time)))
    loop_time = time()


    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break