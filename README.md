# File Sorter

### A small utility program to sort files into subfolders, based on a given spreadsheet.
Given a spreadsheet containing filenames and a directory containing hundreds of files, this program is supposed to do the following:

* Make a new directory with the name of the spreadsheet
* Parse the filename column of the spreadsheet and find the corresponding files
* Copy the files into the new directory
* Rename the file copies
* Output a list of all filenames that could not be found

The end result is a single executable file that 

* Supports .xslx, .xls and .csv spreadsheets
* Is operated via a GUI and gives the user feedback
* Runs on a Windows PC without Python installed

FileSorterTest contains files and a spreadsheet for testing, more test cases will be added soon.