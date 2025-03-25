import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk, UnidentifiedImageError
import os
from encrypt import enc_image,dec_image 
from photo import photo_gallery_page , insert_photo
from tkinter.filedialog import askopenfilename
 #upload windows
def open_upload_window(user_id):
    window = tk.Toplevel()  
    WWIDTH, WHEIGHT = 800, 600
    CWIDTH, CHEIGHT = 400, 300
    window.title('PhotoCipher app')
    window.geometry('%sx%s' % (WWIDTH, WHEIGHT))

    PRIMARY_COLOR = "#6A0DAD"  # Purple
    ACCENT_COLOR = "#FFCC00"   # Yellow
    BACKGROUND_COLOR = "#EDE7F6"  # Light Lavender
    TEXT_COLOR = "#4A148C"  # Dark Purple
    BUTTON_TEXT_COLOR = "#FFFFFF"  # White

    window.configure(bg=BACKGROUND_COLOR)

    canva = tk.Canvas(window, width=CWIDTH, height=CHEIGHT, bg='white')
    canva.pack()

    image_path = None 

    def uploadfun():
        nonlocal image_path 
        try:
            image_path = askopenfilename(
                filetypes=[
                   ("Image Files", "*.jpg *.png *.jpeg "),
                  ("Encrypted Files", "*.enc"),
                    ("All Files", "*.*")
                ]
            )
            if image_path:
                print(f"Selected file: {image_path}")
            else:
                print("No file selected")   
#resize the image
            if image_path:  
                image = Image.open(image_path)
                image.show() 
                imgw, imgh = image.size
                if imgw > CWIDTH or imgh > CHEIGHT:
                    while imgw > CWIDTH or imgh > CHEIGHT:
                        imgw *= 0.99
                        imgh *= 0.99
                    image = image.resize((int(imgw), int(imgh)))
                    messagebox.showinfo(title='Warning', message='Image will be resized.')
                
                img = ImageTk.PhotoImage(image)
                canva.img = img
                canva.create_image(CWIDTH/2, CHEIGHT/2, image=img, anchor=tk.CENTER)
        except UnidentifiedImageError:
            messagebox.showinfo(title='Upload Error', message='Image could not be read')

    def validate_key(key):
        # Check if the key length is either 16, 24, or 32 characters
        if len(key) not in [16, 24, 32]:
            return False
        return True
 
    def encryptfun():
        if image_path:
            encryptwindow = Toplevel()  
            encryptwindow.geometry("400x300")
            encryptwindow.title('Encryption Page')
            encryptwindow.configure(bg=BACKGROUND_COLOR) 
            
            tk.Label(encryptwindow, text="Enter a key", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=2, column=0, padx=10, pady=(10, 0), sticky='w')
            key1 = tk.Entry(encryptwindow, show="*")
            key1.grid(row=2, column=1, padx=10, pady=(10, 10))

            def encrypt_action():
                key = key1.get() 
                if not validate_key(key):
                    messagebox.showerror(title="Error", message="Key must be 16, 24, or 32 characters long!")
                    return   

                encrypted_image_path, scrambled_img_path = enc_image(image_path, key, os.getcwd())
                encryptwindow.destroy()  
                messagebox.showinfo(title="Success", message="Image encrypted successfully!")

                scrambled_img = Image.open(scrambled_img_path)
                scrambled_img.thumbnail((400, 300))  # Resize to fit in your canvas
                scrambled_image_display = ImageTk.PhotoImage(scrambled_img)

                canva.delete("all")  
                canva.img = scrambled_image_display 
                canva.create_image(CWIDTH/2, CHEIGHT/2, image=scrambled_image_display, anchor=tk.CENTER)

                insert_photo(user_id, scrambled_path=scrambled_img_path)

            b1 = tk.Button(encryptwindow, text='Encrypt', command=encrypt_action, fg=TEXT_COLOR, activebackground=ACCENT_COLOR, activeforeground=BUTTON_TEXT_COLOR)
            b1.grid(row=4, column=1, padx=10, pady=(10, 20))

    def decrypt():
        if image_path:
            encryptwindow = Toplevel()  
            encryptwindow.geometry("400x300")
            encryptwindow.title('Decryption Page')
            encryptwindow.configure(bg=BACKGROUND_COLOR) 

            tk.Label(encryptwindow, text="Enter a key", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=2, column=0, padx=10, pady=(10, 0), sticky='w')
            key1 = tk.Entry(encryptwindow, show="*")
            key1.grid(row=2, column=1, padx=10, pady=(10, 10))

            def decrypt_action():
                key = key1.get()
                if not validate_key(key):
                    messagebox.showerror(title="Error", message="Key must be 16, 24, or 32 characters long!")
                    return   
    
                decrypted_image_path = dec_image(image_path, key, os.getcwd())
                try:
                    img = Image.open(decrypted_image_path)
                    img.thumbnail((400, 300))  # Resize to fit in your canvas
                    decrypted_image_display = ImageTk.PhotoImage(img)

                    canva.delete("all")  
                    canva.img = decrypted_image_display  
                    canva.create_image(CWIDTH/2, CHEIGHT/2, image=decrypted_image_display, anchor=tk.CENTER)
        
                    messagebox.showinfo(title="Success", message="Image decrypted successfully!")
                    encryptwindow.destroy()  

                    insert_photo(user_id, image_path, decrypted_image_path)
                except Exception as e:
                     messagebox.showerror(title="Error", message=f"Failed to load decrypted image: {str(e)}")

            b1 = tk.Button(encryptwindow, text='Decrypt', command=decrypt_action, fg=TEXT_COLOR, activebackground=ACCENT_COLOR, activeforeground=BUTTON_TEXT_COLOR)
            b1.grid(row=4, column=1, padx=10, pady=(10, 20))

    b1 = tk.Button(window, text='Upload', command=uploadfun, width=20, font=("Arial", 14), padx=10, pady=10,  fg=TEXT_COLOR, activebackground=ACCENT_COLOR, activeforeground=BUTTON_TEXT_COLOR)
    b1.pack(pady=5)

    b2 = tk.Button(window, text='Encrypt', command=encryptfun, width=20, font=("Arial", 14), padx=10, pady=10, fg=TEXT_COLOR, activebackground=ACCENT_COLOR, activeforeground=BUTTON_TEXT_COLOR)
    b2.pack(side=tk.RIGHT, padx=20)

    b3 = tk.Button(window, text='Decrypt', command=decrypt, width=20, font=("Arial", 14), padx=10, pady=10, fg=TEXT_COLOR, activebackground=ACCENT_COLOR, activeforeground=BUTTON_TEXT_COLOR)
    b3.pack(side=tk.LEFT, padx=20)

    def open_gallery():
        photo_gallery_page(user_id)  # Pass the user_id to the gallery function

    b4 = tk.Button(window, text='Image gallery', command=open_gallery, width=20, font=("Arial", 14), padx=10, pady=10, fg=TEXT_COLOR, activebackground=ACCENT_COLOR, activeforeground=BUTTON_TEXT_COLOR)
    b4.pack(side=tk.LEFT, padx=1)

    window.mainloop()