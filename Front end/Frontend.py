import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
import requests

def show_login():
    signup_frame.pack_forget()
    login_frame.pack()

def show_signup():
    login_frame.pack_forget()
    signup_frame.pack()

def login():
    role = role_var.get()
    email = entry_email.get()
    password = entry_password.get()
    
    # Validate login credentials
    if role == "Developer" and email == "developer@example.com" and password == "password":
        messagebox.showinfo("Login Success", "Welcome, Developer!")
    elif role == "Support Leader" and email == "support@example.com" and password == "password":
        messagebox.showinfo("Login Success", "Welcome, Support Leader!")
    else:
        messagebox.showerror("Login Failed", "Invalid email, password, or role")

# Function for handling forget password action
def forget_password():
    # Close the current window
    root.withdraw()

    # Create a new window for forget password
    forget_password_window = tk.Toplevel()
    forget_password_window.title("Forget Password")
    forget_password_window.geometry("600x700")

    # Logo
    logo = PhotoImage(file="Logo.png").subsample(2, 2)  # Resize logo for better visibility
    logo_label = tk.Label(forget_password_window, image=logo)
    logo_label.pack(pady=10)

    # Label for "Forgot Password"
    label_forgot_password = tk.Label(forget_password_window, text="Forgot Password", font=("Helvetica", 20, "bold"))
    label_forgot_password.pack(pady=10)

    # Label and entry for email
    label_email = tk.Label(forget_password_window, text="Enter your email to reset password:", font=("Helvetica", 16))
    label_email.pack(pady=10)
    entry_email_forget = tk.Entry(forget_password_window, bg="#68e804", font=("Helvetica", 14))  # Light green background color
    entry_email_forget.pack(pady=10)

    # Reset password button
    reset_password_button = tk.Button(forget_password_window, text="Reset Password", command=lambda: reset_password(entry_email_forget.get()), font=("Helvetica", 16))
    reset_password_button.pack(pady=20)

    # Function to handle reset password action
    def reset_password(email):
        # Implement your logic here to send reset password email or message
        # For demonstration, just show a message
        messagebox.showinfo("Reset Password", f"Password reset instructions sent to {email}")
        forget_password_window.destroy()
        root.deiconify()  # Restore the main window after forget password action

    # Already have an account link
    login_link = tk.Label(forget_password_window, text="Already have an account? Login", fg="blue", cursor="hand2", font=("Helvetica", 14))
    login_link.pack(pady=5)
    login_link.bind("<Button-1>", lambda event: (forget_password_window.destroy(), root.deiconify(), show_login()))

    # Don't have an account link
    signup_link = tk.Label(forget_password_window, text="Don't have an account yet? Create Account", fg="blue", cursor="hand2", font=("Helvetica", 14))
    signup_link.pack(pady=5)
    signup_link.bind("<Button-1>", lambda event: (forget_password_window.destroy(), root.deiconify(), show_signup()))

# Create main window
root = tk.Tk()
root.title("Welcome to innovatehers App")
root.geometry("600x700")  # Adjusted window size for better laptop screen fit

# Add Logo and resize it
logo = PhotoImage(file="Logo.png").subsample(2, 2)  # Resize logo for better visibility
logo_label = tk.Label(root, image=logo)
logo_label.pack(side=tk.TOP, pady=20, anchor=tk.NW)  # Moved logo to the top

# Login frame
login_frame = tk.Frame(root)
login_frame.pack(pady=20)  # Increased padding for better spacing

# Signup frame
signup_frame = tk.Frame(root)

# --- Login Frame Contents ---
# Label for "Log in as"
label_log_in_as = tk.Label(login_frame, text="Welcome to innovatehers App", font=("Helvetica", 20, "bold"))
label_log_in_as.pack(pady=10)

label_log_in_as = tk.Label(login_frame, text="Log in as", font=("Helvetica", 16))
label_log_in_as.pack(pady=5)

# Variable to store selected role
role_var = tk.StringVar(login_frame)
role_var.set("Developer")  # Default value

# Dropdown for role selection
roles = ["Developer", "Support Leader"]
role_dropdown = tk.OptionMenu(login_frame, role_var, *roles)
role_dropdown.config(font=("Helvetica", 14))  # Increased font size for dropdown
role_dropdown.pack(pady=5)

# Email field
label_email = tk.Label(login_frame, text="Email", font=("Helvetica", 16))
label_email.pack(pady=5)
entry_email = tk.Entry(login_frame, bg="#68e804", font=("Helvetica", 14))  # Light green background color
entry_email.pack(pady=5)

# Password field
label_password = tk.Label(login_frame, text="Password", font=("Helvetica", 16))
label_password.pack(pady=5)
entry_password = tk.Entry(login_frame, show="*", bg="#68e804", font=("Helvetica", 14))  # Light green background color
entry_password.pack(pady=5)

# Login button
login_button = tk.Button(login_frame, text="Login", command=login, font=("Helvetica", 16))
login_button.pack(pady=20)

# Forget password link
forget_password_link = tk.Label(login_frame, text="Forget your password?", fg="blue", cursor="hand2", font=("Helvetica", 14))
forget_password_link.pack(pady=10)
forget_password_link.bind("<Button-1>", lambda event: forget_password())

# Signup link
signup_link = tk.Label(login_frame, text="New user? Sign up", fg="blue", cursor="hand2", font=("Helvetica", 14))
signup_link.pack(pady=10)
signup_link.bind("<Button-1>", lambda event: show_signup())

# --- Signup Frame Contents ---
# Signup label
label_new_user = tk.Label(signup_frame, text="Sign Up", font=("Helvetica", 20, "bold"))
label_new_user.pack(pady=10)

# First name field
label_first_name = tk.Label(signup_frame, text="First Name", font=("Helvetica", 16))
label_first_name.pack(pady=5)
entry_first_name = tk.Entry(signup_frame, bg="#68e804", font=("Helvetica", 14))  # Light green background color
entry_first_name.pack(pady=5)

# Last name field
label_last_name = tk.Label(signup_frame, text="Last Name", font=("Helvetica", 16))
label_last_name.pack(pady=5)
entry_last_name = tk.Entry(signup_frame, bg="#68e804", font=("Helvetica", 14))  # Light green background color
entry_last_name.pack(pady=5)

# New email field
label_new_email = tk.Label(signup_frame, text="Email", font=("Helvetica", 16))
label_new_email.pack(pady=5)
entry_new_email = tk.Entry(signup_frame, bg="#68e804", font=("Helvetica", 14))  # Light green background color
entry_new_email.pack(pady=5)

# New password field
label_new_password = tk.Label(signup_frame, text="Password", font=("Helvetica", 16))
label_new_password.pack(pady=5)
entry_new_password = tk.Entry(signup_frame, show="*", bg="#68e804", font=("Helvetica", 14))  # Light green background color
entry_new_password.pack(pady=5)

# Confirm password field
label_confirm_password = tk.Label(signup_frame, text="Confirm Password", font=("Helvetica", 16))
label_confirm_password.pack(pady=5)
entry_confirm_password = tk.Entry(signup_frame, show="*", bg="#68e804", font=("Helvetica", 14))  # Light green background color
entry_confirm_password.pack(pady=5)

# Submit button
create_user_button = tk.Button(signup_frame, text="Submit", font=("Helvetica", 16))
create_user_button.pack(pady=10)

# Login link
login_link = tk.Label(signup_frame, text="Already have an account? Login here", fg="blue", cursor="hand2", font=("Helvetica", 14))
login_link.pack(pady=5)
login_link.bind("<Button-1>", lambda event: show_login())

# Run the application
root.mainloop()
