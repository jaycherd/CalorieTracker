import sys
import tkinter as tk
from tkinter import ttk,messagebox
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from frames.base_frame import BaseFrame
from frames import constants as csts
from frames.utility import constants_dashboard as cdash
from frames.utility import utility_fxns as frameutils
from user_data.user import User
from user_data.utility import utility_fxns as utils


class DashboardFrame(BaseFrame):
    def __init__(self,user: User,title="Super Sexy Dashboard"):
        super().__init__(title=title,iconpath=csts.DASHICO_PATH,
                         scr_h_pcnt=csts.DASH_H_PCNT,scr_w_pcnt=csts.DASH_W_PCNT,alter_mouse=True,mouse_type='dot')
        self.user = user
        self.redraw_centermid_flag = False

        self.topleft_frame = self.create_styled_frame(self.root, 0, 0, 0.5, 0.27)
        
        self.topright_frame = self.create_styled_frame(self.root, 0.5, 0, 0.5, 0.27, bg='light green')
        
        self.centerleft_frame = self.create_styled_frame(self.root, 0, 0.27, 0.25, 0.46, bg=csts.BG_COLOR)
        
        self.centermid_frame = self.create_styled_frame(self.root, 0.25, 0.27, 0.5, 0.46, bg=csts.BG_COLOR)
        
        self.centerright_frame = self.create_styled_frame(self.root, 0.75, 0.27, 0.25, 0.46, bg='light yellow')
        
        self.bottomleft_frame = self.create_styled_frame(self.root, 0, 0.73, 0.5, 0.27)
        
        self.bottomright_frame = self.create_styled_frame(self.root, 0.5, 0.73, 0.5, 0.27, bg='light coral')

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
        self.setup_bottomleft()
        self.setup_bottomright()

        self.loop_centermid_plot()


        

    def loop_centermid_plot(self):
        if self.redraw_centermid_flag:
            self.setup_centermid(redraw=True)
            self.redraw_centermid_flag = False
        self.after_id = self.root.after(1500,self.loop_centermid_plot)
        



    def create_styled_frame(self, parent, relx, rely, relwidth, relheight, bg='light blue'):
        frame = tk.Frame(parent, bg=bg)
        frame.place(relx=relx, rely=rely, relwidth=relwidth, relheight=relheight)
        return frame

    #want this frame to hold a weight log chart
    def setup_topleft(self):
        """
        if SHOW_LINEPLOT:
            years = [2006 + x for x in range(16)]
            weights = [80,83,84,85,86,82,81,79,83,80,
                    82,82,83,81,80,79]
            plt.plot(years,weights,c="b",lw=3,linestyle="--")
            plt.show()
        """
        #weights = List[weight], dates = List[datetime]
        weights,dates = frameutils.get_weights_datetimes_fromjson(cdash.WEIGHTLOG_PATH)
        fig,ax = plt.subplots()
        ax.plot(dates,weights)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d/%Y"))
        plt.xticks(rotation=45)
        # plt.tight_layout()
        plt.subplots_adjust(bottom=0.1)

        # Embed the plot in Tkinter frame
        canvas = FigureCanvasTkAgg(fig, master=self.topleft_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side='top',fill='both',expand=1)

    def setup_topright(self):
        pass

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

        label = tk.Label(self.centermid_frame, text="Today's Calories:")
        label.configure(bg=csts.BG_COLOR,fg=csts.FG_COLOR,font=csts.FONT)
        label.pack()

        fig = Figure(figsize=(5,5))
        fig.patch.set_facecolor(csts.BG_COLOR)
        ax = fig.add_subplot(111)
        ax.set_facecolor(csts.BG_COLOR)
        
        
        consumed = self.user.todays_calories
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
        wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct=lambda pct: func(pct, sizes), startangle=140, textprops={'color': 'black'})

        # defining color for labels
        label_color = csts.FG_COLOR  # or any other color you prefer

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
        # Additional setup for the center right frame.
        pass
    
    def setup_bottomleft(self):
        # Additional setup for the bottom left frame.
        pass
    
    def setup_bottomright(self):
        # Additional setup for the bottom right frame.
        pass


    def create_button(self, parent, text, command=None):
        button = tk.Button(parent, text=text, command=command)
        button.configure(bg=csts.BG_COLOR,fg=csts.FG_COLOR,font=csts.FONT,
                         borderwidth=cdash.CENTERLEFT_BRD_W,
                         highlightcolor=csts.MY_GREEN,activebackground=csts.MY_GREEN,
                         highlightbackground=csts.MY_BLUE)
        return button
    
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
        
        submit_btn = self.create_button(parent=popup, text="Submit", command=lambda: self.log_weight(weight_var.get(), popup))
        submit_btn.pack()

        popup.grab_set() #makes popup modal, aka user must interact with popup before
        #making more inputs to the dashboard
    
    def log_weight(self,weight,popup):
        # Code to log weight
        print("Logged Weight:", weight)
        try:
            weight = float(weight)
            utils.log_weight(weight=weight)
        except ValueError:
            messagebox.showerror("Error","Please enter valid number, weight NOT logged")
        popup.destroy()


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
        
        submit_btn = self.create_button(parent=popup, text="Submit", command=lambda: self.log_calories(weight_var.get(), popup))
        submit_btn.pack()

        popup.grab_set() #makes popup modal, aka user must interact with popup before
        #making more inputs to the dashboard

    def log_calories(self,calories,popup):
        # Code to log calories
        try:
            calories = float(calories)
            self.user.todays_calories += calories
            self.redraw_centermid_flag = True
            print("Logged calories:", calories)
            print(f"total logged: {self.user.todays_calories}")
        except ValueError:
            messagebox.showerror("Error","Please enter valid number, calories NOT logged")
        popup.destroy()

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
        if self.after_id:
            self.root.after_cancel(self.after_id)
        self.root.destroy()