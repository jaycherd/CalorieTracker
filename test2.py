import tkinter as tk
from tkinter import ttk

class CustomEntry(ttk.Entry):
    def __init__(self, parent, autocomplete_list, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.listbox = None
        self.autocomplete_list = sorted(autocomplete_list, key=str.lower)  # Sort the list

        self.bind("<Return>", self.check_input)
        self.bind("<FocusOut>", self.destroy_listbox)

    def check_input(self, event=None):
        if self.listbox:
            self.listbox.destroy()
            self.listbox = None
            
        entered_value = self.get()
        
        if len(entered_value) == 0:
            return

        matching_items = [item for item in self.autocomplete_list if entered_value.lower() in item.lower()]
        
        if len(matching_items) == 0:
            return
        
        self.listbox = tk.Listbox(self.master)
        self.listbox.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
        
        for item in matching_items:
            self.listbox.insert(tk.END, item)
        
        self.listbox.bind("<Button-1>", self.set_entry_from_listbox)
        
    def set_entry_from_listbox(self, event=None):
        if self.listbox:
            current_selection = self.listbox.curselection()
            if current_selection:
                self.delete(0, tk.END)
                self.insert(0, self.listbox.get(current_selection))
            self.listbox.destroy()
            self.listbox = None

    def destroy_listbox(self, event=None):
        if self.listbox:
            self.listbox.destroy()
            self.listbox = None

class Dashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dashboard")
        
        # Here's an example frame in your dashboard
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(pady=20)

        # Create an instance of the CustomEntry inside the frame
        autocomplete_list = ["apple", "banana", "pear", "pineapple", "peach", "plum", "pomegranate", "papaya"]
        self.entry = CustomEntry(self.main_frame, autocomplete_list)
        self.entry.pack()

app = Dashboard()
app.mainloop()
