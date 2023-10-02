import tkinter as tk
import threading

class SimpleApp:
    def __init__(self, root):
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.root.destroy()
        print('im back')
        print(threading.enumerate())

root = tk.Tk()
app = SimpleApp(root)
root.mainloop()
print("after mainloop")
