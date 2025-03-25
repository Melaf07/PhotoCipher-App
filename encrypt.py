from PIL import Image
import numpy as np
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def enc_image(image_path, key, output_folder="encrypted_images"):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    with open(image_path, "rb") as f:
        data = f.read()
    
    iv = os.urandom(16)
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))

    encrypted_file_path = os.path.join(output_folder, "encrypted_image.enc")
    with open(encrypted_file_path, "wb") as f:
        f.write(iv + encrypted_data)

    img = Image.open(image_path)
    img_data = np.array(img)

    # Flatten encrypted data and repeat or pad to fit the image size
    required_size = img_data.size
    encrypted_data = np.frombuffer(encrypted_data, dtype=np.uint8)

    if len(encrypted_data) < required_size:
        encrypted_data = np.resize(encrypted_data, required_size)
    else:
        encrypted_data = encrypted_data[:required_size]

    # Reshape the encrypted data to match the image dimensions
    scrambled_img_data = encrypted_data.reshape(img_data.shape)

    # Create and save the scrambled image
    scrambled_img = Image.fromarray(scrambled_img_data)
    scrambled_img_path = os.path.join(output_folder, "scrambled_image.png")
    scrambled_img.save(scrambled_img_path)

    return encrypted_file_path, scrambled_img_path


def dec_image(encrypted_path, key, output_folder="decrypted_images"):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    try:
        with open(encrypted_path, "rb") as f:
            iv = f.read(16)
            encrypted_data = f.read()
    
        cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    
        # Save the decrypted image
        decrypted_file_path = os.path.join(output_folder, "decrypted_image.png")
        with open(decrypted_file_path, "wb") as f:
            f.write(decrypted_data)
    
        return decrypted_file_path

    except Exception as e:
        raise Exception(f"Decryption failed: {str(e)}")