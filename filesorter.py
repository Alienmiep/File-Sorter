import os
import sys
import tkinter as tk
from tkinter import *
from tkinter import ttk

# Building the GUI
window = tk.Tk()
style = ttk.Style()
style.configure('A.TFrame', padding=5, borderwidth=5, relief="ridge")
content = ttk.Frame(window, padding=5)
frame_top = ttk.Frame(content, style='A.TFrame')
frame_bottom = ttk.Frame(content, style='A.TFrame')
frame_margin = ttk.Frame(content, borderwidth=0)

# Top frame layout
label_filename = ttk.Label(frame_top, text="No file chosen")
button_filename = ttk.Button(frame_top, text="Choose File", width=15)
margin_filename = ttk.Frame(frame_top, borderwidth=0)
# TODO: either specify the column names or numbers for ID and amount (if needed)

# Bottom frame layout


# Gridding
content.pack(fill=tk.Y)
frame_top.grid(row=0, column=0)
frame_margin.grid(row=1, column=0)
frame_bottom.grid(row=2, column=0)

label_filename.grid(column=0, row=0, sticky=(E))
margin_filename.grid(column=1, row=0)
button_filename.grid(column=2, row=0, sticky=(W))

# Grid configurations
content.rowconfigure(1, minsize=5)
frame_top.rowconfigure(0, minsize=70)
frame_top.columnconfigure(0, minsize=195)
frame_top.columnconfigure(1, minsize=5)
frame_top.columnconfigure(2, minsize=200)

frame_bottom.rowconfigure(0, minsize=200)
frame_bottom.columnconfigure(0, minsize=200)
frame_bottom.columnconfigure(1, minsize=200)

window.mainloop()

# First file management tests
# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)
print("Application path: "+ application_path)

directory = "Test"
path = os.path.join(application_path, directory)

# TODO: check if the folder exists already! (if yes, retry with (1) appended or display error message)
# os.mkdir(path)
print("Directory '% s' created" % directory)

# src = os.path.join(application_path, "gauntletnew.png")
# dst = os.path.join(path, "gauntletnew-1.png")
# os.link(src,dst)


