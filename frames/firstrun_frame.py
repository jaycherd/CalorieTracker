import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from frames.base_frame import BaseFrame

from frames import constants as csts
from utility.utility_fxns import calc_default_wt

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
        def name_entered_after():
            self.submit_button.config(state=tk.NORMAL)
            name = self.name_var.get()
            if name != "":
                self.name = name
                for widget in self.root.grid_slaves():
                    widget.grid_remove()
                users_name_entry.unbind('<Return>')
                print(f"name: {self.name}") #debug
                self.get_gender()
            else:
                messagebox.showerror("Error","Do you ever feeeel like a plastic bag?\
                                      Please enter something")

        def name_entered(event = None):
            if event: # then enter was pressed to get here so do some magic to highlight btn
                del event
                self.submit_button.config(state=tk.ACTIVE)
                self.root.after(100,name_entered_after)
            else:
                name_entered_after()

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

        self.submit_button.configure(command=name_entered)
        self.submit_button.grid(row=2, column=0, columnspan=4, pady=2*csts.PADY)
    ##############################################################################################

    ## Get Height ################################################################################
    def get_height(self):
        def on_submit_height_after():
            self.submit_button.config(state=tk.NORMAL)
            feet = feet_var.get()
            inches = inches_var.get()
            if feet < 1 or inches < 0 or feet > 10 or inches > 11:
                messagebox.showerror("Error","Please enter a valid height" +
                                     " (between newborn and giraffe)")
            else:
                self.height = feet*12 + inches
                print(f"height: {self.height}") #debug
                for widget in self.root.grid_slaves():
                    widget.grid_remove()
                self.root.unbind('<Return>')
                self.get_weight()
        def on_submit_height(event = None):
            if event:
                del event
                self.submit_button.config(state=tk.ACTIVE)
                self.root.after(100,on_submit_height_after)
            else:
                on_submit_height_after()

        # Creating a Label
        users_ht_label = tk.Label(self.root, text="Enter your height:")
        users_ht_label.configure(font=csts.FONT,bg=csts.BG_COLOR,fg=csts.FG_COLOR)
        users_ht_label.grid(row=0, column=0, columnspan=4, pady=csts.PADY)
        # Creating a Label and a Spinbox for feet
        users_ht_feet_label = tk.Label(self.root, text="Feet:")
        users_ht_feet_label.configure(font=csts.FONT,bg=csts.BG_COLOR,fg=csts.FG_COLOR)
        users_ht_feet_label.grid(row=1, column=0,padx=csts.PADX, pady=csts.PADY)
        feet_var = tk.IntVar(value=5)
        users_ht_feet_spinbox = tk.Spinbox(self.root, from_=0, to=10, width=5, format="%1.0f",
                                           textvariable=feet_var)
        users_ht_feet_spinbox.configure(bg=csts.BG_COLOR,fg=csts.FG_COLOR,font=csts.FONT)
        users_ht_feet_spinbox.grid(row=1, column=1,padx=csts.PADX, pady=csts.PADY)

        # Creating a Label and a Spinbox for inches
        users_ht_inches_label = tk.Label(self.root, text="Inches:")
        users_ht_inches_label.configure(font=csts.FONT,bg=csts.BG_COLOR,fg=csts.FG_COLOR)
        users_ht_inches_label.grid(row=1, column=2,padx=csts.PADX, pady=csts.PADY)
        inches_var = tk.IntVar(value=7)
        users_ht_inches_spinbox = tk.Spinbox(self.root, from_=0, to=11, width=5, format="%1.0f",
                                             textvariable=inches_var)
        users_ht_inches_spinbox.configure(bg=csts.BG_COLOR,fg=csts.FG_COLOR,font=csts.FONT)
        users_ht_inches_spinbox.grid(row=1, column=3,padx=csts.PADX, pady=csts.PADY)

        # Creating a Submit button
        self.submit_button.configure(command=on_submit_height)
        self.submit_button.grid(row=2, column=0, columnspan=4, pady=2*csts.PADY)

        self.root.bind('<Return>',on_submit_height)
    ##############################################################################################

    ## get weight ################################################################################
    def get_weight(self):
        def on_submitwt_after():
            self.submit_button.config(state=tk.NORMAL)
            weight = wt_var.get()
            goal_weight = wt_var2.get()
            if weight < 10 or weight > 700 or goal_weight < 10 or goal_weight > 700:
                messagebox.showerror("Error","Please enter valid weights (10-700)")
            else:
                self.weight = weight
                self.goal_weight = goal_weight
                for widget in self.root.grid_slaves():
                    widget.grid_remove()
                print(f"weight: {self.weight}")
                print(f"goalwt: {self.goal_weight}")
                self.root.unbind('<Return>')
                self.root.destroy()
        def on_submitwt(event = None):
            if event:
                del event
                self.submit_button.config(state=tk.ACTIVE)
                self.root.after(100,on_submitwt_after)
            else:
                on_submitwt_after()

        # Creating a Label
        users_wt_label = tk.Label(self.root, text="Enter your current/goal weight:")
        users_wt_label.configure(font=csts.FONT,bg=csts.BG_COLOR,fg=csts.FG_COLOR)
        users_wt_label.grid(row=0, column=0, columnspan=4, pady=csts.PADY)
        # Creating a Label and a Spinbox for pounds
        users_wt_lbs_label = tk.Label(self.root, text="Current (lbs):")
        users_wt_lbs_label.configure(font=csts.FONT,bg=csts.BG_COLOR,fg=csts.FG_COLOR)
        users_wt_lbs_label.grid(row=1, column=0,padx=csts.PADX, pady=csts.PADY)
        dflt_wt = calc_default_wt(self.height,self.gender)
        wt_var = tk.IntVar(value=dflt_wt)
        users_wt_spinbox = tk.Spinbox(self.root, from_=0, to=700, width=5, format="%1.0f",
                                           textvariable=wt_var)
        users_wt_spinbox.configure(bg=csts.BG_COLOR,fg=csts.FG_COLOR,font=csts.FONT)
        users_wt_spinbox.grid(row=1, column=1,padx=csts.PADX, pady=csts.PADY)

        users_wt_lbs_label2 = tk.Label(self.root, text="Goal (lbs):")
        users_wt_lbs_label2.configure(font=csts.FONT,bg=csts.BG_COLOR,fg=csts.FG_COLOR)
        users_wt_lbs_label2.grid(row=2, column=0,padx=csts.PADX, pady=csts.PADY)
        wt_var2 = tk.IntVar(value=dflt_wt-15)
        users_wt_spinbox2 = tk.Spinbox(self.root, from_=0, to=700, width=5, format="%1.0f",
                                           textvariable=wt_var2)
        users_wt_spinbox2.configure(bg=csts.BG_COLOR,fg=csts.FG_COLOR,font=csts.FONT)
        users_wt_spinbox2.grid(row=2, column=1,padx=csts.PADX, pady=csts.PADY)

        # Creating a Submit button
        self.submit_button.configure(command=on_submitwt)
        self.submit_button.grid(row=3, column=0, columnspan=4, pady=2*csts.PADY)

        self.root.bind('<Return>',on_submitwt)
    ##############################################################################################

    ## get gender ################################################################################
    def get_gender(self):
        def on_submitgnd_after():
            self.submit_button.config(state=tk.NORMAL)
            gender = gender_var.get()
            ## do error checking here
            self.gender = gender
            for widget in self.root.grid_slaves():
                widget.grid_remove()
            self.root.unbind('<Return>')
            print(f"gender: {self.gender}")
            self.get_bday()
        def on_submitgnd(event = None):
            if event:
                del event
                self.submit_button.config(state=tk.ACTIVE)
                self.root.after(100,on_submitgnd_after)
            else:
                on_submitgnd_after()

        # Creating a Label
        users_gnd_label = tk.Label(self.root, text="Enter your Gender:")
        users_gnd_label.configure(font=csts.FONT,bg=csts.BG_COLOR,fg=csts.FG_COLOR)
        users_gnd_label.grid(row=0, column=0, columnspan=4, pady=csts.PADY)
        # Creating a Label and a Spinbox for pounds
        gender_var = tk.StringVar(value='Male')  # default value
        gender_combobox = ttk.Combobox(self.root, values=('Male', 'Female', 'Other'),\
                                       textvariable=gender_var,\
                                       background=csts.BG_COLOR,font=csts.FONT,\
                                       width=csts.FRSR_ENTRY_W)
        gender_combobox.grid(row=1,column=1,padx=csts.PADX,pady=csts.PADY)
        # users_wt_spinbox.configure(bg=csts.BG_COLOR,fg=csts.FG_COLOR,font=csts.FONT)
        # users_wt_spinbox.grid(row=1, column=1,padx=csts.PADX, pady=csts.PADY)
        # Creating a Submit button
        self.submit_button.configure(command=on_submitgnd)
        self.submit_button.grid(row=2, column=0, columnspan=4, pady=2*csts.PADY)

        self.root.bind('<Return>',on_submitgnd)
    ##############################################################################################

    ## get bday   ################################################################################
    def get_bday(self):
        def validate_date_after():
            self.submit_button.config(state=tk.NORMAL)
            month = month_entry.get()
            day = day_entry.get()
            year = year_entry.get()
            date_str = f"{month}/{day}/{year}"
            try:
                usr_bday = datetime.strptime(date_str, '%m/%d/%Y')
                start_date = datetime(1900, 1, 1)  # Example start date: January 1, 2000
                end_date = datetime.today()  # Example end date: December 31, 2025

                if start_date <= usr_bday <= end_date:
                    self.birthday = date_str
                    print(date_str)
                    for widget in self.root.grid_slaves():
                        widget.grid_remove()
                    self.root.unbind('<Return>')
                    self.get_height()
                else:
                    messagebox.showerror("Error", "Date out of range. Please enter a date between \
                                         01/01/1900 and today(for newborns).")
            except ValueError:
                messagebox.showerror("Error", "Invalid Date. Please enter in MM/DD/YYYY format.")
        def validate_date(event = None):
            if event:
                del event
                self.submit_button.config(state=tk.ACTIVE)
                self.root.after(100,validate_date_after)
            else:
                validate_date_after()
        def on_focus_in(event, entry):
            del event
            entry.configure(bd=2, highlightthickness=2, highlightcolor=csts.MY_BLUE)
        def on_focus_out(event, entry):
            del event
            entry.configure(bd=1, highlightthickness=1, highlightcolor='grey')

        # Label
        label = tk.Label(self.root, text='Enter your birthday:')
        label.configure(bg=csts.BG_COLOR,fg=csts.FG_COLOR,font=csts.FONT)
        label.grid(row=0, column=0, columnspan=5, pady=10)

        # Month Entry
        month_entry = tk.Entry(self.root, width=2)
        month_entry.insert(0,'01')
        month_entry.configure(bg=csts.BG_COLOR,fg=csts.FG_COLOR,font=csts.FONT)
        month_entry.grid(row=1, column=0)


        # First '/'
        tk.Label(self.root, text='/',font=csts.FONT,fg=csts.FG_COLOR,bg=csts.BG_COLOR)\
            .grid(row=1, column=1)

        # Day Entry
        day_entry = tk.Entry(self.root, width=2)
        day_entry.insert(0,'01')
        day_entry.configure(bg=csts.BG_COLOR,fg=csts.FG_COLOR,font=csts.FONT)
        day_entry.grid(row=1, column=2)


        # Second '/'
        tk.Label(self.root, text='/',font=csts.FONT,fg=csts.FG_COLOR,bg=csts.BG_COLOR)\
            .grid(row=1, column=3)

        # Year Entry
        year_entry = tk.Entry(self.root, width=4)
        year_entry.insert(0,'2000')
        year_entry.configure(bg=csts.BG_COLOR,fg=csts.FG_COLOR,font=csts.FONT)
        year_entry.grid(row=1, column=4)

        month_entry.bind("<FocusIn>", lambda e: on_focus_in(e, month_entry))
        month_entry.bind("<FocusOut>", lambda e: on_focus_out(e, month_entry))

        day_entry.bind("<FocusIn>", lambda e: on_focus_in(e, day_entry))
        day_entry.bind("<FocusOut>", lambda e: on_focus_out(e, day_entry))

        year_entry.bind("<FocusIn>", lambda e: on_focus_in(e, year_entry))
        year_entry.bind("<FocusOut>", lambda e: on_focus_out(e, year_entry))

        # Validate Button
        self.submit_button.configure(command=validate_date)
        self.submit_button.configure(bg=csts.BG_COLOR,fg=csts.FG_COLOR,font=csts.FONT)
        self.submit_button.grid(row=2, column=0, columnspan=5, pady=10)

        self.root.bind('<Return>',validate_date)
    ##############################################################################################
