📸 Face Recognition Attendance System
        A Python-based attendance system that uses face recognition to mark student attendance. It captures faces in real-time using OpenCV and logs attendance only during defined time slots (e.g., morning 9–9:30 AM, evening till 4:20 PM). Built with a GUI for easy usage in educational institutions like colleges.

    ✅ Features
        🔍 Real-time face detection and recognition using webcam

        🧠 Built using face_recognition, OpenCV, Tkinter

        ⏰ Time-based attendance (e.g., 9–9:30 AM and after 6 hours minimum)

        📁 Attendance logged into a .csv file

        🖼️ Automatically loads known faces from images/ folder

        🖥️ Simple GUI with Start button

        🛑 Automatically exits after marking or skipping attendance

        🧠 Prevents duplicate attendance within time window


    '''
    face-attendance/
│
├── images/                # Folder with known face images
├── attendance.csv         # Log file for storing attendance data
├── main.py                # Backend logic (Face recognition + logging)
├── gui_attendance.py      # GUI interface for launching attendance
└── README.md              # Project documentation
    '''

🛠️ Tech Stack
        Python 3.12+

        OpenCV

        face_recognition

        NumPy, Pandas

        Tkinter (for GUI)
⚙️ How It Works
        Load known face encodings from the images/ folder

        Open webcam and detect face using face_recognition

        Compare with known encodings

        If matched, check if attendance can be marked (based on time logic)

        Log name and time to attendance.csv

        GUI allows the user to start process with a single button click

🏫 Use Case
        Designed for college classroom or lab attendance. Only allows valid entries during:

        🕘 Morning Slot: 9:00 AM – 9:30 AM

        🕓 Evening Slot: After 6-hour gap, till 4:20 PM
💡 Future Improvements
        Add admin login for attendance control

        Generate PDF reports

        Auto email or WhatsApp notifications

        Integrate database for persistent storage

