import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import pyttsx3

# Initialize Text-to-Speech
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Load images from known_faces subfolders
def load_images_from_subfolders(path):
    images = []
    classNames = []
    print("[INFO] Loading images...")

    for person_name in os.listdir(path):
        person_folder = os.path.join(path, person_name)
        if os.path.isdir(person_folder):
            for image_name in os.listdir(person_folder):
                image_path = os.path.join(person_folder, image_name)
                img = cv2.imread(image_path)
                if img is not None:
                    images.append(img)
                    classNames.append(person_name)
                else:
                    print(f"[WARN] Couldn't load {image_path}")

    print(f"[INFO] Loaded {len(images)} images for {len(set(classNames))} people.")
    return images, classNames

# Encoding function
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodes = face_recognition.face_encodings(img)
        if encodes:
            encodeList.append(encodes[0])
    return encodeList

# Create Daily Folder for Attendance Reports
today_date = datetime.now().strftime("%Y-%m-%d")
folder_path = os.path.join('Attendance_Reports', today_date)
os.makedirs(folder_path, exist_ok=True)

# CSV Log File Path
csv_file = os.path.join(folder_path, 'Attendance.csv')
if not os.path.exists(csv_file):
    with open(csv_file, "w") as f:
        f.write("Name,Time\n")

# Load known faces
path = 'known_faces'
images, classNames = load_images_from_subfolders(path)
encodeListKnown = findEncodings(images)
print('[INFO] Encoding Complete')

# Initialize webcam and attendance tracker
cap = cv2.VideoCapture(0)
attendance_marked = set()

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0,0), fx=0.25, fy=0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()

            if name not in attendance_marked:
                attendance_marked.add(name)
                now = datetime.now().strftime("%H:%M:%S")
                with open(csv_file, "a") as f:
                    f.write(f"{name},{now}\n")
                print(f"[INFO] Attendance marked for {name} at {now}")
                speak(f"Attendance marked for {name}")

            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
