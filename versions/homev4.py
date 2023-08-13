"""
Automatically changed the entered user name'ss first letter into upper case
to improve user's experience as first letter of name is always capitalised. 
"""

"""
Imports:
1. Tkinter module for creating the GUI
2. SQLite database
3. For running external processes
"""

# Imports
from tkinter import (
    Tk,
    Label,
    Entry,
    Button,
    StringVar,
    Toplevel,
    END,
    LabelFrame,
    PhotoImage,
    LEFT,
)
import sqlite3
import sys
import subprocess

# Class for Registration Window
class RegistrationWindow:
    """
    This class provides a graphical user interface for users to register
    by entering their desired username and password.
    The user data is then stored in a SQLite database for further processing.
    """

    def __init__(self, main_window):
        """
        Initializes the RegistrationWindow instance.
        """
        # main window assigned to sself_root
        self.root = main_window
        # Create new wiindow with main_window as parent
        self.register_screen = Toplevel(self.root)
        self.register_screen.title("Register")
        self.register_screen.configure(bg="#9fa0ff")

        # Declare StringVar() objects to store the values entered by the user
        self.username = StringVar()
        self.password = StringVar()

        # Frame to group items
        register_frame = LabelFrame(self.register_screen)
        register_frame.grid(padx=10, pady=10)

        # Label to display register instructions
        register_label = Label(
            register_frame,
            text="Please enter details in given entry fields",
            bg="#F0F4FF",
            fg="black",
        )
        register_label.grid(padx=20, pady=10)

        # Label of username
        username_label = Label(register_frame, text="Username: ")
        username_label.grid(pady=10)

        # Entry of username
        self.username_entry = Entry(register_frame, textvariable=self.username)
        self.username_entry.grid(pady=10)

        # Label for password
        password_label = Label(register_frame, text="Password: ")
        password_label.grid(pady=10)

        # Entry for password
        self.password_entry = Entry(
            register_frame, textvariable=self.password, show="*"
        )
        self.password_entry.grid(pady=10)

        # After clicking register button, register_user method will run
        registered_button = Button(
            register_frame,
            text="Register",
            width=10,
            height=1,
            command=self.register_user,
        )
        registered_button.grid(pady=5)

    def register_user(self):
        """
        Retrieves the username and password entered by the user.
        Validates the input and performs the registration process.
        Stores the user data in the database if the registration is successful.
        """
        # Retrieve the username and password entered by the user
        username_info = self.username.get()
        password_info = self.password.get()

        # Check if both username and password are provided
        if not username_info or not password_info:
            reminder_label = Label(
                self.register_screen,
                text="Please enter both username and password!",
                fg="red",
            )
            reminder_label.grid(pady=5)

            # Schedule the reminder label to disappear after 2000 milliseconds (2 seconds)
            self.register_screen.after(2000, reminder_label.destroy)
            return

        # Check if the username and password contain spaces
        if " " in username_info or " " in password_info:
            reminder_label = Label(
                self.register_screen,
                text="Username and password cannot contain spaces!",
                fg="red",
            )
            reminder_label.grid(pady=5)

            # Schedule the reminder label to disappear after 2000 milliseconds (2 seconds)
            self.register_screen.after(2000, reminder_label.destroy)
            return

        # Check if the username length is more than 10 characters
        if len(username_info) > 10:
            reminder_label = Label(
                self.register_screen,
                text="Username should be less than 10 characters!",
                fg="red",
            )
            reminder_label.grid(pady=5)

            # Schedule the reminder label to disappear after 2000 milliseconds (2 seconds)
            self.register_screen.after(2000, reminder_label.destroy)
            return

        # Open a connection to the database
        conn = sqlite3.connect("db/user_data.db")
        cursor = conn.cursor()

        # Check if the provided username already exists in the database
        cursor.execute(
            """SELECT * FROM users WHERE username=?""",
            (username_info,),
        )
        existing_user = cursor.fetchone()

        # Close the connection
        conn.close()

        # Check if a user with the same username already exists
        if existing_user is not None:
            reminder_label = Label(
                self.register_screen,
                text="Username already exists!",
                fg="red",
            )
            reminder_label.grid(pady=5)

            # Schedule the reminder label to disappear after 2000 milliseconds (2 seconds)
            self.register_screen.after(2000, reminder_label.destroy)
            return

        # If the username is unique, proceed with the registration
        conn = sqlite3.connect("db/user_data.db")
        cursor = conn.cursor()

        # Insert the user data into the table
        cursor.execute(
            """
        INSERT INTO users (username, password)
        VALUES (?, ?)""",
            (username_info, password_info),
        )

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        # Clear the username and password entry fields
        self.username_entry.delete(0, END)
        self.password_entry.delete(0, END)

        # Create a label to display the registration success message
        register_success_label = Label(
            self.register_screen, text="Registration Successful!", fg="green"
        )
        register_success_label.grid(pady=5)

        # Schedule the success label to disappear after 2000 milliseconds (2 seconds)
        self.register_screen.after(2000, register_success_label.destroy)


# Window for registration
def register():
    """
    Create a registration window where users can enter their details to register a new account.
    """
    RegistrationWindow(root)


# Function to compare the login details from entry with database
def login_verify():
    """
    Retrieves the username, password, and name entered by the user from the login
    entry fields.
    If a matching user is found, the main application window is opened,
    passing the username and name as arguments to the new window.
    Otherwise, an error message is displayed.
    """
    # Get the username, password, and name entered by the user
    username1 = username_verify.get()
    password1 = password_verify.get()
    name_value = name.get()

    # Clear the login entry fields
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)

    # Check if the name is provided
    if not name_value:
        # If the name is not provided, display an error message
        reminder_label = Label(login_frame, text="Please enter your name!", fg="red")
        reminder_label.grid(pady=5)

        # Schedule the reminder label to disappear after 2000 milliseconds (2 seconds)
        login_frame.after(2000, reminder_label.destroy)
        return

    # Check if the name contain spaces
    if " " in name_value:
        reminder_label = Label(
            login_frame,
            text="Name cannot contain spaces!",
            fg="red",
        )
        reminder_label.grid(pady=5)

        # Schedule the reminder label to disappear after 2000 milliseconds (2 seconds)
        login_frame.after(2000, reminder_label.destroy)
        return

    # Open a connection to the database
    conn = sqlite3.connect("db/user_data.db")
    cursor = conn.cursor()

    # Execute a query to find the user with the given username and password
    cursor.execute(
        """
        SELECT * FROM users WHERE username=? AND password=?
    """,
        (username1, password1),
    )

    # Fetch the result of the query
    result = cursor.fetchone()

    # Close the connection
    conn.close()

    # Check if a matching user was found
    if result is not None:
        root.destroy()
        # Open next window and pass the username as an argument
        subprocess.Popen([sys.executable, "task_display.py", username1, name_value])
    else:
        # If no matching user was found, display an error message
        reminder_label = Label(
            login_frame,
            text="User not found!",
            fg="red",
        )
        reminder_label.grid(pady=5)

        # Schedule the reminder label to disappear after 2000 milliseconds (2 seconds)
        login_frame.after(2000, reminder_label.destroy)
        return


# GUI Code
root = Tk()
root.title("Homework Tracker App")
root.configure(bg="#4E67EB")  # Set the background color

# Disable window resizing (lock the window size)
root.resizable(False, False)

# Configure rows and columns to be expandable
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

# 3 frames for section grouping
# Create the frame displaying basic information
intro_frame = LabelFrame(root)
intro_frame.grid(row=0, column=0, padx=10, pady=10, sticky="NSEW")

# Create the frame displaying informations
instruction_frame = LabelFrame(root)
instruction_frame.grid(row=1, padx=10, pady=10, sticky="NSEW")

# Create bottom frame for logging in
login_frame = LabelFrame(root, text="Login Details")
login_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="NSEW")

# Configure column and row resizing
intro_frame.columnconfigure(1, weight=1)
instruction_frame.columnconfigure(1, weight=1)
login_frame.columnconfigure(1, weight=1)

# Create PhotoImage and subsample method to reduce size
logo_image = PhotoImage(file="assets/logo.png")
smaller_image = logo_image.subsample(2, 2)

# Hold image label
logo_label = Label(intro_frame, image=smaller_image)
logo_label.grid(row=0, column=0, padx=8, pady=8)

# Create and set the Title message text variable
title_label = Label(intro_frame, text="Homework Tracker", font=("Arial", 20, "bold"))
title_label.grid(row=0, column=1, padx=5)

# Create and set the short description text variable
description_label = Label(
    intro_frame,
    # List of the instructions
    text="This homework tracker app created using Tkinter"
    " will allow you to easily record and keep track of your"
    " assignments or homework online",
    wraplength=370,
    justify="left",
)
description_label.grid(row=1, columnspan=2, padx=8, pady=8, sticky="W")

# Create variable and initialise with starting text
# Create instruction list
INSTRUCTIONS_TEXT = "\nHow to use:\n\n"
instructions = [
    "Enter your name, username and password to login ",
    "You will be able to view the work you have added before ",
    "You can add a new task and select a due date for it, and it will be added to the list ",
    "You could also delete the work you finished ",
]

# Enumerate to provide index starting from 1
for index, instruction in enumerate(instructions, start=1):
    INSTRUCTIONS_TEXT += f"{index}. {instruction}\n"

# Create label and allign it to left
instructions_label = Label(
    instruction_frame, text=INSTRUCTIONS_TEXT, justify=LEFT, wraplength=300
)
instructions_label.grid(row=0, column=1, padx=5)

# Login frame title
logtitle_label = Label(login_frame, text="Login", font=("Arial", 20))
logtitle_label.grid(row=0, padx=8, pady=5)

# Label for login details frame
sign_label = Label(login_frame, text="Please sign in to continue", font=("Arial", 15))
sign_label.grid(row=1, padx=20, pady=15)

# Create a label for the amount field and pack it into the GUI
name_label = Label(login_frame, text="Name:")
name_label.grid(row=2, pady=10)

# Create a variable to store the name and display later
name = StringVar()
name.set("")

# Create an entry to type in name
name_entry = Entry(login_frame, textvariable=name, width=15)
name_entry.grid(row=3, pady=10, padx=10)

username_verify = StringVar()
password_verify = StringVar()

# Label for username
login_username_label = Label(login_frame, text="Username: ")
login_username_label.grid(row=4, pady=10)

# Entry for username
username_login_entry = Entry(login_frame, textvariable=username_verify, width=15)
username_login_entry.grid(row=5, pady=10)

# Label for password
login_password_label = Label(login_frame, text="Password: ")
login_password_label.grid(row=6, pady=10)

# Entry for password
password_login_entry = Entry(
    login_frame, textvariable=password_verify, show="*", width=15
)
password_login_entry.grid(row=7, pady=10)


# Button for user to login
login_button = Button(login_frame, text="Login", command=login_verify)
login_button.grid()

# Button for user to register new account
register_button = Button(login_frame, text="Register", command=register)
register_button.grid()

# Label to display login result
login_result_label = Label(login_frame, text="", fg="red")
login_result_label.grid()


# Run the mainloop
root.mainloop()
