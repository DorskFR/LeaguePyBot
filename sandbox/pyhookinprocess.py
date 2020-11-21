import time
import cv2
import numpy as np
from mss import mss
import win32gui
from pyWinhook import HookManager
from multiprocessing import Process
import os


bounding_box ={'left': 0, 'top': 0, 'width': 1920, 'height': 1080}
ratio = 1
sct = mss()


def capture_window():
    sct_img = sct.grab(bounding_box)
    width = int(bounding_box['width']/ratio)
    height = int(bounding_box['height']/ratio)
    sct_img = cv2.resize(np.array(sct_img),(width,height))
    return sct_img


def main():
    loop_time = time.time()
    while True:
        
        sct_img = capture_window()
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
        os.system("taskkill /IM python.exe /f") # lol bruteforce

    def shutdown(self):
        win32gui.PostQuitMessage(0)
        self.hm.UnhookKeyboard()


def listen_k():
    watcher = Keystroke_Watcher()
    win32gui.PumpMessages()


if __name__ == '__main__':
    p = Process(target=listen_k)
    k = Process(target=main)
    p.start()
    k.start()
