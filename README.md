# file-sorter #
 Program with a gui which allows you to sort a chosen folder by file type or by date into automatically generated folders, and then also undo the folders if necessary.

## What I learned
*File i/o
*Building GUI's using tkinter
*Error handling
*Use of OOP
*Combined use of the datetime and os modules for

## Installation
1. Requires python 3 to run. python can be installed from [here](https://www.python.org/downloads/)
2. Clone the repository by opening your command line/terminal and run: git clone https://github.com/Rolv-Apneseth/file-sorter.git
3. Install the requirements for the program.
    *In your terminal, navigate to the cloned directory and run: pip install -r requirements.txt
4. To run the actual program, navigate further into the file-sorter folder and run: python3 main.py

## Usage
1. Select which folder you would like sorted (or unsorted if it is already sorted). To do this, click on Select a folder to open a filedialog menu.
2. Select a sort type by clicking on the sort type dropdown.
    * File Type sorts files into folders based on their file types i.e. all image files into one folder, executables into another etc.
    * Date will sort files into the folder structure of Year/Month which it was last changed in
    *If Date is selected, you will also be prompted to write the earliest year you want a folder for. Please note that this can therefore create an excessive amount of folders.
3. Click on sort files to execute the script

To undo the created folders and move the files back into the chosen sort folder, simply click on the Reset folder button (but make sure that the exact same options, such as sort type, are still selected).
