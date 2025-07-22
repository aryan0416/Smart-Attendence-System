import cv2
import os
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import shutil

SAVE_FOLDER = "known_faces"
os.makedirs(SAVE_FOLDER, exist_ok=True)

cap = cv2.VideoCapture(0)

# Capture Image and Save
def capture_image():
    name = name_entry.get().strip()
    if not name:
        messagebox.showwarning("Input Error", "Please enter a name.")
        return
    ret, frame = cap.read()
    if ret:
        person_folder = os.path.join(SAVE_FOLDER, name)
        os.makedirs(person_folder, exist_ok=True)
        img_count = len(os.listdir(person_folder)) + 1
        img_path = os.path.join(person_folder, f"{img_count}.jpg")
        cv2.imwrite(img_path, frame)
        messagebox.showinfo("Saved", f"Image saved as {img_path}")

# Delete Entire Folder (Person)
def delete_person():
    name = name_entry.get().strip()
    if not name:
        messagebox.showwarning("Input Error", "Enter the person's name to delete.")
        return
    person_folder = os.path.join(SAVE_FOLDER, name)
    if os.path.exists(person_folder):
        shutil.rmtree(person_folder)
        messagebox.showinfo("Deleted", f"{name} deleted.")
    else:
        messagebox.showerror("Not Found", "Person not found.")

# Import Images from Disk
def import_images():
    name = name_entry.get().strip()
    if not name:
        messagebox.showwarning("Input Error", "Please enter a name.")
        return
    file_paths = filedialog.askopenfilenames(title="Select Images", filetypes=[("Images", "*.jpg *.jpeg *.png")])
    if file_paths:
        person_folder = os.path.join(SAVE_FOLDER, name)
        os.makedirs(person_folder, exist_ok=True)
        img_count = len(os.listdir(person_folder))
        for path in file_paths:
            img_count += 1
            dest_path = os.path.join(person_folder, f"{img_count}.jpg")
            shutil.copy(path, dest_path)
        messagebox.showinfo("Imported", f"Imported {len(file_paths)} images.")

# Webcam Feed
def update_frame():
    ret, frame = cap.read()
    if ret:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
    video_label.after(10, update_frame)

def on_closing():
    cap.release()
    root.destroy()

# GUI Setup
root = tk.Tk()
root.title("Face Re-Registration GUI")

tk.Label(root, text="Enter Name:").pack(pady=5)
name_entry = tk.Entry(root)
name_entry.pack(pady=5)

capture_button = tk.Button(root, text="Capture Image from Webcam", command=capture_image)
capture_button.pack(pady=5)

import_button = tk.Button(root, text="Import Images from Files", command=import_images)
import_button.pack(pady=5)

delete_button = tk.Button(root, text="Delete Person", fg="red", command=delete_person)
delete_button.pack(pady=5)

video_label = tk.Label(root)
video_label.pack()

update_frame()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
