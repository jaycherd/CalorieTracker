import tkinter as tk
from tkinter import ttk

from .base_frame import BaseFrame
from .error_frame import ErrorFrame

from . import constants as csts

class FirstRunFrame(BaseFrame):
    def __init__(self,title="Welcom To My App Homie"):
        super().__init__(title=title,iconpath=csts.WELCICO_PATH)

        self.submit_button = tk.Button(self.root, text="Submit")
        self.submit_button.configure(bg=csts.BG_COLOR,fg=csts.FG_COLOR,font=csts.FONT,
                                         activebackground=csts.MY_GREEN)

        self.name = ""
        self.height = -1
        self.weight = -1
        self.gender = ""
        self.birthday = ""
        self.goal_weight = -1

        self.name_var = None
        self.get_name() # the first step, want things to be called one at a time rather than giant
        #gui where user would have to enter it all at once
        self.root.mainloop()

    ## Get Name ##################################################################################
    def get_name(self):
        def name_entered(event):
            del event
            self.name = self.name_var.get()
            users_name_lbl.grid_remove()
            users_name_entry.grid_remove()
            users_name_entry.unbind('<Return>')
            print(f"name: {self.name}") #debug
            self.get_height()

        users_name_lbl = tk.Label(self.root, text = "Welcome to my app bro, what's your name?",
                                  font=csts.FONT)
        users_name_lbl.configure(bg=csts.BG_COLOR,fg=csts.FG_COLOR)
        users_name_lbl.grid(column = 0, row = 0,padx=csts.PADX,pady=csts.PADY)
        self.name_var = tk.StringVar(self.root)
        users_name_entry = tk.Entry(self.root,textvariable=self.name_var,font=csts.FONT)
        users_name_entry.configure(bg=csts.BG_COLOR,fg=csts.FG_COLOR)
        users_name_entry.focus()
        users_name_entry.bind('<Return>',name_entered)
        users_name_entry.grid(row=1,column=0,padx=csts.PADX,pady=csts.PADY)
    ##############################################################################################

    ## Get Height ################################################################################
    def get_height(self):
        def on_submit_height():
            feet = feet_var.get()
            inches = inches_var.get()
            if feet < 0 or inches < 0 or feet > 10 or inches > 11:
                err_frame = ErrorFrame()
                err_frame.draw_height_error()
            else:
                self.height = feet*12 + inches
                print(f"height: {self.height}") #debug
                users_ht_label.grid_remove()
                users_ht_feet_label.grid_remove()
                users_ht_feet_spinbox.grid_remove()
                users_ht_inches_label.grid_remove()
                users_ht_inches_spinbox.grid_remove()
                self.submit_button.grid_remove()
                self.get_weight()
        # Creating a Label
        users_ht_label = tk.Label(self.root, text="Enter your height:")
        users_ht_label.configure(font=csts.FONT,bg=csts.BG_COLOR,fg=csts.FG_COLOR)
        users_ht_label.grid(row=0, column=0, columnspan=4, pady=csts.PADY)
        # Creating a Label and a Spinbox for feet
        users_ht_feet_label = tk.Label(self.root, text="Feet:")
        users_ht_feet_label.configure(font=csts.FONT,bg=csts.BG_COLOR,fg=csts.FG_COLOR)
        users_ht_feet_label.grid(row=1, column=0,padx=csts.PADX, pady=csts.PADY)
        feet_var = tk.IntVar()
        users_ht_feet_spinbox = tk.Spinbox(self.root, from_=0, to=10, width=5, format="%1.0f",
                                           textvariable=feet_var)
        users_ht_feet_spinbox.configure(bg=csts.BG_COLOR,fg=csts.FG_COLOR,font=csts.FONT)
        users_ht_feet_spinbox.grid(row=1, column=1,padx=csts.PADX, pady=csts.PADY)

        # Creating a Label and a Spinbox for inches
        users_ht_inches_label = tk.Label(self.root, text="Inches:")
        users_ht_inches_label.configure(font=csts.FONT,bg=csts.BG_COLOR,fg=csts.FG_COLOR)
        users_ht_inches_label.grid(row=1, column=2,padx=csts.PADX, pady=csts.PADY)
        inches_var = tk.IntVar()
        users_ht_inches_spinbox = tk.Spinbox(self.root, from_=0, to=11, width=5, format="%1.0f",
                                             textvariable=inches_var)
        users_ht_inches_spinbox.configure(bg=csts.BG_COLOR,fg=csts.FG_COLOR,font=csts.FONT)
        users_ht_inches_spinbox.grid(row=1, column=3,padx=csts.PADX, pady=csts.PADY)

        # Creating a Submit button
        self.submit_button.configure(command=on_submit_height)
        self.submit_button.grid(row=2, column=0, columnspan=4, pady=2*csts.PADY)
    ##############################################################################################

    ## get weight ################################################################################
    def get_weight(self):
        def on_submit():
            weight = wt_var.get()
            if weight < 10 or weight > 700:
                err_frame = ErrorFrame()
                err_frame.draw_weight_error()
            else:
                self.weight = weight
                users_wt_label.grid_remove()
                users_wt_lbs_label.grid_remove()
                users_wt_spinbox.grid_remove()
                self.submit_button.grid_remove()
                print(f"weight: {weight}")
                self.get_gender()
                

        # Creating a Label
        users_wt_label = tk.Label(self.root, text="Enter your weight:")
        users_wt_label.configure(font=csts.FONT,bg=csts.BG_COLOR,fg=csts.FG_COLOR)
        users_wt_label.grid(row=0, column=0, columnspan=4, pady=csts.PADY)
        # Creating a Label and a Spinbox for pounds
        users_wt_lbs_label = tk.Label(self.root, text="Pounds:")
        users_wt_lbs_label.configure(font=csts.FONT,bg=csts.BG_COLOR,fg=csts.FG_COLOR)
        users_wt_lbs_label.grid(row=1, column=0,padx=csts.PADX, pady=csts.PADY)
        wt_var = tk.IntVar()
        users_wt_spinbox = tk.Spinbox(self.root, from_=0, to=700, width=5, format="%1.0f",
                                           textvariable=wt_var)
        users_wt_spinbox.configure(bg=csts.BG_COLOR,fg=csts.FG_COLOR,font=csts.FONT)
        users_wt_spinbox.grid(row=1, column=1,padx=csts.PADX, pady=csts.PADY)
        # Creating a Submit button
        self.submit_button.configure(command=on_submit)
        self.submit_button.grid(row=2, column=0, columnspan=4, pady=2*csts.PADY)
    ##############################################################################################

    ## get gender ################################################################################
    def get_gender(self):
        def on_submit():
            gender = gender_var.get()
            ## do error checking here
            self.gender = gender
            print(f"gender: {self.gender}")
        # Creating a Label
        users_gnd_label = tk.Label(self.root, text="Enter your Gender:")
        users_gnd_label.configure(font=csts.FONT,bg=csts.BG_COLOR,fg=csts.FG_COLOR)
        users_gnd_label.grid(row=0, column=0, columnspan=4, pady=csts.PADY)
        # Creating a Label and a Spinbox for pounds
        gender_var = tk.StringVar(value='Male')  # default value
        gender_combobox = ttk.Combobox(self.root, values=('Male', 'Female', 'Other'), textvariable=gender_var)
        gender_combobox.grid(row=1,column=1)
        # users_wt_spinbox.configure(bg=csts.BG_COLOR,fg=csts.FG_COLOR,font=csts.FONT)
        # users_wt_spinbox.grid(row=1, column=1,padx=csts.PADX, pady=csts.PADY)
        # Creating a Submit button
        self.submit_button.configure(command=on_submit)
        self.submit_button.grid(row=2, column=0, columnspan=4, pady=2*csts.PADY)

    ##############################################################################################

        # print(f"weight: {self.weight}")
        # print(f"gender: {self.gender}")
        # print(f"birthday: {self.birthday}")
        # print(f"goal_weight: {self.goal_weight}")



    
        

        