import tkinter as tk
from overlay import Window

win = Window(transparent=True)
label = tk.Label(win.root, text="Window_0")
label.pack()
Window.launch()
