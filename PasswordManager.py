import os
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import messagebox
import csv
import pyperclip  # Make sure to install the pyperclip library for clipboard functionality

# Use the correct generated key here (Replace with the generated key)
key = b'4rb1--uM_fygwnRg1wpnT4uSY5x9cV7D4FcN5V4E8B4='  # Replace with the generated key
cipher_suite = Fernet(key)

# Function to save the password securely
def save_password():
    username = username_entry.get()
    site = site_entry.get()
    password = password_entry.get()

    # Check if fields are empty
    if not username or not site or not password:
        messagebox.showerror("Error", "All fields must be filled!")
        return

    # Encrypt the password
    encrypted_password = cipher_suite.encrypt(password.encode()).decode()

    # Save to CSV
    try:
        with open('passwords.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, site, encrypted_password])
        messagebox.showinfo("Success", "Password saved successfully!")
        clear_fields()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to clear all input fields
def clear_fields():
    username_entry.delete(0, tk.END)
    site_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

# Function to view saved passwords
def view_passwords():
    try:
        with open('passwords.csv', mode='r') as file:
            reader = csv.reader(file)
            display_passwords(reader)
    except FileNotFoundError:
        messagebox.showerror("Error", "No password file found!")

# Function to display saved passwords and add Copy buttons and Reveal functionality
def display_passwords(reader):
    display_window = tk.Toplevel(root)
    display_window.title("Saved Passwords")
    display_window.geometry("600x400")

    # Create a scrollable frame
    frame = tk.Frame(display_window)
    frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(frame)
    scroll_y = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scroll_y.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    canvas.configure(yscrollcommand=scroll_y.set)

    frame_canvas = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame_canvas, anchor="nw")

    # Headers
    headers = ["Username", "Site", "Password"]
    for col_num, header in enumerate(headers):
        label = tk.Label(frame_canvas, text=header, font=("Arial", 12, "bold"))
        label.grid(row=0, column=col_num, padx=10, pady=10)

    # Populate with saved passwords
    row_num = 1
    for row in reader:
        username, site, encrypted_password = row
        decrypted_password = cipher_suite.decrypt(encrypted_password.encode()).decode()

        # Display username, site, and password (hidden by default)
        tk.Label(frame_canvas, text=username).grid(row=row_num, column=0, padx=10, pady=10)
        tk.Label(frame_canvas, text=site).grid(row=row_num, column=1, padx=10, pady=10)

        password_label = tk.Label(frame_canvas, text="********", name=f"password_{row_num}")
        password_label.grid(row=row_num, column=2, padx=10, pady=10)

        # Create a Copy button for each password
        copy_button = tk.Button(frame_canvas, text="Copy", command=lambda password=decrypted_password: copy_password(password))
        copy_button.grid(row=row_num, column=3, padx=10, pady=10)

        # Create a Reveal button to toggle the password visibility
        reveal_button = tk.Button(frame_canvas, text="Reveal", command=lambda label=password_label, password=decrypted_password: toggle_password(label, password))
        reveal_button.grid(row=row_num, column=4, padx=10, pady=10)

        row_num += 1

    frame_canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

# Function to copy password to clipboard
def copy_password(password):
    pyperclip.copy(password)
    messagebox.showinfo("Copied", "Password copied to clipboard!")

# Function to toggle password visibility
def toggle_password(password_label, password):
    if password_label.cget("text") == "********":
        password_label.config(text=password)  # Reveal the password
    else:
        password_label.config(text="********")  # Hide the password

# Function to handle arrow key navigation
def navigate(event):
    if event.keysym == 'Down':
        if event.widget == password_entry:
            username_entry.focus_set()  # Cycle back to the first field
        elif event.widget == site_entry:
            password_entry.focus_set()
        elif event.widget == username_entry:
            site_entry.focus_set()
    elif event.keysym == 'Up':
        if event.widget == username_entry:
            password_entry.focus_set()  # Cycle forward to the last field
        elif event.widget == site_entry:
            username_entry.focus_set()
        elif event.widget == password_entry:
            site_entry.focus_set()

# Function to handle Delete key (clear all fields)
def clear_on_delete(event):
    if event.keysym == 'Delete':
        clear_fields()

# Create the main window
root = tk.Tk()
root.title("Password Manager")
root.geometry("400x300")

# Ensure correct file path for the image (use the absolute path relative to the script)
icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logo.png')

# Try to set the icon, with a fallback in case of failure
try:
    root.iconphoto(False, tk.PhotoImage(file=icon_path))
except Exception as e:
    # If the image is not found, print a message and use the default icon (no error is shown)
    print(f"Icon not found, using default icon: {str(e)}")

# Heading label
heading_label = tk.Label(root, text="Password Manager", font=("Arial", 16, "bold"))
heading_label.pack(pady=10)

# Input frame
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

# Username input
username_label = tk.Label(input_frame, text="Username:")
username_label.grid(row=0, column=0, padx=5, pady=5)
username_entry = tk.Entry(input_frame, width=30)
username_entry.grid(row=0, column=1, padx=5, pady=5)
username_entry.bind('<Down>', navigate)
username_entry.bind('<Up>', navigate)

# Site input
site_label = tk.Label(input_frame, text="Site:")
site_label.grid(row=1, column=0, padx=5, pady=5)
site_entry = tk.Entry(input_frame, width=30)
site_entry.grid(row=1, column=1, padx=5, pady=5)
site_entry.bind('<Down>', navigate)
site_entry.bind('<Up>', navigate)

# Password input
password_label = tk.Label(input_frame, text="Password:")
password_label.grid(row=2, column=0, padx=5, pady=5)
password_entry = tk.Entry(input_frame, width=30, show="*")
password_entry.grid(row=2, column=1, padx=5, pady=5)
password_entry.bind('<Down>', navigate)
password_entry.bind('<Up>', navigate)

# Buttons frame
buttons_frame = tk.Frame(root)
buttons_frame.pack(pady=10)

# Save button
save_button = tk.Button(buttons_frame, text="Save Password", command=save_password)
save_button.grid(row=0, column=0, padx=5, pady=5)

# View button
view_button = tk.Button(buttons_frame, text="View Passwords", command=view_passwords)
view_button.grid(row=0, column=1, padx=5, pady=5)

# Clear button
clear_button = tk.Button(buttons_frame, text="Clear Fields", command=clear_fields)
clear_button.grid(row=0, column=2, padx=5, pady=5)

# Bind Delete key to clear all fields
root.bind('<Delete>', clear_on_delete)

# Set focus to the first input field
username_entry.focus_set()

# Start the main loop
root.mainloop()
