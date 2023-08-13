# Imports
from tkinter import *
from PIL import Image, ImageTk
from datetime import datetime

# Function to update the time and date labels
def update_datetime():
    """
    Updates the time and date labels in the tkinter application.

    This function retrieves the current time and date using the 
    `datetime.now()` method.
    The time is formatted as "%H:%M:%S" (e.g., "10:30:45"), 
    and the date is formatted as "%A, %B %d" (e.g., "Monday, January 01").

    The function then updates the corresponding tkinter labels 
    (`time_label` and `date_label`)
    with the current time and date using the `config()` method.

    After updating the labels, 
    the function schedules the next update after 1s (1000 milliseconds)
    by calling itself using the `root.after()` method. 
    This will ensure that the labels are continuously updated
    """
    current_time = datetime.now().strftime("%H:%M:%S")
    current_date = datetime.now().strftime("%A, %B %d")
    time_label.config(text=current_time)
    date_label.config(text=current_date)
    # Schedule the next update after 1 second (1000 milliseconds)
    root.after(1000, update_datetime)

# GUI Code
root = Tk()
root.title("time")
root.configure(bg="#4E67EB")  # Set the background color

# Get the current time and date
current_time = datetime.now().strftime("%H:%M:%S")
current_date = datetime.now().strftime("%A, %B %d")

# Create label to display the current time
time_label = Label(root, text="", font=("Arial", 20))
time_label.grid(row=0, column=1, padx=8, pady=5, sticky="E")

# Create label to display the current date
date_label = Label(root, text="", font=("Arial", 16))
date_label.grid(row=1, column=1, padx=8, pady=3, sticky="E")

# Schedule the initial update of the date and time labels
update_datetime()

# Run the mainloop
root.mainloop()