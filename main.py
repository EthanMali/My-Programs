import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

# Global Variables
filename = 'passwords.json'

# Function to read passwords from a file
def read_passwords_from_file(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}  # Return empty dictionary if file doesn't exist
    except json.JSONDecodeError:
        return {}  # Handle JSON decoding errors gracefully

# Function to save passwords to a file
def save_passwords_to_file(filename, passwords):
    with open(filename, 'w') as file:
        json.dump(passwords, file, indent=4)

# Function to create a new user account
def signup():
    global user_password
    new_password = simpledialog.askstring("Signup", "Choose your Master Password:", show='*')
    if new_password:
        user_password = new_password
        if not os.path.exists(filename):
            # Create an empty passwords file if it doesn't exist
            with open(filename, 'w') as file:
                json.dump({}, file)
        messagebox.showinfo("Signup Successful", "Your account has been created successfully!")

# Function to handle password validation and display stored passwords
def show_stored_passwords():
    password = password_entry.get()
    if password == user_password:
        stored_passwords_text.delete(1.0, tk.END)
        stored_passwords_text.insert(tk.END, "Stored Passwords:\n")
        for service, pwd in user_stored_passwords.items():
            stored_passwords_text.insert(tk.END, f"{service} - {pwd}\n")
    else:
        messagebox.showerror("Error", "Incorrect Password")

# Function to handle adding a new password
def add_password():
    service = service_entry.get()
    new_password = new_password_entry.get()
    user_stored_passwords[service] = new_password
    save_passwords_to_file(filename, user_stored_passwords)
    messagebox.showinfo("Success", f"Password for {service} added successfully.")
    clear_entries()
    show_stored_passwords()  # Update displayed passwords after adding

# Function to clear entry fields after an operation
def clear_entries():
    service_entry.delete(0, tk.END)
    new_password_entry.delete(0, tk.END)

# GUI elements
root = tk.Tk()
root.title("Password Manager")

frame_signup = tk.Frame(root, padx=10, pady=10)
frame_signup.pack()

signup_button = tk.Button(frame_signup, text="Signup", command=signup, font=("Arial", 12))
signup_button.pack()

frame_password = tk.Frame(root, padx=10, pady=10)
frame_password.pack()

password_label = tk.Label(frame_password, text="Enter Master Password:", font=("Arial", 12))
password_label.grid(row=0, column=0, sticky="w")

password_entry = tk.Entry(frame_password, show='*', font=("Arial", 12))
password_entry.grid(row=0, column=1, padx=10)

show_passwords_button = tk.Button(frame_password, text="Show Stored Passwords", command=show_stored_passwords, font=("Arial", 12))
show_passwords_button.grid(row=0, column=2, padx=10)

stored_passwords_text = tk.Text(root, height=10, width=50, font=("Arial", 12))
stored_passwords_text.pack(pady=10)

frame_add_password = tk.Frame(root, padx=10, pady=10)
frame_add_password.pack()

service_label = tk.Label(frame_add_password, text="Service Name:", font=("Arial", 12))
service_label.grid(row=0, column=0, sticky="w")

service_entry = tk.Entry(frame_add_password, font=("Arial", 12))
service_entry.grid(row=0, column=1, padx=10)

new_password_label = tk.Label(frame_add_password, text="New Password:", font=("Arial", 12))
new_password_label.grid(row=1, column=0, sticky="w")

new_password_entry = tk.Entry(frame_add_password, show='*', font=("Arial", 12))
new_password_entry.grid(row=1, column=1, padx=10)

add_password_button = tk.Button(frame_add_password, text="Add Password", command=add_password, font=("Arial", 12))
add_password_button.grid(row=2, columnspan=2, pady=5)

quit_button = tk.Button(root, text="Quit", command=root.quit, font=("Arial", 12))
quit_button.pack(pady=10)

# Load stored passwords at startup
user_stored_passwords = read_passwords_from_file(filename)

# Start the main Tkinter event loop
root.mainloop()
