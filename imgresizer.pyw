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
        
        # Construct the new file name based on the selected format
        file_dir, file_name = os.path.split(image_path)
        file_name_without_ext, _ = os.path.splitext(file_name)

        # Get the selected file format from radio buttons
        selected_format = file_format.get()
        
        if selected_format == "JPG":
            new_file_name = f"{file_name_without_ext}_resized_{new_width}.jpg"
            save_path = os.path.join(file_dir, new_file_name)
            resized_image.convert("RGB").save(save_path, "JPEG", quality=95)

        elif selected_format == "PNG":
            new_file_name = f"{file_name_without_ext}_resized_{new_width}.png"
            save_path = os.path.join(file_dir, new_file_name)
            resized_image.save(save_path, "PNG", compress_level=5)

        elif selected_format == "WebP":
            new_file_name = f"{file_name_without_ext}_resized_{new_width}.webp"
            save_path = os.path.join(file_dir, new_file_name)
            resized_image.convert("RGB").save(save_path, "WebP", quality=95)
        
        status_label.config(text=f"Image saved: \n{new_file_name} ({new_width}x{new_height})")
        status_label.update()
        
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
root.geometry("288x430")

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

# Add a StringVar to hold the selected file format
file_format = tk.StringVar(value="JPG")  # Default to JPG

# Add radio buttons for format selection
tk.Label(root, text="Select format:").pack(pady=5)
tk.Radiobutton(root, text="JPG", variable=file_format, value="JPG").pack(padx=30,side='left')
tk.Radiobutton(root, text="PNG", variable=file_format, value="PNG").pack(padx=10,side='left')
tk.Radiobutton(root, text="WebP", variable=file_format, value="WebP").pack(padx=10,side='left')

root.mainloop()
