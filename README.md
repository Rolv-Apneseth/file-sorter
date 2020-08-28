# file-sorter
 Program with a gui which allows you to sort a chosen folder by file type or by date into automatically generated folders, and then also undo the folders if necessary.

GUI built with tkinter.

The interface allows you to choose a folder to sort and what to sort files by (file type or date). If date is chosen, a pop up will ask what the earliest year you want to sort by is.
Click sort files to execute the script

For date, a folder will be generated for each year and 12 folders in each for each month.
For file type, different folders will be generated for certain grouped types of files i.e.executables, image files etc.

To undo a previous sort, make sure you select the same folder and same sort options that were selected before, such as file type,
or if by date then the earliest year, and click on reset folder. All the files which have been sorted will be moved back to the root directory of the sort.
