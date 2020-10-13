import os
import tkinter as tk

from tkinter import ttk
from assets.sorter_script import Sorter, Remover

# INITIALISING CLASSES
sorter = Sorter()
remover = Remover()

# BUTTON FUNCTIONS
def choose_sort_type(event):
    """Sets sort type and runs date_year_selection.

    Replaces select_sort_type from Sorter class, as this program uses a dropdown menu instead.
    """
    # .lower because items in dropdown are capitalised
    sorter.sort_type = sort_var.get().lower()

    if sorter.sort_type == "date":
        sorter.date_year_selection()


def choose_folder(event):
    """Executes select_folder method from Sorter class and sets text in label to show new directory path"""

    sorter.select_folder()
    sort4["text"] = sorter.sorted_folder
    if sorter.sorted_folder == "":
        sort4["text"] = "Warning! Please select folder."


def reset_folder():
    for folder in sorter.folders:
        path = sorter.sorted_folder + str(folder)
        if not os.path.exists(path):
            console["text"] = "Please check folders exist.\nMake sure to select options so that same folders as the ones that exist would be created\ni.e. same sort type and same earliest year if date is chosen."
            break
    else:
        remover.undo_folders(sorter.sorted_folder,
                             sorter.sort_type, sorter.folders)
        console["text"] = "Folder reset"


def final_sort():
    if sorter.sorted_folder == "./":
        console["text"] = "Please select a folder to sort first."
    else:
        try:
            sorter.sort_files(sorter.sort_type)
            console["text"] = "Sort folders created.\n\nAll files sorted successfully!\n\nTo undo these changes press reset button to the right.\n\nTo sort further, select another folder."
        except OSError:
            console["text"] = "There was a problem sorting the files.\nPlease make sure a path is selected for the folder."


# GUI ------------------------------------------------------------------------------------------------------------------------------------------------------------------
root = tk.Tk()

# BASE
root.geometry("450x400")
root.title("Download Folder File Sorter")
root.tk.call('wm', 'iconphoto', root._w,
             tk.PhotoImage(file='./assets/icon.ico'))

# main background
bg = tk.Label(root, bg="black")
bg.place(relwidth=1, relheight=1)

# frame
frame1 = tk.Frame(root)
frame1.place(relx=0.015, rely=0.015, relwidth=0.97, relheight=0.97)
frame1_background = tk.Label(frame1, bg="black")
frame1_background.place(relwidth=1, relheight=1)

# Constants
label_font = ("Helvetica", 12, "bold")
small_font = ("Helvetica", 9)
description_font = ("Helvetica", 12)
cursor = "hand2"

# Variables
sort_menu = [None, "File Type", "Date"]
sort_var = tk.StringVar()
sort_var.set(sort_menu[1])

# LABELS
console_bg = tk.Label(frame1)
console_bg.place(relx=0.025, rely=0.45, relwidth=0.95, relheight=0.5)
console = tk.Label(frame1, bg="gray", font=small_font, text="Ready to sort files.\n\nPlease remember to undo sort folders BEFORE changing\nsort type, if files have already been sorted.\nButton to remove sort folders and move files back to original folder\ncan be found directly above (Reset folder button).\n\nOptions above to select folder being sorted and\nwhat to sort files by.")
console.place(relx=0.05, rely=0.5, relwidth=0.9, relheight=0.4)

choose_sort_label = tk.Label(frame1, text="Sort type: ", font=label_font)
choose_sort_label.place(relwidth=0.2, relheight=0.1, relx=0.025, rely=0.15)

sort3 = tk.Label(frame1, text="Folder to be sorted:", font=label_font)
sort3.place(relwidth=0.35, relheight=0.1, relx=0.025, rely=0.025)

sort4 = tk.Label(frame1, text="Select a folder",
                 font=small_font, cursor=cursor)
sort4.place(relwidth=0.6, relheight=0.1, relx=0.375, rely=0.025)
sort4.bind("<Button-1>", choose_folder)

# BUTTONS AND DROPDOWN
choose_sort_type_drop = ttk.OptionMenu(
    frame1, sort_var, *sort_menu, command=choose_sort_type)
choose_sort_type_drop.place(relx=0.225, rely=0.15, relwidth=0.4, relheight=0.1)

sort_files_button = ttk.Button(
    frame1, text="Sort files", cursor=cursor, command=final_sort)
sort_files_button.place(relwidth=0.2, relheight=0.1, relx=0.675, rely=0.15)

undo_folders_button = ttk.Button(
    frame1, text="Reset folder", cursor=cursor, command=reset_folder)
undo_folders_button.place(relwidth=0.2, relheight=0.1, relx=0.4, rely=0.3)


root.mainloop()
