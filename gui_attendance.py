import face_recognition
import cv2
import os
from datetime import datetime, timedelta
import csv
import tkinter as tk
from tkinter import messagebox

# ----------------------------- Setup -----------------------------
path = 'images'
images = []
known_names = []

for filename in os.listdir(path):
    if filename.lower().endswith(('.png', '.jpg')):
        img = cv2.imread(os.path.join(path, filename))
        if img is not None:
            images.append(face_recognition.face_encodings(img)[0])
            known_names.append(os.path.splitext(filename)[0])

# ------------------------ Utility Functions ------------------------
def get_today_filename():
    return datetime.now().strftime("%Y-%m-%d") + ".csv"

def is_time_allowed():
    now = datetime.now()
    morning_start = now.replace(hour=9, minute=0, second=0, microsecond=0)
    morning_end = now.replace(hour=9, minute=30, second=0, microsecond=0)
    evening_start = now.replace(hour=16, minute=0, second=0, microsecond=0)
    evening_end = now.replace(hour=16, minute=20, second=0, microsecond=0)
    return morning_start <= now <= morning_end or evening_start <= now <= evening_end

def already_marked(name):
    filename = get_today_filename()
    if not os.path.exists(filename):
        return False
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row and row[0] == name:
                return True
    return False

def mark_attendance(name):
    filename = get_today_filename()
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        writer.writerow([name, now])

# --------------------------- GUI Setup ----------------------------
window = tk.Tk()
window.title("College Face Attendance")
window.geometry("400x200")
status_label = tk.Label(window, text="", font=("Arial", 14))
status_label.pack(pady=10)

# -------------------------- Attendance Logic --------------------------
def start_attendance():
    cap = cv2.VideoCapture(0)
    recognized = False

    if not cap.isOpened():
        messagebox.showerror("Error", "Camera not accessible")
        return

    ret, frame = cap.read()
    cap.release()

    if not ret:
        messagebox.showerror("Error", "Failed to capture image")
        return

    if not is_time_allowed():
        status_label.config(text="\u26D4 Not allowed at this time")
        messagebox.showinfo("Status", "\u26D4 Not allowed at this time")
        return

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(images, face_encoding)
        face_distances = face_recognition.face_distance(images, face_encoding)

        if True in matches:
            best_match_index = face_distances.argmin()
            name = known_names[best_match_index]

            if already_marked(name):
                status_label.config(text=f"⚠️ Already marked: {name}")
                messagebox.showinfo("Status", f"⚠️ Already marked: {name}")
            else:
                mark_attendance(name)
                status_label.config(text=f"✅ Marked: {name}")
                messagebox.showinfo("Status", f"✅ Attendance marked for {name}")
            recognized = True
            break

    if not recognized:
        status_label.config(text="❌ Face not recognized")
        messagebox.showinfo("Status", "❌ Face not recognized")

# ----------------------------- Buttons -----------------------------
tk.Button(window, text="Start Attendance", command=start_attendance, font=("Arial", 12)).pack(pady=10)
tk.Button(window, text="Exit", command=window.quit, font=("Arial", 12)).pack()

window.mainloop()
