import win32api
import win32com.client

shell = win32com.client.Dispatch("WScript.Shell")
# shell.Run("app")
# win32api.Sleep(100)
# shell.AppActivate("myApp")
win32api.Sleep(100)
shell.SendKeys("%")
win32api.Sleep(500)
shell.SendKeys("t")
win32api.Sleep(500)
shell.SendKeys("r")
win32api.Sleep(500)
shell.SendKeys("name")
win32api.Sleep(500)
shell.SendKeys("{ENTER}")
win32api.Sleep(2500)