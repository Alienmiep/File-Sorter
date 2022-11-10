import os
import sys
import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd


def get_application_path() -> str:
    # determine if application is a script file or frozen exe
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)
    return application_path

def open_dialog():
    filetypes = (('Excel Files', '.xls;.xlsx'), ('CSV Files', '.csv'), ('All Files', '.*'))
    filename_path = fd.askopenfilename(title ='Open', initialdir=application_path, filetypes=filetypes)
    global filename
    filename = get_filename_from_path(filename_path)
    label_filename.configure(text=filename)
    button_start.state(['!disabled'])

def get_filename_from_path(filename_path) -> str:
    list = filename_path.split("/")
    return list[-1]

def start_scan():
    # create output directory
    directory = filename[:filename.rfind(".")]
    directory_path = os.path.join(application_path, directory)

    # TODO: check if the folder exists already! (if yes, retry with (1) appended or display error message)
    # os.mkdir(directory_path)
    print("Directory '% s' created" % directory)
    
    # open file
    # get number of entries
    # create empty text file
    # find and link files (new function)
    # close file
    # output textfile if not empty


application_path = get_application_path()

window = tk.Tk()
window.resizable(width=False, height=False)
style = ttk.Style()
style.configure('A.TFrame', padding=5, borderwidth=5, relief="ridge")
content = ttk.Frame(window, padding=5)
frame_top = ttk.Frame(content, style='A.TFrame')
frame_bottom = ttk.Frame(content, style='A.TFrame')

# Top frame layout
label_filename = ttk.Label(frame_top, text="No file chosen")
button_filename = ttk.Button(frame_top, text="Choose File", width=15, command=open_dialog)
margin_filename = ttk.Frame(frame_top, borderwidth=0)
# TODO: either specify the column names or numbers for ID and amount (if needed)

# Bottom frame layout
button_start = ttk.Button(frame_bottom, text="Start", command=start_scan)
button_start.state(['disabled'])
progressbar = ttk.Progressbar(frame_bottom, orient=HORIZONTAL, length=200, mode='determinate')
logbox = tk.Listbox(frame_bottom, width=44)
logbox_scrollbar = ttk.Scrollbar(frame_bottom, orient=VERTICAL, command=logbox.yview)
logbox.configure(yscrollcommand=logbox_scrollbar.set)

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
frame_top.columnconfigure(1, minsize=5)
frame_top.columnconfigure(2, minsize=200)

frame_bottom.rowconfigure(0, minsize=20)
frame_bottom.rowconfigure(1, minsize=30)
frame_bottom.rowconfigure(2, minsize=180)
frame_bottom.rowconfigure(3, minsize=20)
frame_bottom.columnconfigure(0, minsize=20)
frame_bottom.columnconfigure(1, minsize=100)
frame_bottom.columnconfigure(2, minsize=243)
frame_bottom.columnconfigure(4, minsize=20)

for i in range(1,101):
    logbox.insert('end', 'Line %d of 100' % i)

window.mainloop()



# src = os.path.join(application_path, "gauntletnew.png")
# dst = os.path.join(path, "gauntletnew-1.png")
# os.link(src,dst)


