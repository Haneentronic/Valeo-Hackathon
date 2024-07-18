import eel
import tkinter as tk
from tkinter import messagebox
import subprocess
eel.init('web')  # Initialize with the 'web' folder where HTML files reside

@eel.expose
def login(role, email, password):
    if email == "mariamashrafff163@gmail.com" and password == "123456" and role == "Developer":
       subprocess.Popen(['python', 'message.py'])
       subprocess.Popen(['python', 'developer.py'])
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
