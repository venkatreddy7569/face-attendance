import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import csv
import time

# Load known faces
path = 'images'
images = []
known_names = []

for filename in os.listdir(path):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        img = cv2.imread(os.path.join(path, filename))
        if img is not None:
            images.append(img)
            known_names.append(os.path.splitext(filename)[0])

def encode_faces(image_list):
    encoded = []
    for img in image_list:
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(rgb)
        if encodings:
            encoded.append(encodings[0])
    return encoded

known_encodings = encode_faces(images)

def is_allowed_time():
    now = datetime.now().time()
    morning = datetime.strptime("09:00", "%H:%M").time()
    morning_end = datetime.strptime("09:30", "%H:%M").time()
    evening = datetime.strptime("15:30", "%H:%M").time()
    evening_end = datetime.strptime("16:20", "%H:%M").time()
    return (morning <= now <= morning_end) or (evening <= now <= evening_end)

def last_attendance_time(name):
    if not os.path.exists('attendance.csv'):
        return None
    with open('attendance.csv', 'r') as f:
        for row in reversed(list(csv.reader(f))):
            if row[0] == name:
                return datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
    return None

# Start webcam
cap = cv2.VideoCapture(0)
print("[INFO] Face Attendance System started. Please look at the camera...")

attendance_action_taken = False
start_time = time.time()
MAX_DURATION = 60  # seconds

while True:
    ret, frame = cap.read()
    if not ret:
        print("[ERROR] Camera read failed.")
        break

    small = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

    faces = face_recognition.face_locations(rgb_small)
    encodings = face_recognition.face_encodings(rgb_small, faces)

    for loc, enc in zip(faces, encodings):
        matches = face_recognition.compare_faces(known_encodings, enc)
        distances = face_recognition.face_distance(known_encodings, enc)
        best_match = np.argmin(distances)

        if matches[best_match]:
            name = known_names[best_match]
            now = datetime.now()

            if is_allowed_time():
                last_time = last_attendance_time(name)
                if not last_time or (now - last_time).total_seconds() > 6 * 3600:
                    with open('attendance.csv', 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([name, now.strftime("%Y-%m-%d %H:%M:%S")])
                    print(f"[✅] Attendance marked for: {name} at {now.strftime('%H:%M:%S')}")
                else:
                    print(f"[ℹ️] {name} already marked. Try after 6 hours.")
            else:
                print(f"[⛔] Attendance not allowed now. Come during allowed time.")

            attendance_action_taken = True
            break  # Stop after one detection

    cv2.imshow("Face Attendance", frame)
    if cv2.waitKey(1) & 0xFF == ord('q') or attendance_action_taken:
        break
    if time.time() - start_time > MAX_DURATION:
        print("[⏳] No face detected. Exiting after 60 seconds.")
        break

cap.release()
cv2.destroyAllWindows()
