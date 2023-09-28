import tkinter as tk

from .base_frame import BaseFrame

from . import constants as csts

class ErrorFrame(BaseFrame):
    def __init__(self,title="Oops"):
        super().__init__(title=title,iconpath=csts.ERRICO_PATH)

    def draw_height_error(self):
        def on_submit():
            self.root.destroy()
        mytxt = "Please enter valid numbers for feet (0-10) and inches (0-11)"
        ht_err_lbl = tk.Label(self.root, text=mytxt)
        ht_err_lbl.configure(font=csts.FONT,bg=csts.BG_COLOR,fg=csts.FG_COLOR)
        ht_err_lbl.grid(row=0,column=0)

        accept_btn = tk.Button(self.root, text="OK FINE WHATEVER", command=on_submit)
        accept_btn.configure(bg=csts.BG_COLOR,fg=csts.FG_COLOR,font=csts.FONT,activebackground=csts.MY_GREEN)
        accept_btn.grid(row=2, column=0, columnspan=4, pady=2*csts.PADY)
