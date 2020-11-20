from pyWinhook import HookManager
from win32gui import PumpMessages, PostQuitMessage
from time import time
import cv2
import numpy as np
from mss import mss


bounding_box ={'left': 0, 'top': 0, 'width': 1920, 'height': 1080}
ratio = 1
sct = mss()


class Keystroke_Watcher(object):
    def __init__(self):
        self.hm = HookManager()
        self.hm.KeyDown = self.on_keyboard_event
        self.hm.HookKeyboard()


    def on_keyboard_event(self, event):
        try:
            if event.KeyID  == 70: #F
                self.save_positive()
            if event.KeyID  == 68: #D
                self.save_negative()
        finally:
            return True

    def save_positive(self):
        screenshot = capture_window()
        loop_time = time()
        filename = f"positive/{loop_time}.jpg"
        cv2.imwrite(filename, screenshot)
        print(f'Saved {filename}')
    
    def save_negative(self):
        screenshot = capture_window()
        loop_time = time()
        filename = f"negative/{loop_time}.jpg"
        cv2.imwrite(filename, screenshot)
        print(f'Saved {filename}')

    def shutdown(self):
        PostQuitMessage(0)
        self.hm.UnhookKeyboard()


def capture_window():
    sct_img = sct.grab(bounding_box)
    width = int(bounding_box['width']/ratio)
    height = int(bounding_box['height']/ratio)
    sct_img = cv2.resize(np.array(sct_img),(width,height))
    return sct_img


def main():
    watcher = Keystroke_Watcher()
    PumpMessages()


if __name__ == '__main__':
    main()

