import tkinter as tk

from . import constants as csts



class BaseFrame():
    def __init__(self,title="DEFAULT TITLE",geometry="720x720"):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(geometry)
        self.root.config(bg=csts.BG_COLOR)
        self.root.resizable(width=True,height=True)
