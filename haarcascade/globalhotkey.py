from pyWinhook import HookManager
from win32gui import PumpMessages, PostQuitMessage

class Keystroke_Watcher(object):
    def __init__(self):
        self.hm = HookManager()
        self.hm.KeyDown = self.on_keyboard_event
        self.hm.HookKeyboard()


    def on_keyboard_event(self, event):
        try:
            if event.KeyID  == 83:
                self.your_method()
        finally:
            return True

    def your_method(self):
        print('Hi')

    def shutdown(self):
        PostQuitMessage(0)
        self.hm.UnhookKeyboard()


watcher = Keystroke_Watcher()
PumpMessages()