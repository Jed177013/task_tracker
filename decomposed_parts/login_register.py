"""
This program is a simple login and registration system implemented using the 
Tkinter library in Python. 
It provides a graphical user interface where users 
can enter their username and password to log in or register a new account.
"""

from tkinter import *
import os

# Window for registration
def register():
    """
    Create a registration window where users can enter their details to register a new account.
    """
    # Declare global variable to store the reference to the register screen window
    global register_screen

    register_screen = Toplevel(root)
    register_screen.title("Register")
    register_screen.geometry("300x250") # Set the fixed window size (width x height)
    register_screen.configure(bg="#4E67EB")  # Set the background color

    # Configure rows and columns to be expandable
    register_screen.rowconfigure(0, weight=1)
    register_screen.columnconfigure(0, weight=1)
    
    # Frame to group items
    register_frame  = LabelFrame(register_screen)
    register_frame.grid()

    # Declare global variables to store references to the Tkinter StringVar() 
    global username
    global password
    global username_entry
    global password_entry

    # Create instances of the StringVar() class, 
    # They are used to store the values entered by the user in the username and password Entry widgets. 
    # The StringVar() objects allow updating of the widget values.
    username = StringVar()
    password = StringVar()

    # Label to display register instructions
    register_label = Label(register_frame, text="Please enter details below", bg="blue")
    register_label.grid()

    # Label of username
    r_username_lable = Label(register_frame, text="Username: ")
    r_username_lable.grid()

    # Entry of username
    r_username_entry = Entry(register_frame, textvariable=username)
    r_username_entry.grid()

    # Label for password
    r_password_lable = Label(register_frame, text="Password: ")
    r_password_lable.grid()

    # Entry for password
    r_password_entry = Entry(register_frame, textvariable=password, show='*')
    r_password_entry.grid()

    # After clicking register button, register_user function will run
    register_button = Button(register_frame, text="Register", width=10, height=1, bg="blue", command=register_user)
    register_button.grid()

# Implementing event on register button
def register_user():
    """
    Register the user by storing their username and password in a file.
    """

    # Retrieve the username and password entered by the user
    username_info = username.get()
    password_info = password.get()

    # Open a file with the username as the filename in write mode
    file = open(username_info, "w")

    # Write the username and password to the file
    file.write(username_info + "\n")
    file.write(password_info)

    # Close the file
    file.close()

    # Clear the username and password entry fields
    username_entry.delete(0, END)
    password_entry.delete(0, END)

    # Display a success message in the registration screen
    Label(register_screen, text="Registration Success", fg="green", font=("calibri", 11)).grid()

# Implementing event on login button
def login_verify():
    """
    Verify the username and password entered by the user during login.
    If the credentials are correct, display a success message. 
    Otherwise, display appropriate error messages.
    """

    # Get the username and password entered by the user
    username1 = username_verify.get()
    password1 = password_verify.get()

    # Clear the login entry fields
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)

    # Get the list of files in the current directory
    list_of_files = os.listdir()

    # Check if the entered username exists in the list of files
    if username1 in list_of_files:
        # If the username exists, open the corresponding file
        file1 = open(username1, "r")
        # Read the content of the file and split it into lines
        verify = file1.read().splitlines()
        file1.close()

        # Check if the entered password matches the stored password
        if password1 in verify:
            # If the password matches, display a success message
            login_success_message()
        else:
            # If the password does not match, display an error message
            password_not_recognised_message()
    else:
        # If the username does not exist, display an error message
        user_not_found_message()

# Display login success message
def login_success_message():
    login_result_label.config(text="Login Successful!", fg="green")

# Display password not recognized message
def password_not_recognised_message():
    login_result_label.config(text="Incorrect Password!", fg="red")

# Display user not found message
def user_not_found_message():
    login_result_label.config(text="User Not Found!", fg="red")

# GUI Code
root = Tk()
root.title("Login")
root.configure(bg="#4E67EB") # Background colour
root.geometry("420x500") # Fixed window size

# Configure rows and columns to be expandable
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

# Create a frame to group items
login_frame = LabelFrame(root, text = "Login Details")
login_frame.grid(padx = 5, pady  = 5)

global username_verify
global password_verify

username_verify = StringVar()
password_verify = StringVar()

global username_login_entry
global password_login_entry

# Label for username
username_label = Label(login_frame, text="Username: ")
username_label.grid()

# Entry for username
username_login_entry = Entry(login_frame, textvariable=username_verify)
username_login_entry.grid()

# Label for password
password_label = Label(login_frame, text="Password: ")
password_label.grid()

# Entry for password
password_login_entry = Entry(login_frame, textvariable=password_verify, show='*')
password_login_entry.grid()

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