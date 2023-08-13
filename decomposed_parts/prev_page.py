# Imports
from tkinter import *
import sqlite3
import sys
import subprocess


# After button pressed, go back to login page
def prevPage():
    """
    This function is called when a button is pressed to navigate back to the login page. 
    It destroys the current root window and then launches a new process running
    the home page script using the `subprocess.Popen()` function.
    """
    # Destroy root window
    root.destroy()
    # Subprocess to lsunch new process running home page
    subprocess.Popen(["python", "home.py"])


# GUI Code
root = Tk()
root.title("Homework Tracker App")
root.configure(bg="#4E67EB")  # Set the background color

# Configure rows and columns to be expandable
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

# Frame for grouping widgets
title_frame = LabelFrame(root)
title_frame.grid(row = 0, sticky = "EW")

# Button to go back to login page
back_button = Button(title_frame, text="Back to login page", command=prevPage)
back_button.grid(row = 0, column = 0, padx = 5, pady=10, sticky = "W")

# Run the mainloop
root.mainloop()
