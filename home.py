import tkinter as tk
from tkinter import messagebox
import subprocess

# Sample user data (in a real application, use a database)
user_data = {
    'user1': 'password1',
    'user2': 'password2',
    'user3': 'password3'
}

def login():
    username = username_entry.get()
    password = password_entry.get()

    if username in user_data and user_data[username] == password:
        messagebox.showinfo("Login Successful", "Welcome, {}".format(username))
        subprocess.run(['python','app.py'])
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# Create the main window
root = tk.Tk()
root.title("User Login")

# Create labels, entry widgets, and login button
username_label = tk.Label(root, text="Username:")
username_entry = tk.Entry(root)

password_label = tk.Label(root, text="Password:")
password_entry = tk.Entry(root, show="*")  # Show * for password input

login_button = tk.Button(root, text="Login", command=login)

# Place widgets in the window using grid
username_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)
username_entry.grid(row=0, column=1, padx=10, pady=10)

password_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
password_entry.grid(row=1, column=1, padx=10, pady=10)

login_button.grid(row=2, column=1, pady=10)

# Run the main loop
root.mainloop()
