import os
import subprocess
import pyttsx3

# Initialize Text-to-Speech
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Voice Prompt
speak("Welcome! Please choose. Mark attendance or register yourself.")


def main_menu():
    while True:
        print("\n====== Smart Attendance System ======")
        print("1. Mark Attendance")
        print("2. Register New Face")
        print("3. Exit")

        choice = input("\nEnter your choice (1/2/3): ")

        if choice == '1':
            print("[INFO] Starting Attendance System...")
            subprocess.run(["python", "face_recognition_attendance.py"])

        elif choice == '2':
            print("[INFO] Starting Face Registration...")
            subprocess.run(["python", "face_registration_gui.py"])

        elif choice == '3':
            print("Exiting... Goodbye!")
            break

        else:
            print("Invalid input. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    main_menu()
