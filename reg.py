import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import hashlib
from PIL import Image, ImageTk
from upload import open_upload_window  # Import the upload function
import sqlite3

#database connection
conn = sqlite3.connect('user_info.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (
                username TEXT,
                email TEXT,
                date_of_birth TEXT,
                password INT)''')
conn.commit()
conn.close()

# Function to hash passwords for better security
def hash_password(password):
    encode_password = password.encode()
    return hashlib.sha256(encode_password).hexdigest()

#clear fields on the registration interface
def clear_fields():
    username_field.delete(0, tk.END)
    email_field.delete(0, tk.END)
    day_combo.set('Day')
    month_combo.set('Month')
    year_combo.set('Year')
    password_field.delete(0, tk.END)
    confirmPassw_field.delete(0, tk.END)

# Registration page
def Register_page():
    conn = sqlite3.connect('user_info.db')
    c = conn.cursor()
    # Fetching user input
    username = username_field.get()
    email = email_field.get()
    password = password_field.get()
    confirm_password = confirmPassw_field.get()
    day = day_combo.get()
    month = month_combo.get()
    year = year_combo.get()

    # Check for empty fields
    if not username or not email or not password or not confirm_password or day == "Day" or month == "Month" or year == "Year":
        messagebox.showerror("Error", "All fields must be filled!")
        conn.close()
        return
    
    # Check if username already exists
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    existing_user = c.fetchone()
    if existing_user:
        messagebox.showerror("Error", "Username already exists!")
        conn.close()
        return
    
    # Check if passwords match
    if password != confirm_password:
        messagebox.showerror("Error", "Passwords don't match!") 
        conn.close()
        return
    
    # Insert user data
    c.execute("INSERT INTO users VALUES (:username, :email, :date_of_birth, :password)", {
        'username': username,
        'email': email,
        'date_of_birth': f"{day}/{month}/{year}",
        'password': hash_password(password)
    })
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Registration successful!")
    open_upload_window(logged_in_user_id)
    clear_fields()

# Login logic
logged_in_user_id = None

def login_page():
    global logged_in_user_id
    username = login_username_field.get()
    password = hash_password(login_password_field.get()) 
    conn = sqlite3.connect('user_info.db')
    c = conn.cursor()
    c.execute("SELECT rowid, * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    conn.close()

    if user:
        logged_in_user_id = user[0]  # Store the user's rowid (assumed to be unique for each user)
        messagebox.showinfo("Success", "Login successful!")
        clear_fields()
        open_upload_window(logged_in_user_id)  # Pass logged_in_user_id to the upload window

    else:
        messagebox.showerror("Error", "Incorrect username or password!")
    

# Frame switch functions
def switch_to_login():
    registeration_frame.grid_remove()
    encrypt_decrypt_app_frame.grid_remove()
    login_frame.grid(row=0, column=0, padx=10, pady=10)

def switch_to_register():
    login_frame.grid_remove()
    encrypt_decrypt_app_frame.grid_remove()
    registeration_frame.grid(row=0, column=0, padx=10, pady=10)


PRIMARY_COLOR = "#6A0DAD"  # Purple
ACCENT_COLOR = "#FFCC00"   # Yellow
BACKGROUND_COLOR = "#EDE7F6"  # Light Lavender
TEXT_COLOR = "#4A148C"  # Dark Purple
BUTTON_TEXT_COLOR = "#FFFFFF"  # White

# The main window
encrypt_decrypt_app = tk.Tk()
encrypt_decrypt_app.title("PhotoCipher App")
encrypt_decrypt_app.configure(bg=BACKGROUND_COLOR)

# Welcome Frame
encrypt_decrypt_app_frame = tk.Frame(encrypt_decrypt_app)
encrypt_decrypt_app_frame.configure(bg=BACKGROUND_COLOR)
tk.Label(encrypt_decrypt_app_frame, text="Welcome to PhotoCipher Application !", font=("Arial", 20), bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, columnspan=4, pady=(0, 10))
tk.Button(encrypt_decrypt_app_frame, text="Register",fg=PRIMARY_COLOR, activebackground=ACCENT_COLOR, activeforeground=BUTTON_TEXT_COLOR, command=switch_to_register).grid(row=1, column=0, columnspan=2, pady=(20, 20))
tk.Button(encrypt_decrypt_app_frame, text="Login", fg=PRIMARY_COLOR, activebackground=ACCENT_COLOR, activeforeground=BUTTON_TEXT_COLOR, command=switch_to_login).grid(row=1, column=2, columnspan=2, pady=(20, 20))

# Pack the welcome frame first
encrypt_decrypt_app_frame.grid(row=0, column=0, padx=10, pady=10)

# Registration interface
registeration_frame = tk.Frame(encrypt_decrypt_app)
registeration_frame.configure(bg=BACKGROUND_COLOR)

tk.Label(registeration_frame, text="Create Account", font=("Arial", 16), bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, columnspan=4, pady=(0, 10))

tk.Label(registeration_frame, text="Username:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=1, column=0, padx=10, pady=(10, 0), sticky='w')
username_field = tk.Entry(registeration_frame)
username_field.grid(row=1, column=1, padx=10, pady=(10, 10))

tk.Label(registeration_frame, text="Email:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=2, column=0, padx=10, pady=(10, 0), sticky='w')
email_field = tk.Entry(registeration_frame)
email_field.grid(row=2, column=1, padx=10, pady=(10, 10))

tk.Label(registeration_frame, text="Date of Birth:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=3, column=0, padx=10, pady=(10, 0), sticky='w')
dob_frame = tk.Frame(registeration_frame)
dob_frame.grid(row=3, column=1, columnspan=3, padx=10, pady=(10, 0), sticky="w")

day_combo = ttk.Combobox(dob_frame, values=list(range(1, 32)), state="readonly", width=5)
day_combo.set("Day")
day_combo.grid(row=0, column=0, padx=5)
month_combo = ttk.Combobox(dob_frame, values=list(range(1, 13)), state="readonly", width=7)
month_combo.set("Month")
month_combo.grid(row=0, column=1, padx=5)

year_combo = ttk.Combobox(dob_frame, values=list(range(1900, 2025)), state="readonly", width=5)
year_combo.set("Year")
year_combo.grid(row=0, column=2, padx=5)

tk.Label(registeration_frame, text="Password:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=4, column=0, padx=10, pady=(10, 0), sticky='w')
password_field = tk.Entry(registeration_frame, show="*")  # * For security purpose
password_field.grid(row=4, column=1, padx=10, pady=(10, 10))

tk.Label(registeration_frame, text="Confirm Password:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=5, column=0, padx=10, pady=(10, 0), sticky='w')
confirmPassw_field = tk.Entry(registeration_frame, show="*")
confirmPassw_field.grid(row=5, column=1, padx=10, pady=(10, 10))

tk.Button(registeration_frame, text="Register", fg=TEXT_COLOR, activebackground=ACCENT_COLOR, activeforeground=BUTTON_TEXT_COLOR, command=Register_page).grid(row=6, column=0, columnspan=4, pady=(10, 10))
tk.Button(registeration_frame, text="Already have an account?", fg=TEXT_COLOR, activebackground=ACCENT_COLOR, activeforeground=BUTTON_TEXT_COLOR, command=switch_to_login).grid(row=7, column=0, columnspan=4, pady=(10, 10))

# Login interface
login_frame = tk.Frame(encrypt_decrypt_app)
login_frame.configure(bg=BACKGROUND_COLOR)

tk.Label(login_frame, text="Login", font=("Arial", 16), bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, columnspan=2, pady=(0, 10))

tk.Label(login_frame, text="Username:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=1, column=0, padx=10, pady=(10, 0), sticky='w')
login_username_field = tk.Entry(login_frame)
login_username_field.grid(row=1, column=1, padx=10, pady=(10, 10))

tk.Label(login_frame, text="Password:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=2, column=0, padx=10, pady=(10, 0), sticky='w')
login_password_field = tk.Entry(login_frame, show="*")
login_password_field.grid(row=2, column=1, padx=10, pady=(10, 10))

tk.Button(login_frame, text="Login",fg=PRIMARY_COLOR, activebackground=ACCENT_COLOR, activeforeground=BUTTON_TEXT_COLOR, command=login_page).grid(row=3, column=0, columnspan=2, pady=(10, 10))
tk.Button(login_frame, text="Don't have an account?", fg=PRIMARY_COLOR, activebackground=ACCENT_COLOR, activeforeground=BUTTON_TEXT_COLOR, command=switch_to_register).grid(row=4, column=0, columnspan=2, pady=(10, 10))

encrypt_decrypt_app.mainloop()