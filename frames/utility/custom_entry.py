import tkinter as tk
from tkinter import ttk
from tkinter import messagebox,simpledialog
from icecream import ic
import threading

from frames.utility import constants_dashboard as cdash
from frames.utility import querying as query
from frames.utility.utility_fxns import log_food

class CustomEntry(ttk.Entry):
    def __init__(self, parent, name_id_tuples=None, *args, **kwargs):
        parent_w = parent.winfo_width()
        self.desired_w = int(parent_w * 0.8)
        average_char_w_pixels = 10
        self.desired_w = self.desired_w//average_char_w_pixels
        super().__init__(parent, *args,width=self.desired_w,font=cdash.FONTSMED, **kwargs)
        self.listbox = None
        self.name_id_tuples =  name_id_tuples
        #sorted(name_id_tuples, key=str.lower)  # Sort the list
        self.product_dictionary = {} # --> Dict[Dict]
        self.food_chosen_dict = {} # --> Dict

        self.bind("<Return>", self.check_input)
        self.bind("<FocusOut>", self.destroy_listbox)

    def check_input(self, event=None):
        if self.listbox:
            self.listbox.destroy()
            self.listbox = None
        entered_value = self.get()
        
        if len(entered_value) == 0:
            return
        
        # Display a loading message
        self.loading_label = tk.Label(self.master, text="Loading...", font=cdash.FONTSMED)
        self.loading_label.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())  # Adjust positioning as needed

        # Use threading to run the search without blocking the GUI! esp good during a timeout
        thread = threading.Thread(target=self.run_search, args=(entered_value,))
        thread.start()
        self.after(50, self.check_thread, thread)

    def run_search(self, entered_value):
        self.name_id_tuples,self.product_dictionary = query.search_for_food(entered_value)

    def check_thread(self, thread):
        if thread.is_alive():
            # Check again after 50 milliseconds
            self.after(50, self.check_thread, thread)
        else:
            # Thread has finished; remove the loading message
            self.loading_label.destroy()

            if len(self.name_id_tuples) == 0:
                messagebox.showerror("Error", "No items were found")
            else:
                # Create and display the listbox with the results
                self.listbox = tk.Listbox(self.master, width=self.desired_w, font=cdash.FONTSMED)
                self.listbox.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
                
                for item_name, _ in self.name_id_tuples:
                    self.listbox.insert(tk.END, item_name)
                
                self.listbox.bind("<<ListboxSelect>>", self.set_entry_from_listbox)
                self.listbox.bind("<FocusOut>", self.on_focus_out)

    def on_focus_out(self,event):
        ic("Listbox lost focus")
        
    def set_entry_from_listbox(self, event=None):
        if self.listbox:
            current_selection = self.listbox.curselection()
            if current_selection:
                selected_index = current_selection[0]
                selected_name, selected_id = self.name_id_tuples[selected_index]
                self.delete(0, tk.END)
                self.insert(0, selected_name)
                # You can now use selected_id to fetch details from products_dict, if needed
                print(f"user chose : {self.product_dictionary[selected_id]}")
                self.food_chosen_dict = self.product_dictionary[selected_id]
                if messagebox.askyesno("Confirmation",f"Log {self.food_chosen_dict['name']}? You can choose the amount next step"):
                    servings = simpledialog.askfloat("Input",f"Serving size ({self.food_chosen_dict['servingsize']}), how many servings?")
                    if servings is not None:
                        log_food(servings=servings,food_dict=self.food_chosen_dict)
            else:
                ic(type(current_selection))
            if self.listbox:
                self.listbox.destroy()
                self.listbox = None
    

    def destroy_listbox(self, event=None):
        if self.listbox:
            self.listbox.destroy()
            self.listbox = None



"""
NOTES - to implement
1 - Error Handling: Ensure that query.search_for_food(entered_value) handles potential errors, timeouts, or empty results gracefully.
    For example, if there's a timeout or the service isn't reachable, you might want to display a message to the user or provide default suggestions.
2 - Limiting Query Results: Depending on the volume of results query.search_for_food(entered_value) might return,
    consider limiting the number of results shown in the dropdown to a manageable number (like 10 or 20).
3 - Throttling or Debouncing the Search: Since the search is triggered every time the user presses "Enter",
    you might consider adding a small delay (like 200-300 milliseconds) and only searching if the user hasn't pressed another key in that time.
    This is especially useful if the search takes a while.
4 - Resize the Entry Box and List Drop Down: You can set the width of the entry box and listbox by using the width attribute.
    For the Entry widget:
"""