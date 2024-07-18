import tkinter as tk
from tkinter import messagebox

class SignInApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Valeo Sign-In")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        # Logo or Header
        self.header = tk.Label(self.root, text="Valeo", font=("Arial", 24, "bold"))
        self.header.pack(pady=20)

        # Username
        self.username_label = tk.Label(self.root, text="Username:", font=("Arial", 12))
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.root, font=("Arial", 12))
        self.username_entry.pack(pady=5)

        # Password
        self.password_label = tk.Label(self.root, text="Password:", font=("Arial", 12))
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.root, font=("Arial", 12), show='*')

import os.path
import json
import threading
import tkinter as tk
from tkinter import ttk
import time
from datetime import datetime, timezone
from PIL import Image, ImageTk

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CHECK_INTERVAL = 5  # Check every 5 seconds

class GmailNotifier:
    def __init__(self):
        self.creds = self.authenticate_gmail()
        self.service = build('gmail', 'v1', credentials=self.creds)
        self.displayed_message_ids = set()
        self.app_start_time = datetime.now(timezone.utc)  # Record app start time

        # Create and configure the main window
        self.root = tk.Tk()
        self.root.title("Gmail Notifier")
        self.root.geometry("300x200")  # Set size of main window
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.status_label = tk.Label(self.root, text="Gmail Notifier is running...", font=('calibri', 12))
        self.status_label.pack(pady=20)

    def authenticate_gmail(self):
        """Authenticate Gmail API."""
        creds = None
        if os.path.exists('token.json'):
            try:
                creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            except json.decoder.JSONDecodeError:
                print("Error reading token.json, it might be corrupted. Deleting the file and re-authenticating.")
                os.remove('token.json')
                creds = None

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return creds

    def list_messages(self, user_id='me'):
        """List messages from a specific user."""
        try:
            query = 'from:*@eng.asu.edu.eg'
            response = self.service.users().messages().list(userId=user_id, maxResults=5, q=query).execute()
            messages = response.get('messages', [])
            return messages
        except HttpError as error:
            print(f'An error occurred while listing messages: {error}')
            return []

    def get_message(self, user_id, msg_id):
        """Get a specific message."""
        try:
            message = self.service.users().messages().get(userId=user_id, id=msg_id).execute()
            return message
        except HttpError as error:
            print(f'An error occurred while retrieving message {msg_id}: {error}')
            return None

    def display_message_window(self, sender, subject, snippet):
        """Display a message window with sender, subject, and snippet."""
        def run_window():
            window = tk.Toplevel(self.root)
            window.overrideredirect(True)  # Remove window decorations
            window.attributes("-topmost", True)  # Keep the window on top

            # Position the window at the top-center of the screen
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
            window.geometry(f"400x200+{screen_width // 2 - 200}+10")

            # Create a frame for rounded corners
            frame = tk.Frame(window, bg="#fafbe3", bd=2, relief=tk.RAISED)
            frame.pack(fill=tk.BOTH, expand=True)

            # Load and display message logo
            logo_image = Image.open("message_logo.png")
            logo_image = logo_image.resize((40, 40))
            logo_photo = ImageTk.PhotoImage(logo_image)
            label_logo = tk.Label(frame, image=logo_photo, bg="#fafbe3")
            label_logo.image = logo_photo  # Keep a reference to avoid garbage collection
            label_logo.pack(side=tk.TOP, padx=10, pady=10)

            # Message content
            label_sender = tk.Label(frame, text=f"From: {sender}", font=('Arial', 9), bg="#fafbe3")
            label_sender.pack(anchor='w', padx=10, pady=2)

            label_subject = tk.Label(frame, text=f"Subject: {subject}", font=('Arial', 9), bg="#fafbe3")
            label_subject.pack(anchor='w', padx=10, pady=2)

            label_snippet = tk.Label(frame, text=f"Message: {snippet}", font=('Arial', 9), bg="#fafbe3")
            label_snippet.pack(anchor='w', padx=10, pady=2)
            # Close button
            color1= '#45a049'
            color2= 'WHITE'
            color3= '#00a8ff'
            color4= '#ffd32a'
            close_button = tk.Button(frame, text="ok", command=window.destroy, bg=color1, fg=color2, activebackground=color3, activeforeground=color4,highlightbackground=color2,highlightcolor='WHITE',width=10,height=1,border=0,cursor='hand1',font=('Arial',12))
            close_button.pack(anchor='e', padx=10, pady=10)
            window.mainloop()

        threading.Thread(target=run_window).start()

    def check_for_new_messages(self):
        """Check for new messages and display them directly."""
        try:
            messages = self.list_messages()
            new_messages = [msg for msg in messages if msg['id'] not in self.displayed_message_ids]

            for message in new_messages:
                msg = self.get_message('me', message['id'])
                if msg:
                    msg_snippet = msg.get('snippet', '')
                    msg_subject = None
                    msg_sender = None
                    msg_timestamp = None
                    for header in msg['payload']['headers']:
                        if header['name'] == 'Subject':
                            msg_subject = header['value']
                        elif header['name'] == 'From':
                            msg_sender = header['value']
                        elif header['name'] == 'Date':
                            msg_timestamp = header['value']
                        if msg_subject and msg_sender and msg_timestamp:
                            break
                    if msg_subject and msg_sender and msg_snippet:
                        # Parse message timestamp
                        msg_time = datetime.strptime(msg_timestamp, "%a, %d %b %Y %H:%M:%S %z")
                        # Compare message time with app start time
                        if msg_time > self.app_start_time:
                            # Prepend new message to the text window
                            self.display_message_window(msg_sender, msg_subject, msg_snippet)
                            self.displayed_message_ids.add(message['id'])
        except Exception as e:
            print(f'Error occurred during message check: {e}')

    def run(self):
        """Run the Gmail notifier."""
        threading.Thread(target=self.background_loop).start()
        self.root.mainloop()

    def background_loop(self):
        """Background loop to check for new messages."""
        while True:
            self.check_for_new_messages()
            time.sleep(CHECK_INTERVAL)

    def on_close(self):
        """Handle the close event of the main window."""
        self.root.destroy()

if __name__ == '__main__':
    notifier = GmailNotifier()
    notifier.run()





