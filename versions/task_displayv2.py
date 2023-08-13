"""
On this version, assigned the add_screen formatting to none to avoid
the Pylint formatting error. 
"""

"""Imports:
1. Tkinter module for creating the GUI
2. For working with dates and times
3. SQLite database
4. Provides access to some variables used
5. For running external processes
6. Widget for displaying a date selection calendar
"""

# Imports
from tkinter import *
from datetime import datetime
import sqlite3
import sys
import subprocess
from tkcalendar import Calendar


# Function to update the time and date labels
def update_datetime():
    """
    Update the time and date labels with the current time and date.
    """
    current_time = datetime.now().strftime("%H:%M:%S")
    current_date = datetime.now().strftime("%A, %B %d")

    time_label.config(text=current_time)
    date_label.config(text=current_date)

    # Schedule the next update after 1 second (1000 milliseconds)
    root.after(1000, update_datetime)


# Function to remove tasks
def remove_task(subject, homework, due_date):
    """
    This function is called when the user clicks the "Remove" button.
    It takes the subject, homework name, and due date of the task as input arguments.
    The function then retrieves the username passed from homr page
    and deletes the corresponding task entry from the user's database and display list.
    """
    # Get the username passed from home page
    username1 = sys.argv[1] if len(sys.argv) > 1 else ""

    # Open a connection to the database
    conn = sqlite3.connect("db/homework_data.db")
    cursor = conn.cursor()

    # Create a table name based on the username
    table_name = f"{username1}_table"

    # Delete the task from the table
    cursor.execute(
        f"DELETE FROM {table_name} WHERE subject=? AND homework_name=? AND due_date=?",
        (subject, homework, due_date),
    )

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    # Refresh the displayed tasks
    display_tasks()


# Function to add tasks
def add():
    """
    Opens a window to add tasks to the application.
    It creates entry fields for the subject, homework name, and due date.
    The function also provides a button to open a calendar window for selecting a due date.
    """

    def select_date():
        """
        This function creates a new top-level window with a calendar widget allowing the
        user to select a due date for a task.
        """

        def set_date():
            """
            Function retrieves the date selected by the user from the calendar widget.
            """
            selected_date = cal.selection_get()

            # Check if the selected date is before the current date
            if selected_date < datetime.now().date():
                # Display an error message for selecting past dates
                reminder_label = Label(
                    top, text="Please don't select past dates!", fg="red"
                )
                reminder_label.grid(row=3, columnspan=2, pady=5)

                # Schedule the reminder label to disappear after 2000 milliseconds (2 seconds)
                top.after(2000, reminder_label.destroy)
            else:
                due_date.set(selected_date)
                due_button.config(text=selected_date.strftime("%Y-%m-%d"))
                top.destroy()

        top = Toplevel(root)

        cal = Calendar(top, selectmode="day")
        cal.grid()

        confirm_button = Button(top, text="Select", command=set_date)
        confirm_button.grid()

        top.grab_set()  # Set the focus to the new window
        top.wait_window()  # Wait for the window to be closed

    def save():
        """
        Retrieves the subject, homework name, and due date entered by the user.
        The function then inserts the homework data into the user's table.
        After saving the task, it clears the entry fields and the due date button text.
        """
        subject = chosen_subject.get()
        homework = homework_name.get()
        due = due_date.get()

        # Check if any of the fields are empty
        if not subject or not homework or not due:
            # Display a message reminding the user to provide all inputs
            reminder_label = Label(
                add_frame, text="Please provide all inputs!", fg="red"
            )
            reminder_label.grid(row=3, columnspan=2, pady=5)

            # Schedule the reminder label to disappear after 2000 milliseconds (2 seconds)
            add_screen.after(2000, reminder_label.destroy)
            return

        # Get the username passed from home page
        username1 = sys.argv[1] if len(sys.argv) > 1 else ""

        # Open a connection to the database
        conn = sqlite3.connect("db/homework_data.db")
        cursor = conn.cursor()

        # Create a table for the user if it doessn't exist
        table_name = f"{username1}_table"  # Create a table based on the username
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
            id INTERGER PRIMARY KEY, 
            subject TEXT,
            homework_name TEXT, 
            due_date TEXT
            )
            """
        )

        # Insert the homework data into table
        cursor.execute(
            f"""
            INSERT INTO {table_name} (subject, homework_name, due_date)
            VALUES (?, ?, ?)
            """,
            (subject, homework, due),
        )

        # Commit the changes and close thee connection
        conn.commit()
        conn.close()

        # Clear the entry fields
        homework_name.set("")
        due_date.set("")

        # Clear the date text on the button
        due_button.config(text="Select date")

    add_screen = Toplevel(root)
    add_screen.title("Add tasks")
    add_screen.configure(bg="#9fa0ff")  # Set the background color

    # Configure rows and columns to be expandable
    add_screen.rowconfigure(0, weight=1)
    add_screen.columnconfigure(0, weight=1)

    # Frame to group items
    add_frame = LabelFrame(add_screen)
    add_frame.grid(padx=10, pady=10)

    # Create label for subject
    subject_label = Label(add_frame, text="Subjects: ")
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
    subject_box = OptionMenu(add_frame, chosen_subject, *subject_names)
    subject_box.grid(row=0, column=1)

    # Create label for homework
    work_label = Label(add_frame, text="Homework Name: ")
    work_label.grid(row=1, column=0, padx=20, pady=20)

    # Create a variable to store the homework name
    homework_name = StringVar()
    homework_name.set("")

    # Create an entry to type in the homework name
    work_entry = Entry(add_frame, textvariable=homework_name)
    work_entry.grid(row=1, column=1, padx=30)

    # Create label for due date
    due_label = Label(add_frame, text="Due date: ")
    due_label.grid(row=2, column=0, padx=20, pady=20)

    # Create a variable to store the selected due date
    due_date = StringVar()
    due_date.set("")

    # Create a button to open the calendar and select a due date
    due_button = Button(add_frame, text="Select date", command=select_date)
    due_button.grid(row=2, column=1, padx=10, pady=3)

    save_button = Button(add_frame, text="Save", command=save)
    save_button.grid()


# Showing tasks from database
def display_tasks():
    """
    Function retrieves the username passed from home page.
    It then connects to the database and checks if a table with the username as its name exists.
    If the table exists, it fetches all the tasks associated with that username from the database.
    """
    # Get the username passed from home page
    username1 = sys.argv[1] if len(sys.argv) > 1 else ""

    # Open a connection to the database
    conn = sqlite3.connect("db/homework_data.db")
    cursor = conn.cursor()

    # Create a table name based on the username
    table_name = f"{username1}_table"

    # Check if the table exists
    cursor.execute(
        f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
    )
    table_exists = cursor.fetchone()

    if table_exists:
        # Fetch all the tasks from the table
        cursor.execute(f"SELECT subject, homework_name, due_date FROM {table_name}")
        tasks = cursor.fetchall()

        # Clear the previous tasks displayed in the info_frame
        for widget in info_frame.winfo_children():
            widget.destroy()

        # Title label
        title_label = Label(info_frame, text="Your tasks:", font=("Arial", 20, "bold"))
        title_label.grid(row=0, columnspan=3, padx=10, pady=10, sticky="NSEW")

        # Create an add button
        add_button = Button(info_frame, text="Add", command=add)
        add_button.grid(row=1, padx=5, sticky="W")

        # Display the tasks in the info_frame
        for row, task in enumerate(tasks, start=2):
            subject, homework, due_date = task
            subject_label = Label(info_frame, text=f"Subject: {subject}")
            subject_label.grid(row=row, column=0, sticky="W", padx=3, pady=3)
            homework_label = Label(info_frame, text=f"Homework Name: {homework}")
            homework_label.grid(row=row, column=1, sticky="W", padx=3, pady=3)
            due_date_label = Label(info_frame, text=f"Due Date: {due_date}")
            due_date_label.grid(row=row, column=2, sticky="W", padx=3, pady=3)

            # Create a remove button for each task
            remove_button = Button(
                info_frame,
                text="Remove",
                command=lambda subject=subject, homework=homework, due_date=due_date: remove_task(
                    subject, homework, due_date
                ),
            )
            remove_button.grid(row=row, column=3, padx=3, pady=3)

    else:
        # If the table does not exist, display a message
        no_tasks_label = Label(info_frame, text="No tasks found.")
        no_tasks_label.grid(row=1, column=0, columnspan=3)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    # Schedule the next refresh
    root.after(
        3000, display_tasks
    )  # Refresh every 3 seconds (adjust the interval as needed)


# After button pressed, go back to login page
def back():
    """
    Closes the current root window and return the user to the login page.
    """
    # Destroy root window
    root.destroy()
    # Subprocess to lsunch new process running hoome page
    subprocess.Popen([sys.executable, "home.py"])


# GUI Code
root = Tk()
root.title("Homework Tracker App")
root.configure(bg="#4E67EB")  # Set the background color

# Configure rows and columns to be expandable
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

# Frame for grouping widgets
title_frame = LabelFrame(root)
title_frame.grid(row=0, sticky="EW")

# Frame for grouping widgets
info_frame = LabelFrame(root)
info_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=30, sticky="NSEW")

# Configure column and row resizing
info_frame.columnconfigure(1, weight=1)
title_frame.columnconfigure(1, weight=1)

# Get the name argument passed from home page
NAME_VALUE = sys.argv[2] if len(sys.argv) > 2 else ""

# Create and set the welcome message text variable
welcome_label = Label(title_frame, text=f"Welcome, {NAME_VALUE}", font=("Arial", 20))
welcome_label.grid(row=0, column=0, rowspan=2, padx=10, sticky="W")

# Button to go back to login page
back_button = Button(title_frame, text="Back to login page", command=back)
back_button.grid(row=2, column=0, padx=5, pady=10, sticky="W")

# Get the current time and date
time_now = datetime.now().strftime("%H:%M:%S")
date_now = datetime.now().strftime("%A, %B %d")

# Create label to display the current time
time_label = Label(title_frame, text="", font=("Arial", 20))
time_label.grid(row=0, column=1, padx=8, pady=5, sticky="E")

# Create label to display the current date
date_label = Label(title_frame, text="", font=("Arial", 16))
date_label.grid(row=1, column=1, padx=8, pady=5, sticky="E")

# Schedule the initial update of the date and time labels
update_datetime()

# Display the tasks when the program starts
display_tasks()

# Run the mainloop
root.mainloop()
