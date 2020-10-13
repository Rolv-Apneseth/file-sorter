import os
import time
import tkinter as tk
from datetime import datetime
from tkinter import ttk, filedialog

############################################################
###SORTER###################################################
############################################################
class Sorter(object):
    """Contains functions for making sort folders and sorting files into those folders. Class variables are used by these functions."""
    def __init__(self):
        # DEFAULTS AND CONSTANTS
        self.sort_type = "file type"
        # folder to be sorted
        self.sorted_folder = "./"
        # folders files will be sorted into
        self.folders = ["Set-up or Program Files", "Compressed Archives", "Images", "Text Files", "Other"]
        # Current date
        self.today = datetime.today()
        # current year
        self.year = today.year
        # folder names in each year folder
        self.MONTHS = ["(1) Jan", "(2) Feb", "(3) Mar", "(4) Apr", "(5) May", "(6) Jun", "(7) Jul", "(8) Aug", "(9) Sep", "(10) Oct", "(11) Nov", "(12) Dec"]

    #METHODS
    def select_folder(self):
        """Pop up to ask user to select a directory to be sorted"""

        self.sorted_folder = filedialog.askdirectory() + "/"


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
                    raise Exception
                self.year = year
                date_pop_up.destroy()
                self.wait_for_me = False


            except:
                bad_entry = tk.Toplevel()
                bad_entry.wm_title("Error in year selection")
                bad_entry_label = tk.Label(bad_entry, text="Please enter a valid year.\nMust be less than or equal to current year.")
                bad_entry_label.pack()
                bad_entry_button = ttk.Button(bad_entry, text="Ok", command=bad_entry.destroy)
                bad_entry_button.pack()


        date_pop_up = tk.Toplevel()
        date_pop_up.wm_title("Year Selection")

        year_entry_label = tk.Label(date_pop_up, font=("Helvetica", 10), text="Please enter the earliest year you want\nto create sorted folders for.\nFolders will be created from that year to the current year.\nPlease note that low numbers will create an\nexcessive amount of folders.")
        year_entry_label.pack()

        year_entry = tk.Entry(date_pop_up)
        year_entry.pack()

        year_entry_button = ttk.Button(date_pop_up, text="Submit", command=lambda: validate_and_set_year(year_entry.get()))
        year_entry_button.pack()


    def select_sort_type(self):
        """
        Sets the sort type, either date or file type, using pop-up windows.
        Also calls the date year selection if date type is chosen.

        Requires main.py to have a ui using tkinter.
        """
        self.wait_for_me = True

        def set_to_date_and_destroy(self):
            self.sort_type = "date"
            self.date_year_selection()
            self.sort_type_pop_up.destroy()


        def set_to_type_and_destroy(self):
            self.sort_type = "file type"
            self.sort_type_pop_up.destroy()
            self.wait_for_me = False


        self.sort_type_pop_up = tk.Toplevel()
        self.sort_type_pop_up.wm_title("Sort Type")
        #pop_up_buttons
        date_sort = ttk.Button(self.sort_type_pop_up, text="Sort by date", command= lambda: set_to_date_and_destroy(self))
        date_sort.grid(row=0, column=0)
        file_type_sort = ttk.Button(self.sort_type_pop_up, text="Sort by file type", command= lambda: set_to_type_and_destroy(self))
        file_type_sort.grid(row=0, column=1)


    def check_folders(self, folders):
        """Ensures folders exist in sorted_folder directory, creates them if not found"""

        for folder in folders:
            path = "".join([self.sorted_folder, str(folder)])
            if not os.path.exists(path):
                 os.mkdir(path)


    def make_date_folders(self):
        """Checks that folders for years and folders for months in each year exist and sets self.folders to years between earliest and current year"""

        years = list(range(int(self.year), int(self.year) + 1))
        # make years into strings to be used in file paths
        self.folders = [str(year) for year in years]
        # makes year folders
        self.check_folders(years)
        for y in years:
            # makes month folders
            for month in self.MONTHS:
                y_path = "".join([self.sorted_folder, str(y), "/", month])
                if not os.path.exists(y_path):
                     os.mkdir(y_path)


    def make_file_folders(self):
        """Sets folders to file types and makes the folders"""

        self.folders = ["Set-up or Program Files", "Compressed Archives", "Images", "Text Files", "Other"]
        self.check_folders(self.folders)


    def sort_to_folder_by_date(self):
        """Sorts files into respective year/month folders by looking at the last modification date of each file, if sort type == date"""

        for filename in os.listdir(self.sorted_folder):
            if not filename in self.folders:
                old_path = "".join([self.sorted_folder, filename])
                # finding date of last modification for each file
                mod_time = os.path.getmtime(old_path)
                local_time = time.ctime(mod_time)
                lst = local_time.split()
                month = str(lst[1])
                months = {"Jan": "(1)", "Feb": "(2)", "Mar": "(3)", "Apr": "(4)", "May": "(5)", "Jun": "(6)", "Jul": "(7)", "Aug": "(8)", "Sep": ("9"), "Oct": "(10)", "Nov": "(11)", "Dec": "(12)"}
                new_path = f"{self.sorted_folder}{str(lst[4])}/{months[month]} {month}/{filename}"
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

        for filename in os.listdir(self.sorted_folder):
            if not filename in self.folders:
                old_path = "".join([self.sorted_folder, filename])
                new_path = "".join([self.sorted_folder, self.assign_folder_by_file_type(filename, self.folders), "/", filename])
                try:
                    os.rename(old_path, new_path)
                except FileExistsError:
                    os.remove(new_path)
                    os.rename(old_path, new_path)


    def sort_files(self, sort_type=None):
        """Final function for sorting files, run this to sort."""

        if sort_type == None:
            sort_type = self.sort_type

        if sort_type == "file type":
            self.make_file_folders()
            self.sort_to_folder_by_file_type()

        elif sort_type == "date":
            self.make_date_folders()
            self.sort_to_folder_by_date()



#############################################################
###Remover###################################################
#############################################################
class Remover(object):
    """Contains functions for undoing actions from Sorter class"""

    def __init__(self):
        # same as from Sorter class
        self.MONTHS = ["(1) Jan", "(2) Feb", "(3) Mar", "(4) Apr", "(5) May", "(6) Jun", "(7) Jul", "(8) Aug", "(9) Sep", "(10) Oct", "(11) Nov", "(12) Dec"]

    def empty_date_folders(self, sorted_folder, folders):
        """Moves files out of generated date folders so that a different sort type can be chosen"""

        for folder in folders:
            for month in self.MONTHS:
                folder_path = "".join([sorted_folder, folder, "/", month])
                for filename in os.listdir(folder_path):
                    old_path = "".join([folder_path , "/", filename])
                    new_path = "".join([sorted_folder, filename])
                # try block so program doesn't stop if file already exists in directory. Exising file is replaced by file being moved
                    try:
                        os.rename(old_path, new_path)
                    except FileExistsError:
                        os.remove(new_path)
                        os.rename(old_path, new_path)


    def empty_file_type_folders(self, sorted_folder, folders):
        """Moves files out of generated file type folders so that a different sort type can be chosen"""

        for folder in folders:
            folder_path = "".join([sorted_folder, folder])
            for filename in os.listdir(folder_path):
                old_path = "".join([sorted_folder, folder, "/", filename])
                new_path = "".join([sorted_folder, filename])
                #try block so program doesn't stop if file already exists in directory. Exising file is replaced by file being moved
                try:
                    os.rename(old_path, new_path)
                except FileExistsError:
                    os.remove(new_path)
                    os.rename(old_path, new_path)


    def delete_date_folders(self, sorted_folder, folders):
        """Deletes folders made by Sorter if sort type == date. Folders must be empty."""

        # try blocks so program doesnt stop if certain folders have been manually deleted
        for folder in folders:
            for month in self.MONTHS:
                path = "".join([sorted_folder, folder, "/", month])
                try:
                    os.rmdir(path)
                except:
                    print(f"Please check {path} exists. Make sure to select options so that same folders as the ones that exist would be created i.e. same sort type and same earliest year if date is chosen.")

            path = "".join([sorted_folder, folder])
            try:
                os.rmdir(path)
            except:
                print(f"Please check {path} exists. Make sure to select options so that same folders as the ones that exist would be created i.e. same sort type and same earliest year if date is chosen.")


    def delete_file_type_folders(self, sorted_folder, folders):
        """Deletes folders made by Sorter if sort type == file type. Folders must be empty."""

        # try block so program doesnt stop if certain folders have been manually deleted
        for folder in folders:
            path = "".join([sorted_folder, folder])
            try:
                os.rmdir(path)
            except:
                print(f"Please check {path} exists. Make sure to select options so that same folders as the ones that exist would be created i.e. same sort type and same earliest year if date is chosen.")


    def undo_folders(self, sorted_folder, sort_type, folders):
        """Executes functions to empty and delete folders created by Sorter class functions"""

        if sort_type == "file type":
            self.empty_file_type_folders(sorted_folder, folders)
            self.delete_file_type_folders(sorted_folder, folders)
        elif sort_type == "date":
            self.empty_date_folders(sorted_folder, folders)
            self.delete_date_folders(sorted_folder, folders)
