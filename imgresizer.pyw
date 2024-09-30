import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES  # Importing TkinterDnD2
from PIL import Image
import os

# Function to resize the image, maintaining the aspect ratio
def resize_image(image_path, new_width):
    try:
        # Open the image
        image = Image.open(image_path)
        
        # Get original dimensions
        original_width, original_height = image.size
        
        # Calculate the new height maintaining the aspect ratio
        aspect_ratio = original_height / original_width
        new_height = int(new_width * aspect_ratio)
        
        # Resize the image
        resized_image = image.resize((new_width, new_height))
        
        # Construct the new file name with "_resized" and save it as a .jpg
        file_dir, file_name = os.path.split(image_path)
        file_name_without_ext, _ = os.path.splitext(file_name)
        new_file_name = f"{file_name_without_ext}_resized.jpg"
        save_path = os.path.join(file_dir, new_file_name)
        
        # Save the resized image as a JPG
        resized_image.convert("RGB").save(save_path, "JPEG", quality=95)
        #resized_image.save(save_path, "PNG", compress_level=8)
        #resized_image.save(save_path, "webp", quality=95)
        
        status_label.config(text=f"Image saved to {save_path} ({new_width}x{new_height})")
        status_label.update()  # Force immediate update to the UI
    except Exception as e:
        status_label.config(text=f"Error resizing image: {e}")

# Function to handle file drop event
def on_drop(event):
    file_path = event.data.strip('{}')  # Remove curly braces around file path if present
    status_label.config(text=f"File dropped: {file_path}")

    try:
        # Get the new width from the input field
        new_width = int(width_entry.get())
        
        # Resize the dropped image
        resize_image(file_path, new_width)
    except ValueError:
        status_label.config(text="Please enter a valid width.")

# GUI setup
root = TkinterDnD.Tk()  # Creating a TkinterDnD window
root.title("Drag & Drop Image Resizer")
root.geometry("500x350")

# Labels and entry fields for width (no height input)
tk.Label(root, text="Width:").pack(pady=5)
width_entry = tk.Entry(root)
width_entry.pack(pady=5)

# Drop area
drop_area = tk.Label(root, text="Drag & Drop an Image Here", bg="lightgrey", width=40, height=10)
drop_area.pack(pady=20)

# Bind the drop event to the drop area
drop_area.drop_target_register(DND_FILES)
drop_area.dnd_bind('<<Drop>>', on_drop)

# Status Label to display messages
status_label = tk.Label(root, text="")
status_label.pack(pady=10)  # Ensure this is correctly placed


root.mainloop()
