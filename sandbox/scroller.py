from pyWinhook import HookManager
from win32gui import PumpMessages, PostQuitMessage
from time import time
import win32api
import win32con


class Keystroke_Watcher(object):
    def __init__(self):
        self.hm = HookManager()
        self.hm.KeyDown = self.on_keyboard_event
        self.hm.HookKeyboard()


    def on_keyboard_event(self, event):
        try:
            if event.KeyID  == 70: #F
                self.scroll_up()
            if event.KeyID  == 68: #D
                self.scroll_down()
        finally:
            return True

    def scroll_up(self):
        print("scrolling up")
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, 200, 0)
    
    def scroll_down(self):
        print("scrolling down")
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -200, 0)

    def shutdown(self):
        PostQuitMessage(0)
        self.hm.UnhookKeyboard()


def main():
    watcher = Keystroke_Watcher()
    PumpMessages()


if __name__ == '__main__':
    main()

