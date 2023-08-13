# Imports
from tkinter import *
from tkcalendar import Calendar

# Function to open the calendar and select a date
def select_date():
    """
    Opens a calendar window and allows the user to select a due date.

    This function creates a new window using 
    `Toplevel()` to display the calendar.
    The user can select a date by clicking on a day in the calendar.

    When the user confirms the selection by clicking the "Select" button, 
    the selected date is retrieved using the `cal.selection_get()` method. 
    The `due_date` variable is updated with the selected date 
    using the `due_date.set()` method.

    The text on the `due_button` is updated with the selected date 
    formatted as "%Y-%m-%d" using the `due_button.config()` method.

    Finally, the window is destroyed using `top.destroy()`.
    """
    def set_date():
        """
        Sets selected date as due date and updates the button text.
        This function retrieves the selected date from the calendar 
        using the `cal.selection_get()` method.
        The `due_date` variable is updated with the selected date 
        using the `due_date.set()` method.

        The text on the `due_button` is updated with the selected date 
        formatted as "%Y-%m-%d" using the `due_button.config()` method.

        Finally, the window is destroyed using `top.destroy()`.

        """
        selected_date = cal.selection_get()
        due_date.set(selected_date)
        due_button.config(text=selected_date.strftime("%Y-%m-%d"))
        top.destroy()
        
    top = Toplevel(root)
    cal = Calendar(top, selectmode="day")
    cal.pack()
    confirm_button = Button(top, text="Select", command=set_date)
    confirm_button.pack()
    top.grab_set()  # Set the focus to the new window
    top.wait_window()  # Wait for the window to be closed


# GUI Code
root = Tk()
root.title("add task")
root.configure(bg="#4E67EB")  # Set the background color

# Create label for  subject
subject_label = Label(root, text="Subjects: ")
subject_label.grid(row=0, column=0, padx=20, pady=20)

# Set up a variable and list for the subject OptionMenu
subject_names = [
    "Art",
    "Computer Science",
    "Business Studies",
    "Economics",
    "English",
    "Chinese",
    "Mathematics",
    "Music",
    "Biology",
    "Chemistry",
    "Physics",
    "Social Studies",
]
chosen_subject = StringVar()
chosen_subject.set(subject_names[0])

# Create an OptionMenu to select the subject
subject_box = OptionMenu(root, chosen_subject, *subject_names)
subject_box.grid(row=0, column=1)

# Create label for homework
work_label = Label(root, text="Homework Name: ")
work_label.grid(row=1, column=0, padx=20, pady=20)

# Create a variable to store the mail
work = StringVar()
work.set("")

# Create an entry to type in work name
work_entry = Entry(root, textvariable=work)
work_entry.grid(row=1, column=1, padx=30)

# Create label for due date
due_label = Label(root, text="Due date: ")
due_label.grid(row=2, column=0, padx=20, pady=20)

# Create a variable to store the selected due date
due_date = StringVar()
due_date.set("")

# Create a button to open the calendar and select a due date
due_button = Button(root, text="Select date", command=select_date)
due_button.grid(row=2, column=1, padx=10, pady=3)


# Run the mainloop
root.mainloop()