# Imports
from tkinter import *
from tkcalendar import Calendar
import sqlite3
import sys


# Function to remove tasks
def remove_task(subject, homework, due_date):
    """
    Function connects to the SQLite database named "homework_data.db" and delete the specified task
    from the user's designated table. 
    The username is obtained from the command-line argument passed from home page.
    The function first creates the table name based on the provided username 
    and then performs a delete operation on the database table to remove the task that matches the given subject, 
    homework name, and due date.

    After deleting the task, the function commits the changes to the database and closes the connection. 
    Finally, it calls the "display_tasks()" function to refresh and display the updated list.
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
    This function creates a new window (Toplevel) to allow user to input the details of a new task. 
    The user can select a subject, provide the homework name, and choose a due date using a calendar. 
    
    After filling in the details,
    the user can click the "Save" button to add the new task to the database.
    """
    def select_date():
        """
        Creates new window (Toplevel) with a calendar widget for the user to select a due date for new task. 
        When the user clicks the "Select" button in the calendar window, 
        the 'set_date' function is called to set the selected date as the due date for the new task.
        """
        def set_date():
            """
            Called when user clicks the "Select" button in the calendar window created by 'select_date' function. 
            The selected date is obtained from the calendar widget, 
            and it is set as the value of the 'due_date' variable. 
            
            The selected date is then displayed on the "Select date" button in the 'add' window.
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

    def save():
        """
        This function retrieves the subject, homework name, and due date from 
        the 'chosen_subject', 'homework_name', and 'due_date' variables, respectively. 
        It then connects to "homework_data.db" and creates a newtable for the user if it does not exist. 
        The table name is based on the provided username from home page.
        """
        subject = chosen_subject.get()
        homework = homework_name.get()
        due = due_date.get()

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

    global add_screen

    add_screen = Toplevel(root)
    add_screen.title("Add tasks")
    add_screen.configure(bg="#9fa0ff")  # Set the background color

    # Configure rows and columns to be expandable
    add_screen.rowconfigure(0, weight=1)
    add_screen.columnconfigure(0, weight=1)

    # Frame to group items
    add_frame = LabelFrame(add_screen)
    add_frame.grid(padx = 10, pady = 10)

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
    This function connects to the database "homework_data.db" and retrieves the tasks from the user's
    designated table based on the provided username, 
    which is obtained from the command-line argument passed from home page.

    If the user's table exists in the database, the function fetches all the tasks from 
    that table and displays them in the graphical user interface (GUI) info_frame. 
    Each task is shown with its subject, homework name, and due date,
    along with a corresponding "Remove" button. 
    The "Remove" button allows the user to delete a specific task from the database.

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
        add_button.grid(row = 1, padx = 5, sticky="W")

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


# GUI Code
root = Tk()
root.title("Homework Tracker App")
root.configure(bg="#4E67EB")  # Set the background color

# Configure rows and columns to be expandable
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)



# Frame for grouping widgets
info_frame = LabelFrame(root)
info_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=30, sticky="NSEW")

# Configure column and row resizing
info_frame.columnconfigure(1, weight=1)

# Display the tasks when the program starts
display_tasks()

# Run the mainloop
root.mainloop()
