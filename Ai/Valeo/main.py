import pandas as pd
import re
import matplotlib.pyplot as plt
from datetime import timedelta, time
import customtkinter as ctk
from tkinter import filedialog, messagebox
from tkinter.ttk import Treeview
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Function to convert time string to hours
def convert_to_hours(time_str):
    if isinstance(time_str, str):
        if 'day' in time_str:
            days, time_part = time_str.split(', ')
            days = int(days.split()[0])
            match = re.match(r'(\d+):(\d+):(\d+)', time_part)
            if match:
                hours = int(match.group(1)) + days * 24
                minutes = int(match.group(2))
                seconds = int(match.group(3))
                total_hours = hours + minutes / 60 + seconds / 3600
                return total_hours
        else:
            match = re.match(r'(?:(\d+):)?(\d+):(\d+)', time_str)
            if match:
                hours = int(match.group(1) or 0)
                minutes = int(match.group(2))
                seconds = int(match.group(3))
                total_hours = hours + minutes / 60 + seconds / 3600
                return total_hours
    return 0


# Function to check if a ticket is delayed
def check_delay(row):
    return pd.to_numeric(row['Time_to_resolution_hours'], errors='coerce') < 0


# Function to get timezone based on zone
def get_timezone(zone):
    if zone == 'CET':
        return 'Egypt'
    elif zone == 'Chennai':
        return 'India'
    else:
        return None


# Function to check if time is outside working hours
def is_outside_working_hours(executed_date, zone_from, zone_to, timezone):
    time_difference = pd.Timedelta(hours=3, minutes=30)
    if zone_from == 'CET' and zone_to == 'Chennai':
        india_time = executed_date + time_difference
    elif zone_from == 'Chennai' and zone_to == 'CET':
        india_time = executed_date - time_difference
    else:
        india_time = executed_date

    day = india_time.strftime('%A')
    time_of_day = india_time.time()
    working_hours_india = {
        'Sunday': [(time(9, 0), time(17, 0))],
        'Monday': [(time(9, 0), time(17, 0))],
        'Tuesday': [(time(9, 0), time(17, 0))],
        'Wednesday': [(time(9, 0), time(17, 0))],
        'Thursday': [(time(9, 0), time(17, 0))],
        'Friday': [(time(9, 0), time(17, 0))]
    }
    for start, end in working_hours_india.get(day, []):
        if start <= time_of_day <= end:
            return True
    return False


# Function to determine reasons for breaches
def determine_reason(row):
    reasons = []
    if row['outside']:
        reasons.append("Time difference")
    if row['Breached']:
        reasons.append(f"the team {row['Team']} took more time ")
    return " and ".join(reasons) if reasons else "No reason"


# Main function to process the dataset
def process_dataset(data):
    static_data_With_sla = data['Static Data with SLA Info']
    assignee_team_mapping = data['AssigneeTeam Mapping']
    transition_history = data['Refined Transition History']
    static_data = data['Static Data']

    static_data_With_sla['Time to resolution'] = static_data_With_sla['Time to resolution'].astype(str)
    static_data_With_sla['Time_to_resolution_hours'] = static_data_With_sla['Time to resolution'].apply(
        convert_to_hours)
    static_data_With_sla['Delayed'] = static_data_With_sla.apply(check_delay, axis=1)

    delayed_tickets = static_data_With_sla[static_data_With_sla['Delayed']]
    delayed_tickets = pd.merge(delayed_tickets, assignee_team_mapping, how='left', left_on='Assignee', right_on='Email')
    delayed_tickets.drop('Email', axis=1, inplace=True)

    transition_history['executed_date'] = pd.to_datetime(transition_history['executed_date'], format='ISO8601')
    transition_history['time_spent'] = transition_history.groupby('Ticket_ID')[
                                           'executed_date'].diff().dt.total_seconds() / 3600

    for i in range(1, len(transition_history)):
        if transition_history.iloc[i - 1]['_to'] == 'REQUEST FEEDBACK' and transition_history.iloc[i][
            '_from'] == 'REQUEST FEEDBACK':
            transition_history.at[i - 1, 'time_spent'] = 0.000000

    transition_history['time_spent'] = transition_history['time_spent'].fillna(0)
    transition_with_team = pd.merge(transition_history, assignee_team_mapping, how='left', left_on='_to',
                                    right_on='Assignee')
    transition_with_team['Team'] = transition_with_team.groupby('Ticket_ID')['Team'].ffill()
    transition_with_team['Email'] = transition_with_team.groupby('Ticket_ID')['Email'].ffill()
    transition_with_team['Zone'] = transition_with_team.groupby('Ticket_ID')['Zone'].ffill()

    transition_with_team_priority = pd.merge(transition_with_team, static_data_With_sla, how='left',
                                             left_on='Ticket_ID', right_on='Issue key')
    transition_with_team_priority.drop(['Status', 'Resolution', 'Created', 'Updated', 'Resolved'], axis=1, inplace=True)

    df_team_ticket = transition_with_team_priority.groupby(['Ticket_ID', 'Team', 'Priority'])[
        'time_spent'].sum().reset_index()
    average_time_per_team_priority = df_team_ticket.groupby(['Team', 'Priority'])['time_spent'].mean().reset_index()

    delayed_tickets = delayed_tickets.merge(df_team_ticket[['Ticket_ID', 'Team', 'time_spent', 'Priority']],
                                            left_on='Issue key', right_on='Ticket_ID', how='left',
                                            suffixes=('', '_actual'))
    delayed_tickets = delayed_tickets.merge(average_time_per_team_priority, on=['Team', 'Priority'], how='left')
    delayed_tickets['Breached'] = delayed_tickets['time_spent_x'] > delayed_tickets['time_spent_y']

    assignee_team_mapping['timezone'] = assignee_team_mapping['Zone'].apply(get_timezone)
    transition_history = transition_history.merge(assignee_team_mapping[['Assignee', 'Zone', 'timezone']],
                                                  left_on='_to', right_on='Assignee', how='left')
    transition_history['Assignee'] = transition_history['Assignee'].fillna(method='ffill')
    transition_history['Zone'] = transition_history['Zone'].fillna(method='ffill')
    transition_history['timezone'] = transition_history['timezone'].fillna(method='ffill')

    transition_history['outside_working_hours'] = transition_history.apply(
        lambda x: is_outside_working_hours(x['executed_date'], x['Zone'], 'Chennai' if x['Zone'] == 'CET' else 'CET',
                                           x['timezone']), axis=1
    )

    out_work = transition_history[transition_history['outside_working_hours'] == False]
    delayed_tickets = delayed_tickets.merge(out_work[['Ticket_ID', 'outside_working_hours']], left_on='Issue key',
                                            right_on='Ticket_ID', how='left')
    delayed_tickets['outside_working_hours'] = delayed_tickets['outside_working_hours'].fillna(True)
    delayed_tickets = delayed_tickets.drop_duplicates(subset='Issue key')
    delayed_tickets = delayed_tickets.rename(columns={'outside_working_hours': 'outside'})

    delayed_tickets['Reason'] = delayed_tickets.apply(determine_reason, axis=1)
    # Keep only 'Issue key' and 'Reason' columns
    delayed_tickets = delayed_tickets[['Issue key', 'Reason']]
    return delayed_tickets


# Function to plot the reasons for breaches
def plot_reasons(delayed_tickets, frame):

    reason_counts = delayed_tickets['Reason'].value_counts()
    total_delayed = reason_counts.sum()
    reason_percentages = reason_counts / total_delayed * 100

    plt.figure(figsize=(14, 14))
    bars = plt.bar(reason_percentages.index, reason_percentages.values, color='skyblue', edgecolor='black')

    plt.xlabel('Reason', fontsize=12, fontweight='bold')
    plt.ylabel('Percentage of Delayed Tickets', fontsize=12, fontweight='bold')
    plt.title('Percentage of Delayed Tickets by Reason', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Add data labels on the bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, f'{yval:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')

    # Clear the frame
    for widget in frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(plt.gcf(), master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

    plt.close()


# GUI Application
class Application:
    def __init__(self, master):
        self.master = master
        master.title("Ticket Breach Analyzer")

        self.label = ctk.CTkLabel(master, text="Upload your dataset and analyze ticket breaches",
                                  font=('Helvetica', 14))
        self.label.pack(pady=10)

        self.upload_button = ctk.CTkButton(master, text="Upload Dataset", command=self.upload_dataset)
        self.upload_button.pack(pady=5)

        self.process_button = ctk.CTkButton(master, text="Process Dataset", command=self.process_dataset,
                                            state='disabled')
        self.process_button.pack(pady=5)

        self.results_frame = ctk.CTkFrame(master)
        self.results_frame.pack(fill='both', expand=True, padx=10, pady=10)

    def upload_dataset(self):
        self.filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if self.filepath:
            self.data = pd.read_excel(self.filepath, sheet_name=None)
            messagebox.showinfo("Dataset Uploaded", "Dataset uploaded successfully!")
            self.process_button.configure(state='normal')

    def process_dataset(self):
        if hasattr(self, 'data'):
            delayed_tickets = process_dataset(self.data)
            self.show_results(delayed_tickets)
            plot_reasons(delayed_tickets, self.results_frame)
        else:
            messagebox.showerror("No Dataset", "Please upload a dataset first.")

    def show_results(self, delayed_tickets):
        top = ctk.CTkToplevel(self.master)
        top.title("Delayed Tickets")

        frame = ctk.CTkFrame(top)
        frame.pack(fill='both', expand=True)

        tree = Treeview(frame, columns=("Issue key", "Reason"), show='headings')
        tree.heading("Issue key", text="Issue Key")
        tree.heading("Reason", text="Reason")

        for index, row in delayed_tickets.iterrows():
            tree.insert("", "end", values=(row["Issue key"], row["Reason"]))

        tree.pack(fill='both', expand=True)


root = ctk.CTk()
app = Application(root)
root.mainloop()
