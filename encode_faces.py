import os
import cv2
import face_recognition
import pickle

def generate_encodings(known_faces_dir="known_faces", encodings_file="encodings.pickle"):
    known_encodings = []
    known_names = []

    for name in os.listdir(known_faces_dir):
        person_folder = os.path.join(known_faces_dir, name)
        if not os.path.isdir(person_folder):
            continue

        for filename in os.listdir(person_folder):
            img_path = os.path.join(person_folder, filename)
            image = cv2.imread(img_path)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            boxes = face_recognition.face_locations(rgb, model='hog')
            encodings = face_recognition.face_encodings(rgb, boxes)

            for encoding in encodings:
                known_encodings.append(encoding)
                known_names.append(name)

    data = {"encodings": known_encodings, "names": known_names}
    with open(encodings_file, "wb") as f:
        pickle.dump(data, f)

    print(f"[INFO] Encodings updated and saved to {encodings_file}")
