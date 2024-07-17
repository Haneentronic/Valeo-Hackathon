import tkinter as tk
from tkinter import messagebox, PhotoImage
import imaplib
import email

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
    if email == "mariamashrafff163@gmail.com" and password == "123456" and role == "Developer":
        open_new_page("Welcome, Developer!")
    elif role == "Support Leader" and email == "mariamashrafff163@gmail.com" and password == "123456":
        open_new_page("Welcome, Support Leader!")
    else:
        messagebox.showerror("Login Failed", "Invalid email, password, or role")

def open_new_page(welcome_message):
    # Hide the main login window
    root.withdraw()
    
    # Create a new window for the welcome page
    welcome_window = tk.Toplevel()
    welcome_window.title("Welcome Page")
    welcome_window.geometry("600x400")
    
    # Label for welcome message
    label_welcome = tk.Label(welcome_window, text=welcome_message, font=("Helvetica", 20, "bold"))
    label_welcome.pack(pady=20)
    
    # Button to logout and go back to main login
    logout_button = tk.Button(welcome_window, text="Logout", command=lambda: logout(welcome_window), font=("Helvetica", 16))
    logout_button.pack(pady=20)

def logout(window):
    # Destroy the welcome window and show the main login window
    window.destroy()
    root.deiconify()
def forget_password():
    root.withdraw()

    forget_password_window = tk.Toplevel()
    forget_password_window.title("Forget Password")
    forget_password_window.geometry("600x700")

    logo = PhotoImage(file="Logo.png").subsample(2, 2)
    logo_label = tk.Label(forget_password_window, image=logo)
    logo_label.pack(pady=10)

    label_forgot_password = tk.Label(forget_password_window, text="Forgot Password", font=("Helvetica", 20, "bold"))
    label_forgot_password.pack(pady=10)

    label_email = tk.Label(forget_password_window, text="Enter your email to reset password:", font=("Helvetica", 16))
    label_email.pack(pady=10)
    entry_email_forget = tk.Entry(forget_password_window, bg="#68e804", font=("Helvetica", 14))
    entry_email_forget.pack(pady=10)
    entry_email_forget.bind("<FocusIn>", lambda event: change_entry_color(entry_email_forget))
    entry_email_forget.bind("<FocusOut>", lambda event: reset_entry_color(entry_email_forget))

    reset_password_button = tk.Button(forget_password_window, text="Reset Password", command=lambda: reset_password(entry_email_forget.get()), font=("Helvetica", 16))
    reset_password_button.pack(pady=20)

    def reset_password(email):
        messagebox.showinfo("Reset Password", f"Password reset instructions sent to {email}")
        forget_password_window.destroy()
        root.deiconify()

    login_link = tk.Label(forget_password_window, text="Already have an account? Login", fg="blue", cursor="hand2", font=("Helvetica", 14))
    login_link.pack(pady=5)
    login_link.bind("<Button-1>", lambda event: (forget_password_window.destroy(), root.deiconify(), show_login()))

    signup_link = tk.Label(forget_password_window, text="Don't have an account yet? Create Account", fg="blue", cursor="hand2", font=("Helvetica", 14))
    signup_link.pack(pady=5)
    signup_link.bind("<Button-1>", lambda event: (forget_password_window.destroy(), root.deiconify(), show_signup()))

def change_entry_color(entry):
    entry.config(bg="#ffffff", highlightbackground="#68e804")

def reset_entry_color(entry):
    entry.config(bg="#68e804", highlightbackground="#68e804")

root = tk.Tk()
root.title("Welcome to innovatehers App")
root.geometry("600x700")

logo = PhotoImage(file="Logo.png").subsample(2, 2)
logo_label = tk.Label(root, image=logo)
logo_label.pack(side=tk.TOP, pady=20, anchor=tk.NW)

login_frame = tk.Frame(root)
login_frame.pack(pady=20)

signup_frame = tk.Frame(root)

label_log_in_as = tk.Label(login_frame, text="Welcome to innovatehers App", font=("Helvetica", 20, "bold"))
label_log_in_as.pack(pady=10)

label_log_in_as = tk.Label(login_frame, text="Log in as", font=("Helvetica", 16))
label_log_in_as.pack(pady=5)

role_var = tk.StringVar(login_frame)
role_var.set("Developer")

roles = ["Developer", "Support Leader"]
role_dropdown = tk.OptionMenu(login_frame, role_var, *roles)
role_dropdown.config(font=("Helvetica", 14))
role_dropdown.pack(pady=5)

label_email = tk.Label(login_frame, text="Email", font=("Helvetica", 16))
label_email.pack(pady=5)
entry_email = tk.Entry(login_frame, bg="#68e804", font=("Helvetica", 14))
entry_email.pack(pady=5)
entry_email.bind("<FocusIn>", lambda event: change_entry_color(entry_email))
entry_email.bind("<FocusOut>", lambda event: reset_entry_color(entry_email))

label_password = tk.Label(login_frame, text="Password", font=("Helvetica", 16))
label_password.pack(pady=5)
entry_password = tk.Entry(login_frame, show="*", bg="#68e804", font=("Helvetica", 14))
entry_password.pack(pady=5)
entry_password.bind("<FocusIn>", lambda event: change_entry_color(entry_password))
entry_password.bind("<FocusOut>", lambda event: reset_entry_color(entry_password))

login_button = tk.Button(login_frame, text="Login", command=login, font=("Helvetica", 16))
login_button.pack(pady=20)

forget_password_link = tk.Label(login_frame, text="Forget your password?", fg="blue", cursor="hand2", font=("Helvetica", 14))
forget_password_link.pack(pady=10)
forget_password_link.bind("<Button-1>", lambda event: forget_password())

signup_link = tk.Label(login_frame, text="New user? Sign up", fg="blue", cursor="hand2", font=("Helvetica", 14))
signup_link.pack(pady=10)
signup_link.bind("<Button-1>", lambda event: show_signup())

label_new_user = tk.Label(signup_frame, text="Sign Up", font=("Helvetica", 20, "bold"))
label_new_user.pack(pady=10)

label_first_name = tk.Label(signup_frame, text="First Name", font=("Helvetica", 16))
label_first_name.pack(pady=5)
entry_first_name = tk.Entry(signup_frame, bg="#68e804", font=("Helvetica", 14))
entry_first_name.pack(pady=5)
entry_first_name.bind("<FocusIn>", lambda event: change_entry_color(entry_first_name))
entry_first_name.bind("<FocusOut>", lambda event: reset_entry_color(entry_first_name))

label_last_name = tk.Label(signup_frame, text="Last Name", font=("Helvetica", 16))
label_last_name.pack(pady=5)
entry_last_name = tk.Entry(signup_frame, bg="#68e804", font=("Helvetica", 14))
entry_last_name.pack(pady=5)
entry_last_name.bind("<FocusIn>", lambda event: change_entry_color(entry_last_name))
entry_last_name.bind("<FocusOut>", lambda event: reset_entry_color(entry_last_name))

label_new_email = tk.Label(signup_frame, text="Email", font=("Helvetica", 16))
label_new_email.pack(pady=5)
entry_new_email = tk.Entry(signup_frame, bg="#68e804", font=("Helvetica", 14))
entry_new_email.pack(pady=5)
entry_new_email.bind("<FocusIn>", lambda event: change_entry_color(entry_new_email))
entry_new_email.bind("<FocusOut>", lambda event: reset_entry_color(entry_new_email))

label_new_password = tk.Label(signup_frame, text="Password", font=("Helvetica", 16))
label_new_password.pack(pady=5)
entry_new_password = tk.Entry(signup_frame, show="*", bg="#68e804", font=("Helvetica", 14))
entry_new_password.pack(pady=5)
entry_new_password.bind("<FocusIn>", lambda event: change_entry_color(entry_new_password))
entry_new_password.bind("<FocusOut>", lambda event: reset_entry_color(entry_new_password))

label_confirm_password = tk.Label(signup_frame, text="Confirm Password", font=("Helvetica", 16))
label_confirm_password.pack(pady=5)
entry_confirm_password = tk.Entry(signup_frame, show="*", bg="#68e804", font=("Helvetica", 14))
entry_confirm_password.pack(pady=5)
entry_confirm_password.bind("<FocusIn>", lambda event: change_entry_color(entry_confirm_password))
entry_confirm_password.bind("<FocusOut>", lambda event: reset_entry_color(entry_confirm_password))

create_user_button = tk.Button(signup_frame, text="Submit", font=("Helvetica", 16))
create_user_button.pack(pady=10)

login_link = tk.Label(signup_frame, text="Already have an account? Login here", fg="blue", cursor="hand2", font=("Helvetica", 14))
login_link.pack(pady=5)
login_link.bind("<Button-1>", lambda event: show_login())

root.mainloop()
