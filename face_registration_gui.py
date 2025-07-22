import cv2
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Folder where faces will be saved
SAVE_FOLDER = "known_faces"

# Create folder if not exists
os.makedirs(SAVE_FOLDER, exist_ok=True)

# Initialize camera
cap = cv2.VideoCapture(0)

# Function to capture and save image
def capture_image():
    name = name_entry.get().strip()
    if not name:
        messagebox.showwarning("Input Error", "Please enter a name first.")
        return
    
    ret, frame = cap.read()
    if ret:
        person_folder = os.path.join(SAVE_FOLDER, name)
        os.makedirs(person_folder, exist_ok=True)
        img_count = len(os.listdir(person_folder)) + 1
        img_path = os.path.join(person_folder, f"{img_count}.jpg")
        cv2.imwrite(img_path, frame)
        messagebox.showinfo("Image Captured", f"Saved as {img_path}")
    else:
        messagebox.showerror("Capture Failed", "Failed to capture image from webcam.")

# Update webcam feed in GUI
def update_frame():
    ret, frame = cap.read()
    if ret:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
    video_label.after(10, update_frame)

# Close application safely
def on_closing():
    cap.release()
    root.destroy()

# GUI Setup
root = tk.Tk()
root.title("Face Registration App")

tk.Label(root, text="Enter Name:").pack(pady=5)
name_entry = tk.Entry(root)
name_entry.pack(pady=5)

capture_button = tk.Button(root, text="Capture Image", command=capture_image)
capture_button.pack(pady=10)

video_label = tk.Label(root)
video_label.pack()

update_frame()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
