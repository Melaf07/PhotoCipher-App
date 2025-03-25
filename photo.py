import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import hashlib
from PIL import Image, ImageTk, UnidentifiedImageError
import sqlite3
import io

# Connect to the database
conn = sqlite3.connect('Gallery_User.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute("""CREATE TABLE IF NOT EXISTS photos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        Encrypted BLOB,
        Decrypted BLOB,
        Scrambled BLOB NULL
)
""")
conn.commit()

conn.commit()

# Function to insert photos into the database
def insert_photo(user_id, encrypted_path=None, decrypted_path=None, scrambled_path=None):
    encrypted_data = None
    if encrypted_path:
        with open(encrypted_path, 'rb') as enc_file:
            encrypted_data = enc_file.read()

    decrypted_data = None
    if decrypted_path:
        with open(decrypted_path, 'rb') as dec_file:
            decrypted_data = dec_file.read()

    scrambled_data = None
    if scrambled_path:
        with open(scrambled_path, 'rb') as scr_file:
            scrambled_data = scr_file.read()

    c.execute(
        "INSERT INTO photos (user_id, Encrypted, Decrypted, Scrambled) VALUES (?, ?, ?, ?)",
        (user_id, encrypted_data, decrypted_data, scrambled_data)
    )
    conn.commit()



# Function to retrieve photos from the database
def fetch_photos(user_id, filter_option):
    if filter_option == 'Encrypted':
        c.execute("SELECT Scrambled FROM photos WHERE user_id = ? AND Scrambled IS NOT NULL", (user_id,))
    elif filter_option == 'Decrypted':
        c.execute("SELECT Decrypted FROM photos WHERE user_id = ? AND Decrypted IS NOT NULL", (user_id,))
    else:  # All
        c.execute("SELECT Scrambled, Decrypted FROM photos WHERE user_id = ?", (user_id,))
    return c.fetchall()



def blob_to_image(blob_data):
    if blob_data is None:  # Check if blob_data is None
        messagebox.showerror("Error", "No image data available.")
        return None

    img_data = io.BytesIO(blob_data)
    try:
        img = Image.open(img_data)
        img = img.resize((150, 150), Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except UnidentifiedImageError:
        messagebox.showerror("Error", "Cannot identify the image file.")
        return None


PRIMARY_COLOR = "#6A0DAD"  # Purple
ACCENT_COLOR = "#FFCC00"   # Yellow
BACKGROUND_COLOR = "#EDE7F6"  # Light Lavender
TEXT_COLOR = "#4A148C"  # Dark Purple
BUTTON_TEXT_COLOR = "#FFFFFF"  # White

def photo_gallery_page(user_id):
    gallery_window = tk.Toplevel()
    gallery_window.configure(bg=BACKGROUND_COLOR)

    title_frame = tk.Frame(gallery_window, bg=BACKGROUND_COLOR)
    title_frame.grid(row=0, column=0, columnspan=3, padx=20, pady=(20, 10))  

    tk.Label(title_frame, text="Your Gallery", font=("Arial", 16), bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, columnspan=2, padx=0, pady=(0, 10))

    tk.Label(title_frame, text="Filter:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=1, column=0, padx=20, pady=(20, 10))
    photo_filter = ttk.Combobox(title_frame, values=['All', 'Encrypted', 'Decrypted'], state="readonly")
    photo_filter.set("All")
    photo_filter.grid(row=1, column=1, padx=20, pady=(20, 10))

    photo_frame = tk.Frame(gallery_window, bg=BACKGROUND_COLOR) 
    photo_frame.grid(row=1, column=0, columnspan=2, pady=(20, 20))  

    def update_photo_frame():
        for widget in photo_frame.winfo_children():
            widget.destroy()

        selected_option = photo_filter.get()
        photo_data_list = fetch_photos(user_id, selected_option)

        for photo_data in photo_data_list:
            if selected_option == 'Encrypted':
                blob_data = photo_data[0]
                if blob_data:  
                    photo = blob_to_image(blob_data)
                    if photo:
                        photo_label = tk.Label(photo_frame, image=photo, relief="solid", bg=BACKGROUND_COLOR)
                        photo_label.image = photo
                        photo_label.pack(side="left", padx=10, pady=10)

            elif selected_option == 'Decrypted':
                
                blob_data = photo_data[0]
                if blob_data:  
                    photo = blob_to_image(blob_data)
                    if photo:
                        photo_label = tk.Label(photo_frame, image=photo, relief="solid", bg=BACKGROUND_COLOR)
                        photo_label.image = photo
                        photo_label.pack(side="left", padx=10, pady=10)

            else:  # If "All" is selected
                scrambled_data, decrypted_data = photo_data

                if scrambled_data:
                    scrambled_photo = blob_to_image(scrambled_data)
                    if scrambled_photo:
                        scrambled_label = tk.Label(photo_frame, image=scrambled_photo, relief="solid", bg=BACKGROUND_COLOR)
                        scrambled_label.image = scrambled_photo
                        scrambled_label.pack(side="left", padx=10, pady=10)

                if decrypted_data:
                    decrypted_photo = blob_to_image(decrypted_data)
                    if decrypted_photo:
                        decrypted_label = tk.Label(photo_frame, image=decrypted_photo, relief="solid", bg=BACKGROUND_COLOR)
                        decrypted_label.image = decrypted_photo
                        decrypted_label.pack(side="left", padx=10, pady=10)

    update_photo_frame()  # Initial call to display all photos
    photo_filter.bind("<<ComboboxSelected>>", lambda e: update_photo_frame())  # Update on filter change