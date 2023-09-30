import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from frames.base_frame import BaseFrame

from frames import constants as csts
from frames.utility import utility_fxns as utils
from user_data.utility.utility_fxns import convert_actlvl_toint,generate_usrinfo_json
from utility.utility_fxns import calc_default_wt

class FirstRunFrame(BaseFrame):
    def __init__(self,title="Welcom To My App Homie"):
        super().__init__(title=title,iconpath=csts.WELCICO_PATH)

        self.submit_button = tk.Button(self.root, text="Submit")
        self.submit_button.configure(bg=csts.BG_COLOR,fg=csts.FG_COLOR,font=csts.FONT,
                                         activebackground=csts.MY_GREEN)
        self.accept_button = tk.Button(self.root,text="Accept")

        self.name = ""
        self.height = -1
        self.weight = -1
        self.gender = ""
        self.birthday = ""
        self.goal_weight = -1
        self.goal_days = -1
        self.act_lvl = ""
        self.height_cm = None
        self.weight_kg = None
        self.bmi = None
        self.age = None
        self.bmr = None
        self.maintenance_cal = None
        self.cal_plan = None

        self.name_var = None
        self.act_lvl_var = None
        self.cal_plan_var = None
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
                messagebox.showerror("Error","Do you ever feeeel like a plastic bag?" +
                                     " Please enter something")

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
        self.name_var = tk.StringVar(self.root,value="noname")
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
            try:
                weight = float(wt_var.get())
                goal_weight = float(wt_var2.get())
                goal_days = int(wt_var3.get())
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values")
            if weight < 10 or weight > 700 or goal_weight < 10 or goal_weight > 700:
                messagebox.showerror("Error","Please enter valid weights (10-700)")
            elif goal_days < 1:
                messagebox.showerror("Error","Please enter a number greater than 0 for the days :)")
            else:
                self.weight = weight
                self.goal_weight = goal_weight
                self.goal_days = goal_days
                for widget in self.root.grid_slaves():
                    widget.grid_remove()
                print(f"weight: {self.weight}")
                print(f"goalwt: {self.goal_weight}")
                self.root.unbind('<Return>')
                self.get_act_lvl()
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
        wt_var = tk.StringVar(value=dflt_wt)
        users_wt_spinbox = tk.Spinbox(self.root, from_=0, to=700, width=5, format="%0.1f",
                                           textvariable=wt_var)
        users_wt_spinbox.configure(bg=csts.BG_COLOR,fg=csts.FG_COLOR,font=csts.FONT)
        users_wt_spinbox.grid(row=1, column=1,padx=csts.PADX, pady=csts.PADY)

        users_wt_lbs_label2 = tk.Label(self.root, text="Goal (lbs):")
        users_wt_lbs_label2.configure(font=csts.FONT,bg=csts.BG_COLOR,fg=csts.FG_COLOR)
        users_wt_lbs_label2.grid(row=2, column=0,padx=csts.PADX, pady=csts.PADY)
        wt_var2 = tk.StringVar(value=dflt_wt-15)
        users_wt_spinbox2 = tk.Spinbox(self.root, from_=0, to=700, width=5, format="%0.1f",
                                           textvariable=wt_var2)
        users_wt_spinbox2.configure(bg=csts.BG_COLOR,fg=csts.FG_COLOR,font=csts.FONT)
        users_wt_spinbox2.grid(row=2, column=1,padx=csts.PADX, pady=csts.PADY)

        users_wt_lbs_label3 = tk.Label(self.root, text="In how many days do you want to hit your goal?:")
        users_wt_lbs_label3.configure(font=csts.FONT,bg=csts.BG_COLOR,fg=csts.FG_COLOR)
        users_wt_lbs_label3.grid(row=3, column=0,padx=csts.PADX, pady=csts.PADY)
        wt_var3 = tk.IntVar(value=200)
        users_wt_spinbox3 = tk.Spinbox(self.root, from_=0, to=700, width=5, format="%1.0f",
                                           textvariable=wt_var3)
        users_wt_spinbox3.configure(bg=csts.BG_COLOR,fg=csts.FG_COLOR,font=csts.FONT)
        users_wt_spinbox3.grid(row=3, column=1,padx=csts.PADX, pady=csts.PADY)

        # Creating a Submit button
        self.submit_button.configure(command=on_submitwt)
        self.submit_button.grid(row=4, column=0, columnspan=4, pady=2*csts.PADY)

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
                    messagebox.showerror("Error", "Date out of range. Please enter a date" +
                                         " between 01/01/1900 and today(if you a baby).")
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
        self.submit_button.grid(row=2, column=0, columnspan=5, pady=10)

        self.root.bind('<Return>',validate_date)
    ##############################################################################################

    ## get activity_level ########################################################################
    def get_act_lvl(self):
        def act_submit_after():
            self.submit_button.config(state=tk.NORMAL)
            self.act_lvl = convert_actlvl_toint(self.act_lvl_var.get())
            print(f"activity level: {self.act_lvl}")
            for widget in self.root.grid_slaves():
                widget.grid_remove()
            self.root.unbind('<Return>')
            self.generate_necessary_attributes()
        def act_submit(event=None):
            label.unbind_all('<Button-1>')
            if event:
                self.submit_button.config(state=tk.ACTIVE)
                self.root.after(100,act_submit_after)
            else:
                act_submit_after()
        def create_radiobtn(option,row,col) -> None:
            rbtn_frame = tk.Frame(self.root)
            rbtn_frame.configure(bg=csts.BG_COLOR)
            rbtn_frame.grid(row=row,column=col,padx=csts.PADX,pady=csts.PADY,sticky='w')
            style = ttk.Style()
            style.configure('radio.TRadiobutton',background=csts.BG_COLOR,\
                            foreground=csts.FG_COLOR,activebackground=csts.MY_BLUE)
            rbtn = ttk.Radiobutton(rbtn_frame, style='radio.TRadiobutton', \
                                   variable=self.act_lvl_var, value=option)
            rbtn.pack(side='left')
            label = tk.Label(rbtn_frame, text=option, wraplength=csts.FRSR_RADIO_LBL_W)
            label.configure(bg=csts.BG_COLOR,fg=csts.FG_COLOR,font=csts.FRSR_RB_FONT)
            label.pack(side='left')
            #trying to bind label so label click will select the radio btn its assoc. with
            label.bind('<Button-1>', lambda e: self.act_lvl_var.set(option))
        label = tk.Label(self.root, text='Choose Your Activity Level:')
        label.configure(bg=csts.BG_COLOR,fg=csts.FG_COLOR,font=csts.FONT)
        label.grid(row=0, column=0, columnspan=5, pady=10)
        self.act_lvl_var = tk.StringVar(value=csts.ACTLVL_OP2)
        create_radiobtn(csts.ACTLVL_OP1,1,0)
        create_radiobtn(csts.ACTLVL_OP2,1,1)
        create_radiobtn(csts.ACTLVL_OP3,1,2)
        create_radiobtn(csts.ACTLVL_OP4,1,3)
        create_radiobtn(csts.ACTLVL_OP5,2,0)
        create_radiobtn(csts.ACTLVL_OP6,2,1)
        create_radiobtn(csts.ACTLVL_OP7,2,2)

        self.submit_button.configure(command=act_submit)
        self.submit_button.grid(row=3, column=0, columnspan=3, pady=10)
        self.root.bind('<Return>',act_submit)
    ##############################################################################################
    
    ## get plan ##################################################################################
    # def get_plan(self):
    #     def plan_submit_after():
    #         self.submit_button.config(tk.NORMAL)
    #     def plan_submit(event=None):
    #         if event:
    #             self.submit_button.config(tk.ACTIVE)
    #             self.root.after(100,plan_submit_after)
    #         else:
    #             plan_submit_after()

    ## generate attributes #######################################################################
    def generate_necessary_attributes(self) -> None:
        self.height_cm = utils.calc_height_cm(height_in=self.height)
        self.weight_kg = utils.calc_weight_kg(weight_lbs=self.weight)
        self.bmi = utils.calc_bmi(weight=self.weight,height=self.height)
        self.age = utils.calc_age(self.birthday)
        self.bmr = utils.calc_bmr(gender=self.gender,weight_kg=self.weight_kg,\
                                  height_cm=self.height_cm,age=self.age)
        self.maintenance_cal = utils.calc_maintenance_rate(bmr=self.bmr,act_factor=self.act_lvl)

        self.one_last_question()
    ##############################################################################################

    ## cal plan ##################################################################################
    def one_last_question(self) -> None:
        def on_accept():
            self.accept_button.config(state=tk.NORMAL)
            self.cal_plan = num_cals
            print("User accepted the recommendation.")
            for widget in self.root.grid_slaves():
                widget.grid_remove()
            self.root.destroy()  # or hide this window and open a new one
            self.all_steps_done()

        def on_accept_b4(event = None):
            if event:
                self.accept_button.config(state=tk.ACTIVE)
                self.root.after(100,on_accept)
            else:
                on_accept()

        def on_submit_cust_b4(event = None):
            if event:
                self.submit_button.config(state=tk.ACTIVE)
                self.root.after(100,on_submit_cust_after)
            else:
                on_submit_cust_after()

        def on_submit_cust_after():
            self.submit_button.config(state=tk.NORMAL)
            custom_calories = self.cal_plan_var.get()
            try:
                custom_calories = int(custom_calories)
            except ValueError:
                messagebox.showerror("Error","Please enter valid number for your calorie plan")
                return
            if custom_calories < 0:
                messagebox.showerror("Error","Please enter only positive numbers")
                return
            print(f"User entered custom calorie intake: {custom_calories}")
            self.cal_plan = custom_calories
            self.goal_days = utils.calc_days_to_goal(maintcal=self.maintenance_cal,\
                                                     cal_plan=self.cal_plan,\
                                                        currweight=self.weight,\
                                                            goalweight=self.goal_weight)
            self.root.destroy()
            self.all_steps_done()

        def on_decline():
            def update_label_var():
                print("in update")
                try:
                    current_value = int(self.cal_plan_var.get())
                    days = utils.calc_days_to_goal(self.maintenance_cal,cal_plan=current_value,\
                                                   currweight=self.weight,\
                                                    goalweight=self.goal_weight)
                    var.set(str(days))
                    lbl_dynamic.config(text=f"It will take you {var.get()}" +
                                       "days to reach your weight goal")
                except ValueError:
                    var.set('__')
                self.root.after(1000, update_label_var) # continue looping every second

            self.root.bind('<Return>',on_submit_cust_b4)
            # Hide the current widgets
            for widget in self.root.grid_slaves():
                widget.grid_remove()
            lbl3 = tk.Label(self.root,text="Enter a custom daily calorie plan")
            lbl3.configure(bg=csts.BG_COLOR,fg=csts.FG_COLOR,font=csts.FONT)
            lbl3.grid(row=0,column=0)
            
            self.cal_plan_var = tk.StringVar()
            entry = tk.Entry(self.root,textvariable=self.cal_plan_var,font=csts.FONT,\
                             bg=csts.BG_COLOR,fg=csts.FG_COLOR)
            self.submit_button.configure(text="Submit", command=on_submit_cust_b4)
            # Show the Entry widget
            entry.grid(row=1, column=0, padx=csts.PADX, pady=csts.PADY)

            self.submit_button.grid(row=0, column=1, padx=10, pady=10)

            inner_frame = tk.Frame(self.root,bg=csts.BG_COLOR)
            inner_frame.grid(row=2,column=0,columnspan=2)
            var = tk.StringVar(value="__")
            lbl_dynamic = tk.Label(inner_frame,text=f"It will take you {var.get()} " +
                                   " days to reach your weight goal")
            lbl_dynamic.configure(bg=csts.BG_COLOR,fg=csts.FG_COLOR,font=csts.FONT)
            lbl_dynamic.pack()

            update_label_var()

            # You can now proceed to the next step or frame with the entered value.
        def create_lbl_based_on_severity(txt,svrty) -> 'tk.Label':
            lbl = tk.Label(self.root, text=txt,bg=csts.BG_COLOR,font=csts.FONT)
            if svrty == 1:
                lbl.configure(fg=csts.MY_GREEN)
            elif svrty == 2:
                lbl.configure(fg=csts.MY_WARNING_CLR)
            elif svrty == 3:
                lbl.configure(fg=csts.MY_SVR_WARNING_CLR)
            else:
                lbl.configure(fg=csts.MY_SVR_WARNING_CLR)
            return lbl

        num_cals = utils.calc_rec_cals(self.maintenance_cal,self.weight,self.goal_weight,\
                                       self.goal_days)

        # Create a Label
        label = tk.Label(self.root, text="Based on your responses it is recommended to intake " +
                         f"{num_cals} calories per day to lose {self.weight-self.goal_weight} " +
                         f"lbs in {self.goal_days} days")
        label.configure(bg=csts.BG_COLOR,fg=csts.FG_COLOR,font=csts.FONT)
        label.grid(row=0, column=0,columnspan=2, padx=csts.PADX, pady=csts.PADY)

        # Create a lbl based on plan aggresiveness
        svrtxt,severity = utils.check_calplan_validity(self.maintenance_cal,num_cals)
        lbl2 = create_lbl_based_on_severity(svrtxt,severity)
        lbl2.grid(row=1,column=0,columnspan=2)

        # Create "Sounds Good" Button
        self.accept_button.configure(text="Sounds Good", command=on_accept)
        self.accept_button.configure(bg=csts.BG_COLOR,fg=csts.FG_COLOR,font=csts.FONT,\
                                     activebackground=csts.MY_GREEN)
        self.accept_button.grid(row=2, column=0, padx=10, pady=10)


        # Create "No" Button
        decline_button = tk.Button(self.root, text="   No   ", command=on_decline)
        decline_button.configure(bg=csts.BG_COLOR,fg=csts.FG_COLOR,font=csts.FONT)
        decline_button.grid(row=2, column=1, padx=10, pady=10)

        self.root.bind('<Return>',on_accept_b4)
    ##############################################################################################

    ## make sure to call this last, after all things are done generate a json file to store dict
    def all_steps_done(self) -> None:
        usr_info = {
            "name":             self.name,
            "height":           self.height,
            "weight":           self.weight,
            "gender":           self.gender,
            "birthday":         self.birthday,
            "goal_weight":      self.goal_weight,
            "activity_level":   self.act_lvl,
            "goal_days":        self.goal_days,
            "height_cm":        self.height_cm,
            "weight_kg":        self.weight_kg,
            "bmi":              self.bmi,
            "age":              self.age,
            "bmr":              self.bmr,
            "maintenance_cal":  self.maintenance_cal,
            "cal_plan":         self.cal_plan
        }
        generate_usrinfo_json(usr_info=usr_info)
