import tkinter as tk
from tkinter import ttk

combo_list = ["Subscribe", "Not Subscribed", "Other"]

#__________________________________________________fUNCTIONS___________________________________________________________

def toggle_mode():
    if mode_switch.instate(["selected"]):
        style.theme_use("forest-light")
        root.config(bg="white")
    else:
        style.theme_use("forest-dark")
        root.config(bg="#2B2B2B")

def load_data():
    cols = ("Name", "Age", "Subscription", "Employment")
    for value in cols:
        treeview.heading(value, text=value)

    treeview.insert("","end", values=("Luis", "35", "Subscribed", "Employed"))
#________________________________________________GUI__________________________________________________________________

root = tk.Tk()
root.config(bg="#2B2B2B")

style = ttk.Style(root)
root.tk.call("source", "forest-dark.tcl")
root.tk.call("source", "forest-light.tcl")
style.theme_use("forest-dark")


frame = ttk.Frame(root)
frame.pack()

#______________________________________________widgets Frame_______________________________________________________
widgets_frame = ttk.LabelFrame(frame, text="Insert Row")
widgets_frame.grid(column=0, row=0, padx=20, pady=10)

name_entry = ttk.Entry(widgets_frame)
name_entry.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
name_entry.insert(0, string="name")
name_entry.bind("<FocusIn>", lambda e: name_entry.delete(0, "end"))

age_spinbox = ttk.Spinbox(widgets_frame, from_=18, to=100)
age_spinbox.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
age_spinbox.insert(0, "Age")

status_combobox = ttk.Combobox(widgets_frame, values=combo_list)
status_combobox.current(0)
status_combobox.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

a = tk.BooleanVar()
check_button = ttk.Checkbutton(widgets_frame, text="Employed", variable=a)
check_button.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)

button = ttk.Button(widgets_frame, text="Insert")
button.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)

separator = ttk.Separator(widgets_frame)
separator.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

mode_switch = ttk.Checkbutton(widgets_frame, text="Mode", style="Switch", command= toggle_mode)
mode_switch.grid(row=6, column=0, padx=5, pady=5, sticky="nsew")

#_______________________________________tree Frame __________________________________________________________________

tree_frame = ttk.Frame(frame)
tree_frame.grid(row=0, column=1, padx=10, pady=10)
tree_scrollbar = ttk.Scrollbar(tree_frame)
tree_scrollbar.pack(side="right", fill="y")

cols = ("Name", "Age", "Subscription", "Employment")
treeview = ttk.Treeview(tree_frame, show="headings", yscrollcommand=tree_scrollbar.set,  columns=cols, height=13)
treeview.column("Name", width=100)
treeview.column("Age", width=50)
treeview.column("Subscription", width=100)
treeview.column("Employment", width=100)
treeview.pack()
tree_scrollbar.config(command=treeview.yview)

load_data()

root.mainloop()