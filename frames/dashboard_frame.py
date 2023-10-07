import sys
import pdb #for debugging
import traceback
import threading
import tkinter as tk
from tkinter import ttk,messagebox
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import AutoMinorLocator

from frames.base_frame import BaseFrame
from frames import constants as csts
from frames.utility import constants_dashboard as cdash
from frames.utility import utility_fxns as frameutils
from frames.utility.custom_entry import CustomEntry
from user_data.user import User
from user_data.utility import utility_fxns as utils


class DashboardFrame(BaseFrame):
    def __init__(self,user: User,title="Super Sexy Dashboard"):
        super().__init__(title=title,iconpath=csts.DASHICO_PATH,
                         scr_h_pcnt=csts.DASH_H_PCNT,scr_w_pcnt=csts.DASH_W_PCNT,alter_mouse=True,mouse_type='dot')
        self.user = user
        self.after_id_centermid = None
        self.after_id_topleft = None

        self.topleft_frame = self.create_styled_frame(self.root, 0, 0, 0.5, 0.35)
        self.topright_frame = self.create_styled_frame(self.root, 0.5, 0, 0.5, 0.35,)
        self.centerleft_frame = self.create_styled_frame(self.root, 0, 0.35, 0.25, 0.65,)
        self.centermid_frame = self.create_styled_frame(self.root, 0.25, 0.35, 0.5, 0.65,)
        self.centerright_frame = self.create_styled_frame(self.root, 0.75, 0.35, 0.25, 0.65)

        # to be implemented if you want to add more frames
        # self.bottomleft_frame = self.create_styled_frame(self.root, 0, 0.73, 0.5, 0.27,bg='green')
        # self.bottomright_frame = self.create_styled_frame(self.root, 0.5, 0.73, 0.5, 0.27, bg='light coral')

        self.setup_frames()

        self.root.protocol("WM_DELETE_WINDOW",self.on_closing)
        self.root.mainloop()

        
    def setup_frames(self):
        # Creating frames to place in widgets, bg temp while developing dashboard
        self.setup_topleft()
        self.setup_topright()
        self.setup_centerleft()
        self.setup_centermid()
        self.setup_centerright()

        # to be implemented, for two additional frames
        # self.setup_bottomleft()
        # self.setup_bottomright()



        

    # def loop_centermid_plot(self):
    #     if self.redraw_centermid_flag:
    #         self.setup_centermid(redraw=True)
    #         self.redraw_centermid_flag = False
    #     self.after_id_centermid = self.root.after(1500,self.loop_centermid_plot)
    
    # def loop_topleft_plot(self):
    #     if self.redraw_topleft_flag:
    #         self.setup_topleft(redraw=True)
    #         self.redraw_topleft_flag = False
    #     self.after_id_topleft = self.root.after(1500,self.loop_topleft_plot)
        



    def create_styled_frame(self, parent, relx, rely, relwidth, relheight, bg=csts.BG_COLOR):
        frame = tk.Frame(parent, bg=bg)
        frame.configure(highlightbackground=cdash.FRAMEBORDER_CLR,highlightcolor=cdash.FRAMEBORDER_CLR,highlightthickness=cdash.BORDERWIDTH)
        frame.place(relx=relx, rely=rely, relwidth=relwidth, relheight=relheight)
        return frame

    #want this frame to hold a weight log chart
    def setup_topleft(self,redraw=False):
        if redraw:
            for widget in self.topleft_frame.winfo_children():
                # widget.pack_forget()
                widget.destroy() #for my usage, i dont use anymore, and they just hide with forget

        label = tk.Label(self.topleft_frame, text="Your Weight Log")
        label.configure(bg=csts.BG_COLOR,fg=csts.FG_COLOR,font=cdash.FONTSMALLBOLD)
        label.pack()

        weights, dates = frameutils.get_weights_datetimes_fromjson(cdash.WEIGHTLOG_PATH)
        fig, ax = plt.subplots()
        ax.plot(dates, weights,color=cdash.LIGHTBLUE)

        #horizontal line to represent goal weight
        goal_weight = self.user.goal_weight
        ax.axhline(y=goal_weight,color=cdash.LIGHTRED,linestyle='--')
        #horizontal line label
        ax.text(dates[0], goal_weight + 1, f'Goal Weight ({round(goal_weight)})', color=cdash.LIGHTRED, va='bottom')

        #explicitly set limits to plot data
        min_limit = min(goal_weight, *weights) - 10
        max_limit = max(goal_weight, *weights) + 10
        ax.set_ylim(min_limit,max_limit)
        
        

        #formatting - colors
        fig.patch.set_facecolor(csts.BG_COLOR)
        ax.set_facecolor(csts.BG_COLOR)
        ax.tick_params(axis='x',colors=cdash.LIGHTBLUE)
        ax.tick_params(axis='y',colors=cdash.LIGHTBLUE)
        ax.xaxis.label.set_color(cdash.LIGHTBLUE)
        ax.yaxis.label.set_color(cdash.LIGHTBLUE)

        # Set labels for the axes
        ax.set_xlabel('Date (MM/DD)')
        ax.set_ylabel('Weight (lbs)')
        
        # Format the date on the x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
        
        # Calculate the interval for major ticks
        num_dates = len(dates)
        major_interval = max(1, num_dates // 10)  # Avoid zero interval, ensure there's at least one major tick
        
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=major_interval))
        ax.xaxis.set_minor_locator(AutoMinorLocator())  # Automatically add minor locators
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.4)
        
        # Embed the plot in Tkinter frame
        canvas = FigureCanvasTkAgg(fig, master=self.topleft_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side='top', fill='both', expand=1)
        
        plt.close(fig)

    def setup_topright(self,redraw=False):
        if redraw:
            for widget in self.topright_frame.winfo_children():
                # widget.pack_forget()
                widget.destroy() #for my usage, i dont use anymore, and they just hide with forget

        label = tk.Label(self.topright_frame, text="Your Calorie Log")
        label.configure(bg=csts.BG_COLOR,fg=csts.FG_COLOR,font=cdash.FONTSMALLBOLD)
        label.pack()

        calories, dates = frameutils.get_calories_datetimes_fromjson()
        fig, ax = plt.subplots()
        ax.plot(dates, calories,color=cdash.LIGHTBLUE)

        #formatting - colors
        fig.patch.set_facecolor(csts.BG_COLOR)
        ax.set_facecolor(csts.BG_COLOR)
        ax.tick_params(axis='x',colors=cdash.LIGHTBLUE)
        ax.tick_params(axis='y',colors=cdash.LIGHTBLUE)
        ax.xaxis.label.set_color(cdash.LIGHTBLUE)
        ax.yaxis.label.set_color(cdash.LIGHTBLUE)

        #horizontal line - calorie plan
        cal_plan = self.user.cal_plan
        ax.axhline(y=cal_plan,color=cdash.LIGHTRED,linestyle='--')
        #horizontal line label
        ax.text(dates[0], cal_plan + 1, f'Goal Calories ({round(cal_plan)})', color=cdash.LIGHTRED, va='bottom')

        #explicitly set limits to plot data
        min_limit = min(cal_plan, *calories) - 250
        max_limit = max(cal_plan, *calories) + 250
        ax.set_ylim(min_limit,max_limit)

        # Set labels for the axes
        ax.set_xlabel('Date (MM/DD)')
        ax.set_ylabel('Calories (lbs)')
        
        # Format the date on the x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
        
        # Calculate the interval for major ticks
        num_dates = len(dates)
        major_interval = max(1, num_dates // 10)  # Avoid zero interval, ensure there's at least one major tick
        
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=major_interval))
        ax.xaxis.set_minor_locator(AutoMinorLocator())  # Automatically add minor locators
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.4)
        
        # Embed the plot in Tkinter frame
        canvas = FigureCanvasTkAgg(fig, master=self.topright_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side='top', fill='both', expand=1)
        
        plt.close(fig)

    def setup_centerleft(self):
        # Create buttons
        log_weight_btn = self.create_button(self.centerleft_frame, text="Log Weight", command=self.log_weight_popup)
        log_calories_btn = self.create_button(self.centerleft_frame, text="Log Calories", command=self.log_calories_popup)
        third_button = self.create_button(self.centerleft_frame, text="Third Button", command=self.third_command)
        fourth_button = self.create_button(self.centerleft_frame, text="Fourth Button", command=self.fourth_command)
        
        # Place buttons
        log_weight_btn.pack(fill='both', expand=True)
        log_calories_btn.pack(fill='both', expand=True)
        third_button.pack(fill='both', expand=True)
        fourth_button.pack(fill='both', expand=True)

    def setup_centermid(self,redraw=False):
        if redraw:
            for widget in self.centermid_frame.winfo_children():
                # widget.pack_forget()
                widget.destroy() #for my usage, i dont use anymore, and they just hide with forget

        label = tk.Label(self.centermid_frame, text="Today's Calories")
        label.configure(bg=csts.BG_COLOR,fg=csts.FG_COLOR,font=cdash.FONTBOLD)
        label.pack()

        fig = Figure(figsize=(5,5))
        fig.patch.set_facecolor(csts.BG_COLOR)
        ax = fig.add_subplot(111)
        ax.set_facecolor(csts.BG_COLOR)
        
        
        consumed = frameutils.check_todays_calories()
        remaining = max(self.user.cal_plan - consumed, 0)  # Avoid negative values
        overconsumed_flag = None
        # Data to plot
        if consumed > self.user.cal_plan:
            sizes = [consumed]
            labels = ['Overconsumed']
            colors = ['#ff9999']
            explode = (0.1,)
            overconsumed_flag = True
        else:
            sizes = [consumed, remaining]
            labels = ['Consumed', 'Remaining']
            colors = ['#ff9999','#66b3ff']
            explode = (0.1, 0)  # explode 1st slice
            overconsumed_flag = False

        if overconsumed_flag:
            txt = f"You consumed {self.user.todays_calories - self.user.cal_plan} excess calories.. there is always tomorrow  :)"
            lbl_ovrcon = self.create_label(parent=self.centermid_frame,text=txt)
            lbl_ovrcon.pack()

        
        def func(pct, allvalues):
            absolute = int(pct/100.*sum(allvalues))
            return "{:d}".format(absolute)

        # Plotting the Pie chart
        _,texts,_ = ax.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct=lambda pct: func(pct, sizes), startangle=140, textprops={'color': 'black'})

        # defining color for labels
        label_color = cdash.LIGHTBLUE  # or any other color you prefer

        # Applying color to 'Consumed' and 'Remaining' labels
        for text in texts:
            text.set_color(label_color)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        
        # Embedding the pie chart in Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.centermid_frame)
        widget = canvas.get_tk_widget()
        widget.configure(bg=csts.BG_COLOR,highlightthickness=0)
        widget.pack()

    def setup_centerright(self):
        label = tk.Label(self.centerright_frame, text="Food Search")
        label.configure(bg=csts.BG_COLOR,fg=csts.FG_COLOR,font=cdash.FONTBOLD)
        label.pack()

        #need to do a search to generate the list
        autocomplete_list = ["apple", "banana", "pear", "pineapple", "peach", "plum", "pomegranate", "papaya"]
        self.entry = CustomEntry(self.centerright_frame, autocomplete_list,self)
        self.entry.pack()
    
    def setup_bottomleft(self):
        # Additional setup for the bottom left frame.
        pass
    
    def setup_bottomright(self):
        # Additional setup for the bottom right frame.
        pass


    # def create_button(self, parent, text, command=None):
    #     button = tk.Button(parent, text=text, command=command)
    #     button.configure(bg=csts.BG_COLOR,fg=cdash.LIGHTBLUE,font=csts.FONT,
    #                      borderwidth=cdash.CENTERLEFT_BRD_W+ 10,activebackground=csts.MY_GREEN)
    #     button.configure(highlightbackground=cdash.FRAMEBORDER_CLR,highlightcolor=cdash.FRAMEBORDER_CLR,highlightthickness=cdash.BORDERWIDTH)
    #     return button
    def create_button(self, parent, text, command=None):
        border_frame = tk.Frame(parent, background=cdash.FRAMEBORDER_CLR, bd=cdash.CENTERLEFT_BRD_W)
        border_frame.pack(fill='both', expand=True)  # Ensure border_frame expands
        
        button = tk.Button(border_frame, text=text, command=command, bg=csts.BG_COLOR, 
                        fg=cdash.LIGHTBLUE, font=csts.FONT, activebackground=csts.MY_GREEN)
        button.pack(side='left', fill='both', expand=True)  # Button expands within border_frame
        
        return border_frame  # Return border_frame since it’s the container holding the button

    
    def log_weight_popup(self):
        popup = tk.Toplevel(self.root)
        popup.configure(bg=csts.BG_COLOR)
        popup.title("Log Weight")
        # Calculating the position to center the popup over the parent window.
        window_width = popup.winfo_reqwidth()
        window_height = popup.winfo_reqheight()
        
        position_right = int(self.root.winfo_screenwidth()/2 - window_width/2)
        position_down = int(self.root.winfo_screenheight()/2 - window_height/2)
        
        # Positions the window in the center of the page.
        popup.geometry(f"+{position_right}+{position_down}")
        
        label = tk.Label(popup, text="Enter Weight:")
        label.configure(bg=csts.BG_COLOR,fg=csts.FG_COLOR,font=csts.FONT)
        label.pack()
        
        weight_var = tk.StringVar()
        entry = tk.Entry(popup, textvariable=weight_var)
        entry.configure(bg=csts.BG_COLOR,fg=csts.FG_COLOR,font=csts.FONT)
        entry.pack()
        entry.focus_set()
        
        submit_btn = self.create_button(parent=popup, text="Submit", command=lambda: self.log_weight(weight_var.get(), popup))
        submit_btn.pack()

        popup.grab_set() #makes popup modal, aka user must interact with popup before
        #making more inputs to the dashboard
    
    def log_weight(self,weight,popup):
        # Code to log weight
        try:
            weight = float(weight)
            utils.log_weight(weight=weight)
            print("Logged Weight:", weight)
        except ValueError:
            messagebox.showerror("Error","Please enter valid number, weight NOT logged")
        popup.destroy()
        self.setup_topleft(redraw=True)


    def log_calories_popup(self):
        popup = tk.Toplevel(self.root)
        popup.configure(bg=csts.BG_COLOR)
        popup.title("Log Calories")
        # Calculating the position to center the popup over the parent window.
        window_width = popup.winfo_reqwidth()
        window_height = popup.winfo_reqheight()
        
        position_right = int(self.root.winfo_screenwidth()/2 - window_width/2)
        position_down = int(self.root.winfo_screenheight()/2 - window_height/2)
        
        
        # Positions the window in the center of the page.
        popup.geometry(f"+{position_right}+{position_down}")
        
        label = tk.Label(popup, text="Enter Calories:")
        label.configure(bg=csts.BG_COLOR,fg=csts.FG_COLOR,font=csts.FONT)
        label.pack()
        
        weight_var = tk.StringVar()
        entry = tk.Entry(popup, textvariable=weight_var)
        entry.configure(bg=csts.BG_COLOR,fg=csts.FG_COLOR,font=csts.FONT)
        entry.pack()
        entry.focus_set()
        
        
        submit_btn = self.create_button(parent=popup, text="Submit", command=lambda: self.log_calories(weight_var.get(), popup))
        submit_btn.pack()
        
        popup.bind('<Return>',lambda event: self.log_calories(weight_var.get(), popup))
        popup.grab_set() #makes popup modal, aka user must interact with popup before
        #making more inputs to the dashboard

    def log_calories(self,calories,popup,event=None):
        # Code to log calories
        try:
            calories = float(calories)
            self.user.todays_calories += calories
            print("Logged calories:", calories)
            print(f"total logged: {self.user.todays_calories}")
            frameutils.log_calories(calories=calories)
        except ValueError:
            messagebox.showerror("Error","Please enter valid number, calories NOT logged")
        popup.destroy()
        self.setup_centermid(redraw=True)

    def third_command(self):
        # Code for the third button
        print("Third Button Clicked")

    def fourth_command(self):
        # Code for the fourth button
        print("Fourth Button Clicked")



    def create_label(self,parent,text):
        lbl = tk.Label(master=parent,text=text)
        lbl.configure(bg=csts.BG_COLOR,fg=csts.FG_COLOR,font=csts.FONT)
        return lbl
    

    def on_closing(self):
        if self.after_id_centermid:
            self.root.after_cancel(self.after_id_centermid)
        if self.after_id_topleft:
            self.root.after_cancel(self.after_id_topleft)
        try:
            self.root.destroy()
        except Exception as err:
            print(err)
            traceback.print_exc()
            print("error destroying root!!")
        # sys.exit(0)
        # pdb.set_trace()