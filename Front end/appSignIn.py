import eel
import tkinter as tk
from tkinter import messagebox

eel.init('web')  # Initialize with the 'web' folder where HTML files reside

@eel.expose
def login(role, email, password):
    if email == "mariamashrafff163@gmail.com" and password == "123456" and role == "Developer":
        eel.start('developer.html', block=False)  # Open the developer page
    else:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Login Failed", "Invalid email, password, or role")

@eel.expose
def forgetPassword():
    # Implement your forget password logic here
    pass

@eel.expose
def showSignup():
    eel.start('signup.html', block=False)  # Open the signup page

# Start the application with the signin page
eel.start('signin.html', size=(600, 700))
