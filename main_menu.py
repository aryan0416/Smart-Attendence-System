import tkinter as tk
import subprocess
import os
from datetime import datetime
from tkinter import messagebox
from PIL import Image, ImageTk
import pyttsx3

# Initialize Text-to-Speech
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Paths to scripts
REGISTER_SCRIPT = 'face_registration_gui.py'
ATTENDANCE_SCRIPT = 'face_recognition_attendance.py'

attendance_process = None  # Track attendance process

# Functions
def register_face():
    speak("Opening face registration.")
    subprocess.Popen(['python', REGISTER_SCRIPT])

def mark_attendance():
    global attendance_process
    if attendance_process is None or attendance_process.poll() is not None:
        speak("Starting attendance marking.")
        attendance_process = subprocess.Popen(['python', ATTENDANCE_SCRIPT])
    else:
        speak("Attendance marking is already running.")
        messagebox.showinfo("Info", "Attendance marking is already running.")

def view_report():
    today_date = datetime.now().strftime("%Y-%m-%d")
    report_folder = os.path.join('Attendance_Reports', today_date)
    csv_file = os.path.join(report_folder, 'Attendance.csv')
    if os.path.exists(csv_file):
        speak("Opening today's attendance report.")
        os.startfile(csv_file)
    else:
        speak("No report found for today.")
        messagebox.showinfo("No Report Found", "Attendance hasn't been marked today.")

def close_app():
    global attendance_process
    speak("Closing application.")
    if attendance_process and attendance_process.poll() is None:
        attendance_process.terminate()
        speak("Attendance process terminated.")
    root.destroy()

def on_enter(e):
    e.widget.config(bg='#45A049')

def on_leave(e):
    e.widget.config(bg='#4CAF50')

def on_close_enter(e):
    e.widget.config(bg='#FF3B3B')

def on_close_leave(e):
    e.widget.config(bg='#FF5C5C')

# GUI Setup
root = tk.Tk()
root.title("Smart Attendance Dashboard")
root.geometry("600x500")
root.resizable(False, False)

# Load Background Image
bg_image = Image.open("background.jpg")
bg_image = bg_image.resize((600, 500))
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

overlay = tk.Frame(root, bg='#000000')
overlay.place(relwidth=1, relheight=1)

tk.Label(overlay, text="Smart Attendance System", font=('Helvetica', 20, 'bold'),
         bg="#000000", fg="white").pack(pady=30)

button_style = {
    'font': ('Helvetica', 14),
    'bg': '#4CAF50',
    'fg': 'white',
    'activebackground': '#45A049',
    'relief': 'flat',
    'width': 30,
    'height': 2
}

buttons = [
    ("➕  Register New Face", register_face),
    ("✅  Mark Attendance", mark_attendance),
    ("📊  View Today's Report", view_report)
]

for text, command in buttons:
    btn = tk.Button(overlay, text=text, command=command, **button_style)
    btn.pack(pady=10)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

close_btn = tk.Button(overlay, text="❌  Close Application", command=close_app,
                      font=('Helvetica', 14),
                      bg="#FF5C5C", fg='white',
                      activebackground="#FF3B3B",
                      relief='flat',
                      width=30, height=2)
close_btn.pack(pady=20)
close_btn.bind("<Enter>", on_close_enter)
close_btn.bind("<Leave>", on_close_leave)

tk.Label(overlay, text="© Smart Attendance System", font=('Arial', 10),
         bg="#000000", fg="#AAAAAA").pack(side='bottom', pady=10)

root.mainloop()
