import os
import time
import tkinter as tk
from datetime import datetime
from tkinter import ttk, filedialog


# SORTER-------------------------------------------------------------------------------------------------------------------------------------
class Sorter(object):
    """Contains functions for making sort folders and sorting files into those folders. Class variables are used by these functions."""

    # DEFAULTS AND CONSTANTS
    sort_type = "file type"
    # folder to be sorted
    sorted_folder = "./"
    # folders files will be sorted into
    folders = ["Set-up or Program Files",
               "Compressed Archives", "Images", "Text Files", "Other"]
    # Folders that will be emptied
    to_empty = folders
    # Earliest year if date sort type is used
    earliest = 2020
    # Current date
    today = datetime.today()
    # current year
    year = today.year
    # folder names in each year folder
    MONTHS = ["(1) Jan", "(2) Feb", "(3) Mar", "(4) Apr", "(5) May", "(6) Jun",
              "(7) Jul", "(8) Aug", "(9) Sep", "(10) Oct", "(11) Nov", "(12) Dec"]

    # METHODS
    def select_folder(self):
        """Pop up to ask user to select a directory to be sorted"""

        Sorter.sorted_folder = filedialog.askdirectory() + "/"

    def date_year_selection(self):
        """
        Sets earliest year to make folder for if date is chosen as the sort type.

        Requires main.py to have a ui using tkinter.
        """

        def validate_and_set_year(year):
            """Try block to validate year is an int"""

            try:
                year = int(year)
                today = datetime.today()
                if year > int(today.year) or year < 1900:
                    raise ValueError
                Sorter.earliest = year
                date_pop_up.destroy()
                Sorter.wait_for_me = False

            except ValueError:
                bad_entry = tk.Toplevel()
                bad_entry.wm_title("Error in year selection")
                bad_entry_label = tk.Label(
                    bad_entry, text="Please enter a valid year.\nMust be less than or equal to current year.")
                bad_entry_label.pack()
                bad_entry_button = ttk.Button(
                    bad_entry, text="Ok", command=bad_entry.destroy)
                bad_entry_button.pack()

        date_pop_up = tk.Toplevel()
        date_pop_up.wm_title("Year Selection")

        year_entry_label = tk.Label(date_pop_up, font=(
            "Helvetica", 10), text="Please enter the earliest year you want\nto create sorted folders for.\nFolders will be created from that year to the current year.\nPlease note that low numbers will create an\nexcessive amount of folders.")
        year_entry_label.pack()

        year_entry = tk.Entry(date_pop_up)
        year_entry.pack()

        year_entry_button = ttk.Button(
            date_pop_up, text="Submit", command=lambda: validate_and_set_year(year_entry.get()))
        year_entry_button.pack()

    def select_sort_type(self):
        """
        Sets the sort type, either date or file type, using pop-up windows.
        Also calls the date year selection if date type is chosen.

        Requires main.py to have a ui using tkinter.
        """
        Sorter.wait_for_me = True

        def set_to_date_and_destroy(self):
            Sorter.sort_type = "date"
            Sorter.date_year_selection(self)
            sort_type_pop_up.destroy()

        def set_to_type_and_destroy(self):
            Sorter.sort_type = "file type"
            sort_type_pop_up.destroy()
            Sorter.wait_for_me = False

        sort_type_pop_up = tk.Toplevel()
        sort_type_pop_up.wm_title("Sort Type")

        # pop_up_buttons
        date_sort = ttk.Button(sort_type_pop_up, text="Sort by date",
                               command=lambda: set_to_date_and_destroy(self))
        date_sort.grid(row=0, column=0)
        file_type_sort = ttk.Button(
            sort_type_pop_up, text="Sort by file type", command=lambda: set_to_type_and_destroy(self))
        file_type_sort.grid(row=0, column=1)

    def check_folders(self, folders):
        """ensures folders exist in sorted_folder directory, creates them if not found"""

        for folder in folders:
            path = "".join([Sorter.sorted_folder, str(folder)])
            if not os.path.exists(path):
                os.mkdir(path)

    def make_date_folders(self):
        """Checks that folders for years and folders for months in each year exist and sets Sorter.folders to years between earliest and current year"""

        years = list(range(int(Sorter.earliest), int(Sorter.year) + 1))
        # make years into strings to be used in file paths
        Sorter.folders = [str(year) for year in years]
        # makes year folders
        Sorter.check_folders(self, years)
        for y in years:
            # makes month folders
            for month in Sorter.MONTHS:
                y_path = "".join([Sorter.sorted_folder, str(y), "/", month])
                if not os.path.exists(y_path):
                    os.mkdir(y_path)

    def make_file_folders(self):
        """Sets folders to file types and makes the folders"""

        Sorter.folders = ["Set-up or Program Files",
                          "Compressed Archives", "Images", "Text Files", "Other"]
        Sorter.check_folders(self, Sorter.folders)

    def sort_to_folder_by_date(self):
        """Sorts files into respective year/month folders by looking at the last modification date of each file, if sort type == date"""

        for filename in os.listdir(Sorter.sorted_folder):
            if filename not in Sorter.folders:
                old_path = "".join([Sorter.sorted_folder, filename])
                # finding date of last modification for each file
                mod_time = os.path.getmtime(old_path)
                local_time = time.ctime(mod_time)
                lst = local_time.split()
                month = str(lst[1])
                months = {"Jan": "(1)", "Feb": "(2)", "Mar": "(3)", "Apr": "(4)", "May": "(5)", "Jun": "(6)",
                          "Jul": "(7)", "Aug": "(8)", "Sep": ("9"), "Oct": "(10)", "Nov": "(11)", "Dec": "(12)"}
                new_path = f"{Sorter.sorted_folder}{str(lst[4])}/{months[month]} {month}/{filename}"
                # try block so program doesn't stop if file already exists in directory. Exising file is replaced by file being moved
                try:
                    os.rename(old_path, new_path)
                except FileExistsError:
                    os.remove(new_path)
                    os.rename(old_path, new_path)

    # insert elif statement above else statement if adding a folder to the list folders

    def assign_folder_by_file_type(self, filename, folders):
        """returns folder name based on file name extension i.e. .exe"""

        if filename.lower().endswith((".exe", ".app", ".dmg")):
            return folders[0]
        elif filename.lower().endswith((".zip", ".7z", ".rar")):
            return folders[1]
        elif filename.lower().endswith((".ico", ".jpg", ".jpeg", ".png", ".pdf")):
            return folders[2]
        elif filename.lower().endswith((".doc", ".docx", ".docm", ".rtx", ".txt", ".ini")):
            return folders[3]
        else:
            return folders[-1]

    def sort_to_folder_by_file_type(self):
        """Sort function if sort type == file type"""

        for filename in os.listdir(Sorter.sorted_folder):
            if filename not in Sorter.folders:
                old_path = "".join([Sorter.sorted_folder, filename])
                new_path = "".join([Sorter.sorted_folder, Sorter.assign_folder_by_file_type(
                    self, filename, Sorter.folders), "/", filename])
                try:
                    os.rename(old_path, new_path)
                except FileExistsError:
                    os.remove(new_path)
                    os.rename(old_path, new_path)

    def sort_files(self, sort_type=None):
        """Final function for sorting files, run this to sort."""

        if sort_type is None:
            sort_type = self.sort_type

        if sort_type == "file type":
            Sorter.make_file_folders(self)
            Sorter.sort_to_folder_by_file_type(self)

        elif sort_type == "date":
            Sorter.make_date_folders(self)
            Sorter.sort_to_folder_by_date(self)


# Remover ---------------------------------------------------------------------------------------------------------------------------------------------------
class Remover(object):
    """Functions for undoing actions from Sorter Class"""

    # same as from Sorter class
    MONTHS = ["(1) Jan", "(2) Feb", "(3) Mar", "(4) Apr", "(5) May", "(6) Jun",
              "(7) Jul", "(8) Aug", "(9) Sep", "(10) Oct", "(11) Nov", "(12) Dec"]

    # METHODS
    def empty_date_folders(self, sorted_folder=Sorter.sorted_folder, folders=Sorter.folders):
        """Moves files out of generated date folders so that a different sort type can be chosen"""

        for folder in folders:
            for month in Remover.MONTHS:
                folder_path = "".join([sorted_folder, folder, "/", month])
                for filename in os.listdir(folder_path):
                    old_path = "".join([folder_path, "/", filename])
                    new_path = "".join([sorted_folder, filename])
                # try block so program doesn't stop if file already exists in directory. Exising file is replaced by file being moved
                    try:
                        os.rename(old_path, new_path)
                    except FileExistsError:
                        os.remove(new_path)
                        os.rename(old_path, new_path)

    def empty_file_type_folders(self, sorted_folder=Sorter.sorted_folder, folders=Sorter.folders):
        """Moves files out of generated file type folders so that a different sort type can be chosen"""

        for folder in folders:
            folder_path = "".join([sorted_folder, folder])
            for filename in os.listdir(folder_path):
                old_path = "".join([sorted_folder, folder, "/", filename])
                new_path = "".join([sorted_folder, filename])
                # try block so program doesn't stop if file already exists in directory. Exising file is replaced by file being moved
                try:
                    os.rename(old_path, new_path)
                except FileExistsError:
                    os.remove(new_path)
                    os.rename(old_path, new_path)

    def delete_date_folders(self, sorted_folder=Sorter.sorted_folder, folders=Sorter.folders):
        """Deletes folders made by Sorter if sort type == date. Folders must be empty."""

        # try blocks so program doesnt stop if certain folders have been manually deleted
        for folder in folders:

            for month in Remover.MONTHS:
                path = "".join([sorted_folder, folder, "/", month])
                try:
                    os.rmdir(path)
                except:
                    print(
                        f"Please check {path} exists. Make sure to select options so that same folders as the ones that exist would be created i.e. same sort type and same earliest year if date is chosen.")

            path = "".join([sorted_folder, folder])
            try:
                os.rmdir(path)
            except:
                print(f"Please check {path} exists. Make sure to select options so that same folders as the ones that exist would be created i.e. same sort type and same earliest year if date is chosen.")

    def delete_file_type_folders(self, sorted_folder=Sorter.sorted_folder, folders=Sorter.folders):
        """Deletes folders made by Sorter if sort type == file type. Folders must be empty."""

        # try block so program doesnt stop if certain folders have been manually deleted
        for folder in folders:
            path = "".join([sorted_folder, folder])
            try:
                os.rmdir(path)
            except:
                print(f"Please check {path} exists. Make sure to select options so that same folders as the ones that exist would be created i.e. same sort type and same earliest year if date is chosen.")

    def undo_folders(self, sorted_folder=Sorter.sorted_folder, sort_type=Sorter.sort_type, folders=Sorter.folders):
        """Executes functions to empty and delete folders created by Sorter class functions"""

        if sort_type == "file type":
            Remover.empty_file_type_folders(self, sorted_folder, folders)
            Remover.delete_file_type_folders(self, sorted_folder, folders)
        elif sort_type == "date":
            Remover.empty_date_folders(self, sorted_folder, folders)
            Remover.delete_date_folders(self, sorted_folder, folders)
