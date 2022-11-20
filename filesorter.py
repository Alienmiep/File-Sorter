import os
import sys
import glob
import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd


def get_application_path() -> str:
    """Determine and return path to the application directory."""
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)
    return application_path

def open_dialog():
    """Open a file dialog where the user chooses a spreadsheet file."""
    filetypes = (('Excel/CSV Files', '*.xls;*.xlsx;*.csv'), ('All Files', '.*'))
    application_path = get_application_path()
    global spreadsheet_path
    spreadsheet_path = fd.askopenfilename(title ='Open File', initialdir=application_path, filetypes=filetypes)
    if spreadsheet_path != '': 
        global spreadsheet_name
        spreadsheet_name = get_filename_from_path(spreadsheet_path)
        label_filename.configure(text=spreadsheet_name)
        button_start.state(['!disabled'])
        logbox.delete(0, logbox.size())
        window.update_idletasks()

def get_filename_from_path(filename_path) -> str:
    """Extract and return the filename at the end of a path."""
    list = filename_path.split('/')
    return list[-1]

def cleanup(spreadsheet_data) -> pd.DataFrame:
    """Remove blank lines, replace NaN with 0 and ensure all values are integers."""
    spreadsheet_data = spreadsheet_data.dropna(axis='rows', subset=['ID'])
    spreadsheet_data['bestellt'] = spreadsheet_data['bestellt'].fillna(0)
    spreadsheet_data['ID'] = spreadsheet_data['ID'].astype('int64')  # if the spreadsheet had blank lines, it will detect the columns as float64 instead of int64
    spreadsheet_data['bestellt'] = spreadsheet_data['bestellt'].astype('int64')
    return spreadsheet_data

def start_scan():
    """Read filenames from chosen spreadsheet and copy them into a subdirectory.
    
    This method is called by the Start button, which only becomes available once the user has chosen a spreadsheet to load.
    1. A directory named after the chosen spreadsheet is created, in the same directory that the spreadsheet resides in (which may be different from the application directory).
    2. The spreadsheet gets read into a DataFrame using pandas.
    3. Filenames listed in the spreadsheet are searched in the spreadsheet directory and, if found, copied into the subdirectory and renamed.
    """
    button_start.state(['disabled'])
    # create output directory
    directory_name = spreadsheet_name[:spreadsheet_name.rfind('.')]
    spreadsheet_directory = spreadsheet_path[: spreadsheet_path.rfind('/')]
    directory_path = os.path.join(spreadsheet_directory, directory_name)
    # TODO: handle case that directory exists already (just overwrite, append (1) or display error message)
    if not os.path.exists(directory_path): os.mkdir(directory_path)
    logbox.insert('end', 'Directory {0} created'.format(directory_name))
    
    # open file
    extension = spreadsheet_name[spreadsheet_name.rfind('.')+1 :]
    if extension == 'xlsx' or extension == 'xls':
        spreadsheet_data = pd.read_excel(spreadsheet_path, usecols='A, D')  # A -> "ID" and D -> "bestellt" is hardcoded for now    
    elif extension == 'csv':
        spreadsheet_data = pd.read_csv(spreadsheet_name, sep=';')
    spreadsheet_data = cleanup(spreadsheet_data)
    length = len(spreadsheet_data.index)
    progressbar.configure(maximum=length)

    # create empty text file
    textfile_path = directory_path + '/' + directory_name + '_not_found.txt'
    textfile = open(textfile_path, 'w')
    
    # find and link files 
    for i in range(0, length):
        current_file = str(spreadsheet_data['ID'].iloc[i])
        current_path = spreadsheet_directory + '/' + current_file + '.*'
        matches = glob.glob(current_path)
        if matches:
            for m in matches:
                new_name = str(spreadsheet_data['bestellt'].iloc[i]) + '_' + get_filename_from_path(m.replace(chr(92), '/'))
                index = new_name.rfind('.')
                new_name = new_name[:index] + '_' + directory_name + new_name[index:]
                dst = directory_path + '/' + new_name
                if not os.path.exists(dst): os.link(m, dst)
            logbox.insert('end', 'File {0} copied to {1}'.format(current_file, directory_name))
        else:
            textfile.write(current_file + '\n')
            logbox.insert('end', 'Could not find file {0}'.format(current_file))
        logbox.see(logbox.size())
        progressbar.step()
        window.update_idletasks()

    # close textfile
    textfile.close()
    if os.stat(textfile_path).st_size == 0:
        os.remove(textfile_path)
    logbox.insert('end', 'Sorting complete')
    logbox.see(logbox.size())
    button_start.state(['!disabled'])


window = tk.Tk()
window.title('File Sorter')
window.resizable(width=False, height=False)
style = ttk.Style()
style.configure('A.TFrame', padding=5, borderwidth=5, relief='ridge')
content = ttk.Frame(window, padding=5)
frame_top = ttk.Frame(content, style='A.TFrame')
frame_bottom = ttk.Frame(content, style='A.TFrame')

# Top frame layout
label_filename = ttk.Label(frame_top, text='No file chosen')
button_filename = ttk.Button(frame_top, text='Choose File', width=15, command=open_dialog)
margin_filename = ttk.Frame(frame_top, borderwidth=0)
# TODO: either specify the column names or numbers for ID and amount (if needed)

# Bottom frame layout
button_start = ttk.Button(frame_bottom, text='Start', command=start_scan)
button_start.state(['disabled'])
progressbar = ttk.Progressbar(frame_bottom, orient=HORIZONTAL, length=200, mode='determinate')
logbox = tk.Listbox(frame_bottom, width=44, activestyle='none')
logbox_scrollbar = ttk.Scrollbar(frame_bottom, orient=VERTICAL, command=logbox.yview)
logbox.configure(yscrollcommand=logbox_scrollbar.set)
logbox_scrollbar.configure(command=logbox.yview)

# Gridding
content.pack(fill=tk.Y)
frame_top.grid(row=0, column=0)
frame_bottom.grid(row=2, column=0)

label_filename.grid(column=0, row=0, sticky=(E))
margin_filename.grid(column=1, row=0)
button_filename.grid(column=2, row=0, sticky=(W))

button_start.grid(row=1, column=1, sticky=(N, W))
progressbar.grid(row=1, column=2, sticky=(N, W), pady=1)
logbox.grid(row=2, column=1, columnspan=2, sticky=(N, S, W, E))
logbox_scrollbar.grid(row=2, column=3, sticky=(N, S))

# Grid configurations
content.rowconfigure(1, minsize=5)
frame_top.rowconfigure(0, minsize=70)
frame_top.columnconfigure(0, minsize=195)
frame_top.columnconfigure(1, minsize=10)
frame_top.columnconfigure(2, minsize=195)

frame_bottom.rowconfigure(0, minsize=20)
frame_bottom.rowconfigure(1, minsize=30)
frame_bottom.rowconfigure(2, minsize=180)
frame_bottom.rowconfigure(3, minsize=20)
frame_bottom.columnconfigure(0, minsize=20)
frame_bottom.columnconfigure(1, minsize=100)
frame_bottom.columnconfigure(2, minsize=243)
frame_bottom.columnconfigure(4, minsize=20)

window.mainloop()