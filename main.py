import tkinter as tk
from tkinter import ttk
import pandas
import os.path as path
from tkinter import messagebox
import datetime
filter_list = ["All", "Asset Group", "Location", "District", "Cell"]

header_dict = {
    "SN": [None],
    "Asset Name": [None],
    "Asset Group": [None],
    "Description": [None],
    "Location": [None],
    "District": [None],
    "Cell": [None],
    "Op Status": [None],

}

maintenance_dict = {
    "SN": [None],
    "Asset Name": [None],
    "Date": [None],
    "Event": [None],
    "User": [None],
    "Op Status": [None],
    }

asset_data = pandas.DataFrame(header_dict)
maintenance_data = pandas.DataFrame(maintenance_dict)

#__________________________________________________fUNCTIONS___________________________________________________________
def filter_select_combobox_values():
    global asset_data
    filter_combobox_current = filter_combobox.get()
    if filter_combobox_current == "All":
        filter_select_combobox.config(values=["All"])
    elif filter_combobox_current == "Asset Group":
        new_list=[]
        [new_list.append(item) for item in asset_data["Asset Group"].tolist() if item not in new_list]
        filter_select_combobox.config(values=new_list)

    elif filter_combobox_current == "Location":
        new_list=[]
        [new_list.append(item) for item in asset_data["Location"].tolist() if item not in new_list]
        filter_select_combobox.config(values=new_list)

    elif filter_combobox_current == "District":
        new_list=[]
        [new_list.append(item) for item in asset_data["District"].tolist() if item not in new_list]
        filter_select_combobox.config(values=new_list)

    elif filter_combobox_current == "Cell":
        new_list=[]
        [new_list.append(item) for item in asset_data["Cell"].tolist() if item not in new_list]
        filter_select_combobox.config(values=new_list)

def toggle_mode():
    if mode_switch.instate(["selected"]):
        style.theme_use("forest-light")
        root.config(bg="white")
    else:
        style.theme_use("forest-dark")
        root.config(bg="#2B2B2B")

def load_data():
    global asset_data
    global header_dict
    global maintenance_data
    global maintenance_dict

    if path.exists("./tool_asset_managment_data.csv"):
        asset_data = pandas.read_csv("./tool_asset_managment_data.csv", index_col=0)
        load_tree(asset_data)
    else:
        asset_data = pandas.DataFrame(header_dict)
        asset_data.to_csv("./tool_asset_managment_data.csv")
        load_tree(asset_data)

    if path.exists("./maintenance_data.csv"):
        maintenance_data = pandas.read_csv("./maintenance_data.csv", index_col=0)
        load_maintenance_tree(maintenance_data)
    else:
        maintenance_data = pandas.DataFrame(maintenance_dict)
        maintenance_data.to_csv("./maintenance_data.csv")
        load_maintenance_tree(maintenance_data)


def load_tree(fasset_data):
    for item in treeview.get_children():
        treeview.delete(item)
    header_list = fasset_data.columns.values.tolist()
    for value in header_list:
        treeview.heading(value, text=value)

    sn_list = fasset_data.SN.tolist()
    for sn in sn_list:
        row_data_list = fasset_data[fasset_data.SN == sn].values.flatten().tolist()
        treeview.insert("", "end", values=row_data_list)

def load_maintenance_tree(fmaintenance_data):

    for item in mant_treeview.get_children():
        mant_treeview.delete(item)
    header_list = ["Date", "Event", "User", "Op Status"]
    for value in header_list:
        mant_treeview.heading(value, text=value)

    sn_list = fmaintenance_data.SN.tolist()

    i=0
    for sn in sn_list:
        if sn == search_entry.get():
            row_data_list = fmaintenance_data[fmaintenance_data.SN == sn].values.tolist()[i]
            i+=1
            mant_treeview.insert("", "end", values=row_data_list[2:])

def search():
    global filter_list
    global asset_data
    global maintenance_data

    if search_entry.get() in asset_data.SN.tolist():

        temp_asset_data = asset_data[asset_data["SN"] == search_entry.get()]
        load_tree(temp_asset_data)

        temp_maintenance_data =maintenance_data[maintenance_data["SN"] == search_entry.get()]
        load_maintenance_tree(temp_maintenance_data)

        # this will update label in maintenance event window
        maintenance_sn_label.config(text=f"SN: {search_entry.get()}         Asset Name: {asset_data.loc[asset_data.index[asset_data['SN'] == search_entry.get()].tolist()[0], 'Asset Name']}")

    elif filter_combobox.get() in filter_list[1:] and filter_select_combobox.get() != "All":

        temp_asset_data =asset_data[asset_data[filter_combobox.get()]==filter_select_combobox.get()]
        load_tree(temp_asset_data)
        load_maintenance_tree(maintenance_data)

    else:
        load_tree(asset_data)
        load_maintenance_tree(maintenance_data)

        maintenance_sn_label.config(text=f"SN:          Asset Name: ")
        messagebox.showwarning(message=f"SN: {search_entry.get()} doesn't exist")


def insert_asset():
    tree_frame.grid_remove()
    move_frame.grid_remove()
    maintenance_tree_frame.grid_remove()
    insert_frame.grid()

def move_asset():
    tree_frame.grid_remove()
    insert_frame.grid_remove()
    maintenance_tree_frame.grid_remove()
    move_frame.grid()

    selected_item = treeview.focus()
    details = treeview.item(selected_item)

    if details["values"] != "":

        sn_move_entry.delete(0, "end")
        asset_group_opt2_combobox.delete(0, "end")
        location_opt2_combobox.delete(0, "end")
        district_opt2_combobox.delete(0, "end")
        cell_opt2_combobox.delete(0, "end")
        search_entry.delete(0, "end")

        sn_move_entry.insert(0, details["values"][0])
        asset_group_opt2_combobox.insert(0, details["values"][2])
        location_opt2_combobox.insert(0, details["values"][4])
        district_opt2_combobox.insert(0, details["values"][5])
        cell_opt2_combobox.insert(0, details["values"][6])
        search_entry.insert(0, details["values"][0])

def home():
    insert_frame.grid_remove()
    move_frame.grid_remove()
    maintenance_tree_frame.grid_remove()
    tree_frame.grid()

def maintenance_event():
    insert_frame.grid_remove()
    move_frame.grid_remove()
    tree_frame.grid_remove()
    maintenance_tree_frame.grid()

    selected_item = treeview.focus()
    details = treeview.item(selected_item)

    if details["values"] != "":

        search_entry.delete(0, "end")
        search_entry.insert(0, details["values"][0])
        maintenance_sn_label.config(text=f"SN: {search_entry.get()}         Asset Name: {asset_data.loc[asset_data.index[asset_data['SN']==search_entry.get()].tolist()[0], 'Asset Name']}")
        load_maintenance_tree(maintenance_data)

def insert_asset_data():
    global cols
    global asset_data

    insert_dict = {
    "SN": sn_entry.get(),
    "Asset Name": asset_name_entry.get(),
    "Asset Group": asset_group_combobox.get(),
    "Description": description_entry.get(),
    "Location": location_combobox.get(),
    "District": district_combobox.get(),
    "Cell": cell_combobox.get(),
    "Op Status": op_status_combobox.get(),

    }

    if "" not in insert_dict.values() and sn_entry.get() not in asset_data.SN.tolist():
        ask_user_insert = messagebox.askokcancel(title="Save new Asset", message="Click OK to save new Asset")


        if ask_user_insert:

            asset_data.loc[len(asset_data)] = insert_dict
            asset_data = asset_data.reset_index(drop=True)

            asset_data.to_csv("/Users/USER/Desktop/tool_asset_managment_data.csv")
            load_tree(asset_data)

            sn_entry.delete(0, "end")
            asset_name_entry.delete(0, "end")
            description_entry.delete(0,"end")

    elif sn_entry.get() in asset_data.SN.tolist():
        messagebox.showwarning(message=f"SN: {sn_entry.get()} \n already exist")

    elif "" in insert_dict.values():
        messagebox.showwarning(message="Please insert empty fields")

def assign_asset():

    global asset_data

    if sn_move_entry.get() == "" or asset_move_group_combobox.get() == "":
        messagebox.showwarning(message="Please insert empty fields")

    elif sn_move_entry.get() not in asset_data.SN.tolist():
        messagebox.showwarning(message=f"SN: {sn_move_entry.get()} doesn't exist")

    elif sn_move_entry.get() in asset_data.SN.tolist():
        ask_user_move = messagebox.askokcancel(title="Save", message=f"Assign {sn_move_entry.get()} to {asset_move_group_combobox.get()}")
        if ask_user_move:
            asset_data.loc[asset_data.index[asset_data["SN"]==sn_move_entry.get()].tolist()[0], "Asset Group"] = asset_move_group_combobox.get()
            update_data()

def move_asset_button():

    if asset_group_opt2_combobox.get() =="" or location_opt2_combobox.get() == "" or district_opt2_combobox.get() == "" or cell_opt2_combobox.get() == "":
        messagebox.showwarning(message="Please insert empty fields")

    elif asset_group_opt2_combobox.get() not in asset_data["Asset Group"].tolist():
        messagebox.showwarning(message=f"{asset_group_opt2_combobox.get()} doesn't exist")

    elif asset_group_opt2_combobox.get() in asset_data["Asset Group"].tolist():

        ask_user_tomove = messagebox.askokcancel(title="Save", message=f"{asset_group_opt2_combobox.get()}\nmove to:\nLocation: {location_opt2_combobox.get()}"
                                                                       f"\nDistrict: {district_opt2_combobox.get()}\nCell: {cell_opt2_combobox.get()}")

        if ask_user_tomove:

            asset_data.loc[asset_data.index[asset_data["Asset Group"] == asset_group_opt2_combobox.get()].tolist(), "Location"] = location_opt2_combobox.get()
            asset_data.loc[asset_data.index[asset_data["Asset Group"] == asset_group_opt2_combobox.get()].tolist(), "District"] = district_opt2_combobox.get()
            asset_data.loc[asset_data.index[asset_data["Asset Group"] == asset_group_opt2_combobox.get()].tolist(), "Cell"] = cell_opt2_combobox.get()
            update_data()

def create_maintenance_event():
    global maintenance_data

    if search_entry.get()=="" or maintenance_event_entry.get() == "" or maintenance_user_entry.get() == "" or maintenance_status_combobox.get() == "":
        messagebox.showwarning(message="Please insert empty fields")

    elif search_entry.get() not in asset_data.SN.tolist():
        messagebox.showwarning(message=f"{search_entry.get()}, doesn't exist")

    elif search_entry.get() in asset_data.SN.tolist():

        maintenance_dict_insert = {
            "SN": search_entry.get(),
            "Asset Name": asset_data.loc[asset_data.index[asset_data['SN'] == search_entry.get()].tolist()[0], 'Asset Name'],
            "Date": datetime.datetime.now().date(),
            "Event": maintenance_event_entry.get(),
            "User": maintenance_user_entry.get(),
            "Op Status": maintenance_status_combobox.get(),
        }

        ask_user_create_event = messagebox.askokcancel(title="save", message="create maintenance event")

        if ask_user_create_event:

            maintenance_data.loc[len(maintenance_data)]= maintenance_dict_insert
            maintenance_data = maintenance_data.reset_index(drop=True)
            maintenance_data.to_csv("/Users/USER/Desktop/maintenance_data.csv")
            load_maintenance_tree(maintenance_data)
            maintenance_event_entry.delete(0, "end")

            #changing the op status of the asset in the databa
            asset_data.loc[asset_data.index[asset_data.SN == search_entry.get()], "Op Status"] = maintenance_status_combobox.get()
            update_data()

def get_option_combolist(combolist):
    global asset_data
    asset_group_combobox_list = []
    location_combobox_list = []
    cell_combobox_list = []
    district_combobox_list = []

    if path.exists("/Users/USER/Desktop/tool_asset_managment_data.csv"):
        asset_data = pandas.read_csv("/Users/USER/Desktop/tool_asset_managment_data.csv")

        if combolist == "Location":
            [location_combobox_list.append(item) for item in asset_data["Location"].tolist() if item not in location_combobox_list]
            return location_combobox_list[1:]
        elif combolist == "District":
            [district_combobox_list.append(item) for item in asset_data["District"].tolist() if item not in district_combobox_list]
            return district_combobox_list[1:]
        elif combolist == "Cell":
            [cell_combobox_list.append(item) for item in asset_data["Cell"].tolist() if item not in cell_combobox_list]
            return cell_combobox_list[1:]
        elif combolist == "Asset Group":
            [asset_group_combobox_list.append(item) for item in asset_data["Asset Group"].tolist() if item not in asset_group_combobox_list]
            return asset_group_combobox_list[1:]

    else:
        return []

def update_data():
    global asset_data
    asset_data.to_csv("/Users/USER/Desktop/tool_asset_managment_data.csv")
    load_tree(asset_data)

#________________________________________________GUI__________________________________________________________________

root = tk.Tk()
root.title("Asset Tracker")
root.config(bg="#2B2B2B")

style = ttk.Style(root)
root.tk.call("source", "forest-dark.tcl")
root.tk.call("source", "forest-light.tcl")
style.theme_use("forest-dark")

frame = ttk.Frame(root)
frame.pack()

#______________________________________________widgets Frame_______________________________________________________
widgets_frame = ttk.LabelFrame(frame, text="Search")
widgets_frame.grid(column=0, row=1, padx=20, pady=10)

filter_combobox = ttk.Combobox(widgets_frame, values=filter_list)
filter_combobox.current(0)
filter_combobox.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

filter_select_combobox = ttk.Combobox(widgets_frame, postcommand=filter_select_combobox_values)
filter_select_combobox.insert(0, "All")
filter_select_combobox.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

search_entry = ttk.Entry(widgets_frame)
search_entry.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
search_entry.insert(0, string=" SN")
search_entry.bind("<FocusIn>", lambda e: search_entry.delete(0, "end"))

search_button = ttk.Button(widgets_frame, text="Search", command=search)
search_button.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)

separator = ttk.Separator(widgets_frame)
separator.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

mode_switch = ttk.Checkbutton(widgets_frame, text="Mode", style="Switch", command= toggle_mode)
mode_switch.grid(row=5, column=0, padx=5, pady=5, sticky="nsew")

#_______________________________________tree Frame __________________________________________________________________

tree_frame = ttk.Frame(frame)
tree_frame.grid(row=1, column=1, padx=10, pady=10)

tree_scrollbar = ttk.Scrollbar(tree_frame)
tree_scrollbar.pack(side="right", fill="y")

cols = ("SN", "Asset Name", "Asset Group", "Description", "Location", "District", "Cell", "Op Status")
treeview = ttk.Treeview(tree_frame, show="headings", yscrollcommand=tree_scrollbar.set, columns=cols, height=20)
treeview.column("SN", width=100)
treeview.column("Asset Name", width=100)
treeview.column("Asset Group", width=100)
treeview.column("Description", width=100)
treeview.column("Location", width=100)
treeview.column("District", width=100)
treeview.column("Cell", width=100)
treeview.column("Op Status", width=100)
treeview.pack()
tree_scrollbar.config(command=treeview.yview)

#______________________________________Function Buttons________________________________________________________________

function_buttons_frame = ttk.Frame(frame)
function_buttons_frame.grid(row=0, column=1)

home_button = ttk.Button(function_buttons_frame)
home_button.config(text="Home", width=20, command=home)
home_button.grid(column=0, row=0, padx=10, pady=10)

insert_button = ttk.Button(function_buttons_frame)
insert_button.config(text="Insert Asset", width=20, command=insert_asset)
insert_button.grid(column=1, row=0, padx=10, pady=10)

move_button = ttk.Button(function_buttons_frame)
move_button.config(text="Move Asset", width=20, command=move_asset)
move_button.grid(column=2, row=0, padx=10, pady=10)

maintenance_button = ttk.Button(function_buttons_frame, command=maintenance_event)
maintenance_button.config(text="Maintenance Event", width=20)
maintenance_button.grid(column=3, row=0, padx=10, pady=10)

comfig_button = ttk.Button(function_buttons_frame)
comfig_button.config(text="Config", width=20)
comfig_button.grid(column=4, row=0, padx=10, pady=10)

#_______________________________________________Insert Frame_________________________________________________________

insert_frame = ttk.Frame(frame)
insert_frame.grid(row=1, column=1, padx=10, pady=10)

label_insert_frame = ttk.LabelFrame(insert_frame, text="Insert Asset")
label_insert_frame.grid(column=0, row=0, padx=20, pady=10)

sn_label = ttk.Label(label_insert_frame, text="SN:")
sn_label.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

asset_name_label = ttk.Label(label_insert_frame, text="Asset Name:")
asset_name_label.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

asset_group_label = ttk.Label(label_insert_frame, text="Asset Group:")
asset_group_label.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

description_label = ttk.Label(label_insert_frame, text="Description:")
description_label.grid(row=3, column=0, sticky="ew", padx=5, pady=5)

location_label = ttk.Label(label_insert_frame, text="Location:")
location_label.grid(row=4, column=0, sticky="ew", padx=5, pady=5)

district_label = ttk.Label(label_insert_frame, text="District:")
district_label.grid(row=5, column=0, sticky="ew", padx=5, pady=5)

cell_label = ttk.Label(label_insert_frame, text="Cell:")
cell_label.grid(row=6, column=0, sticky="ew", padx=5, pady=5)

op_status_label = ttk.Label(label_insert_frame, text="Op Status:")
op_status_label.grid(row=7, column=0, sticky="ew", padx=5, pady=5)


sn_entry = ttk.Entry(label_insert_frame, width=20)
sn_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

asset_name_entry = ttk.Entry(label_insert_frame, width=40)
asset_name_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

asset_group_combobox = ttk.Combobox(label_insert_frame, width=40, values=get_option_combolist("Asset Group"))
if get_option_combolist("Asset Group") != []: asset_group_combobox.current(0)
asset_group_combobox.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

description_entry = ttk.Entry(label_insert_frame, width=40)
description_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

location_combobox = ttk.Combobox(label_insert_frame, width=40, values=get_option_combolist("Location"))
if get_option_combolist("Location") != []: location_combobox.current(0)
location_combobox.grid(row=4, column=1, sticky="ew", padx=5, pady=5)

district_combobox_list = ["Midland", "Victoria", "Pennsylvania"]
district_combobox = ttk.Combobox(label_insert_frame, width=40, values=district_combobox_list)
district_combobox.current(0)
district_combobox.grid(row=5, column=1, sticky="ew", padx=5, pady=5)

cell_combobox = ttk.Combobox(label_insert_frame, width=40, values=get_option_combolist("Cell"))
if get_option_combolist("Cell") != []: cell_combobox.current(0)
cell_combobox.grid(row=6, column=1, sticky="ew", padx=5, pady=5)

op_status_combobox_list = ["Good", "Warning", "Bad"]
op_status_combobox = ttk.Combobox(label_insert_frame, width=40, values=op_status_combobox_list)
op_status_combobox.current(0)
op_status_combobox.grid(row=7, column=1, sticky="ew", padx=5, pady=5)

insert_asset_button = ttk.Button(label_insert_frame, text="Insert Asset", command=insert_asset_data)
insert_asset_button.grid(row=8, column=1, sticky="ew", padx=5, pady=5)

#_____________________________________________________Move Asset GUI__________________________________________________

move_frame = ttk.Frame(frame)
move_frame.grid(row=1, column=1, padx=10, pady=10)

label_move_frame = ttk.LabelFrame(move_frame, text="Option 1: Assign Asset to an Asset Group")
label_move_frame.grid(column=0, row=0, padx=20, pady=10)

sn_move_label = ttk.Label(label_move_frame, text="SN:")
sn_move_label.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

assign_asset_move_label = ttk.Label(label_move_frame, text="Assign Asset to Group:")
assign_asset_move_label.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

asset_group_move_label = ttk.Label(label_move_frame, text="Asset Group:")
asset_group_move_label.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

sn_move_entry = ttk.Entry(label_move_frame, width=40)
sn_move_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

asset_move_group_combobox = ttk.Combobox(label_move_frame, width=40, values=get_option_combolist("Asset Group"))
if get_option_combolist("Asset Group") != []: asset_move_group_combobox.current(0)
asset_move_group_combobox.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

assign_asset_button = ttk.Button(label_move_frame, text="Assign Asset", command=assign_asset)
assign_asset_button.grid(row=3, column=1, sticky="ew", padx=5, pady=5)


label_move_group_frame = ttk.LabelFrame(move_frame, text="Option 2: Move Asset group to [Client / District / Cell]")
label_move_group_frame.grid(column=0, row=1, padx=20, pady=10)

asset_group_move_label_opt2 = ttk.Label(label_move_group_frame, text="Asset Group:")
asset_group_move_label_opt2.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

location_opt2_label = ttk.Label(label_move_group_frame, text="Assign Asset Group to Location:")
location_opt2_label.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

district_opt2_label = ttk.Label(label_move_group_frame, text="Assign Asset Group to District:")
district_opt2_label.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

cell_opt2_label = ttk.Label(label_move_group_frame, text="Assign Asset Group to Cell:")
cell_opt2_label.grid(row=3, column=0, sticky="ew", padx=5, pady=5)


asset_group_opt2_combobox = ttk.Combobox(label_move_group_frame, width=40, values=get_option_combolist("Asset Group"))
if get_option_combolist("Asset Group") != []: asset_group_opt2_combobox.current(0)
asset_group_opt2_combobox.grid(row=0, column=1, sticky="ew", padx=5, pady=5)


location_opt2_combobox = ttk.Combobox(label_move_group_frame, width=40, values=get_option_combolist("Location"))
if get_option_combolist("Location") != []: location_opt2_combobox.current(0)
location_opt2_combobox.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

district_opt2_combobox = ttk.Combobox(label_move_group_frame, width=40, values=district_combobox_list)
district_opt2_combobox.current(0)
district_opt2_combobox.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

cell_opt2_combobox = ttk.Combobox(label_move_group_frame, width=40, values=get_option_combolist("Cell"))
if get_option_combolist("Cell") != []: cell_opt2_combobox.current(0)
cell_opt2_combobox.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

move_asset_button = ttk.Button(label_move_group_frame, text="Move", command=move_asset_button)
move_asset_button.grid(row=4, column=1, sticky="ew", padx=5, pady=5)

#_____________________________________________________Maintenance Event GUI___________________________________________

maintenance_tree_frame = ttk.Frame(frame)
maintenance_tree_frame.grid(row=1, column=1, padx=10, pady=10)

maintenance_sn_label = ttk.Label(maintenance_tree_frame, text="SN:                                    Asset Name:")
maintenance_sn_label.config(width=120)
maintenance_sn_label.pack(padx=5, pady=5)

maintenance_tree_scrollbar = ttk.Scrollbar(maintenance_tree_frame)
maintenance_tree_scrollbar.pack(side="right", fill="y")

maintenance_header = ("Date", "Event", "User", "Op Status")
mant_treeview = ttk.Treeview(maintenance_tree_frame, show="headings", yscrollcommand=maintenance_tree_scrollbar.set,
                             columns=maintenance_header, height=10)
mant_treeview.column("Date", width=100)
mant_treeview.column("Event", width=600)
mant_treeview.column("User", width=100)
mant_treeview.column("Op Status", width=100)
mant_treeview.pack()
maintenance_tree_scrollbar.config(command=treeview.yview)


create_maintenance_label = ttk.LabelFrame(maintenance_tree_frame, text="Create new Maintenance Event")
create_maintenance_label.pack(padx=20, pady=10)

maintenance_event_label = ttk.Label(create_maintenance_label, text="Maintenance Event:")
maintenance_event_label.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

maintenance_user_label = ttk.Label(create_maintenance_label, text="User:")
maintenance_user_label.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

maintenance_status_label = ttk.Label(create_maintenance_label, text="Op Status:")
maintenance_status_label.grid(row=2, column=0, sticky="ew", padx=5, pady=5)


maintenance_event_entry = ttk.Entry(create_maintenance_label, width=100)
maintenance_event_entry.grid(row=0, column=1, columnspan=5,  sticky="ew", padx=5, pady=5)

maintenance_user_entry = ttk.Entry(create_maintenance_label, width=20)
maintenance_user_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

maintenance_status_combobox = ttk.Combobox(create_maintenance_label, values=op_status_combobox_list, width=20)
maintenance_status_combobox.current(0)
maintenance_status_combobox.grid(row=2, column=1, sticky="ew", padx=5, pady=5)


create_maintenance_event_button = ttk.Button(create_maintenance_label, text="Create Maintenance Event", command=create_maintenance_event)
create_maintenance_event_button.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

#_____________________________________________________Load Data and Initialize_________________________________________

load_data()
insert_frame.grid_remove()
move_frame.grid_remove()
maintenance_tree_frame.grid_remove()
#_____________________________________________________Closing________________________________________________________

root.mainloop()