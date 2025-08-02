# Face Attendance System

This project is a Python-based Face Attendance System that uses face recognition to automatically mark attendance. The system allows real-time recognition using a webcam and stores the attendance records in an Excel sheet.

## 📌 Features

- Face detection and recognition using OpenCV
- Graphical User Interface (GUI) for ease of use
- Attendance records saved to Excel file
- Option to collect face images and use them for training
- Time-based attendance validation (e.g., morning and evening sessions)

## 🧠 Technologies Used

- Python 3.x
- OpenCV
- SQLite (optional)
- Pandas (for Excel file management)
- Tkinter (for GUI)
- face_recognition library


## 📁 Project Structure

face-attendance/
├── .git/ # Git repository folder
├── images/ # Collected face images
├── attendance.xlsx # Attendance record file
├── gui_attendance.py # GUI implementation
├── main.py # Main execution logic
├── README.md # Project description


## 🚀 How to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/venkatreddy7569/face-attendance.git

# file path
cd face-attendance

# install dependencies
pip install -r requirements.txt

# Output command
python main.py

# 📸 How It Works

Collect face images and save them in the images/ folder.

When the program runs, it compares detected faces against stored faces.

If a match is found, it marks attendance in attendance.xlsx.

# 👨‍💻 Author
Venkat Reddy
GitHub: venkatreddy7569

# 📃 License
This project is for learning and personal use. Feel free to modify or build upon it!
