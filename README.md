# Real-Time Secure Face Recognition Attendance System Using Raspberry Pi

## 1. Project Overview

This project implements a real-time faculty attendance system using a Raspberry Pi 3B+ and a Logitech HD 720p USB webcam. The system utilizes lightweight ONNX models to process facial data at the edge, requiring no external cloud computing.

Recent updates have integrated a passive anti-spoofing model (MiniFAS), allowing the system to instantly distinguish between real faces and photographs or digital screens without requiring active head-turning challenges.

## 2. Hardware and Software Stack

### Hardware Requirements

* Processing board: Raspberry Pi 3B+
* Camera: Logitech HD 720p USB webcam
* Storage: microSD card (16GB minimum)
* Power: Stable 2.5A Raspberry Pi power supply

### Software and Models

* Python 3
* OpenCV (DNN module)
* Flask
* SQLite
* YuNet (Face Detection)
* SFace (Face Recognition / Feature Extraction)
* MiniFAS (Passive Anti-Spoofing)
* Scikit-learn (SVM Classifier)

## 3. Features

* Real-time face detection and recognition.
* Passive liveness detection to prevent spoofing with printed photos or phone screens.
* Automated attendance recording to a local SQLite database.
* Cooldown mechanism to prevent duplicate attendance entries.
* Web-based dashboard for faculty management and attendance viewing.
* Monthly attendance reports with CSV export capabilities.
* Configurable performance settings optimized for limited hardware (1GB RAM).

## 4. Purpose of the Raspberry Pi Module

The Raspberry Pi 3B+ is used as the embedded computing device that runs the attendance system at the physical attendance location.

The basic workflow is:

```text
Person
   │
   ▼
Logitech HD 720p Webcam
   │
   ▼
Raspberry Pi 3B+
   │
   ├── Capture image/video frame
   ├── Detect face
   ├── Generate/compare face features
   ├── Identify registered person
   └── Record attendance
   │
   ▼
Attendance Data
```

## 5. Project Structure

```text
frs_attendance/
├── app.py                     # Flask web dashboard and API
├── kiosk.py                   # Main recognition and attendance camera loop
├── enroll.py                  # Faculty registration and photo capture
├── preflight.py               # System and model verification check
├── lite_core.py               # Core database, camera, and pipeline logic
├── anti_spoof.py              # MiniFAS passive anti-spoofing logic
├── train_lite.py              # SVM classifier training script
├── requirements_lite.txt      # Python dependencies
├── models/                    # ONNX model directory
├── templates/                 # HTML templates for the Flask dashboard
├── known_faces/               # Captured reference photos (local only)
└── attendance.db              # SQLite database (auto-generated)
```

## 5. Installation and Setup

### 5.1 Clone the Repository

Download the project to the Raspberry Pi environment.

```bash
git clone <repository_url>
cd frs_attendance
```

### 5.2 Python Virtual Environment

Create and activate a virtual environment to isolate dependencies.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements_lite.txt
```

### 5.3 Verify ONNX Models

If the project was cloned from GitHub without Git LFS installed, the model files may be 133-byte text pointers instead of the actual binary files. Verify the file size of the SFace model.

```bash
ls -lh models/face_recognition_sface_2021dec.onnx
```

If the file size is in bytes rather than megabytes (approx 36.8 MB), download the raw model files directly.

```bash
wget -O models/face_recognition_sface_2021dec.onnx https://github.com/opencv/opencv_zoo/raw/main/models/face_recognition_sface/face_recognition_sface_2021dec.onnx
```

### 5.4 Run Preflight Checks

Ensure all cameras, models, and databases are correctly initialized.

```bash
python preflight.py
```

## 6. Usage Workflow

### Hardware

Connect the hardware as follows:

```text
                 ┌──────────────────────────┐
                 │     Logitech Webcam      │
                 │       HD 720p USB        │
                 └────────────┬─────────────┘
                              │ USB
                              ▼
                 ┌──────────────────────────┐
                 │     Raspberry Pi 3B+     │
                 │                          │
                 │ Face Recognition System  │
                 │ Attendance Processing    │
                 └────────────┬─────────────┘
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
               microSD Card         Network
```

#### Connection procedure

1. Insert the prepared microSD card into the Raspberry Pi.
2. Connect the Logitech webcam to a USB port.
3. Connect the Raspberry Pi to its power supply.
4. Connect a display if required.
5. Connect a keyboard and mouse for initial configuration.
6. Connect the Raspberry Pi to the required network.
7. Boot the Raspberry Pi.
8. Verify that the operating system starts correctly.
9. Verify that the webcam is detected.
10. Start the attendance application.

### Software

#### Step 1: Start the Dashboard

Run the Flask application to access the management interface.

```bash
python app.py
```

Access the dashboard via a web browser at `http://127.0.0.1:5000` (or the respective Raspberry Pi IP address).

#### Step 2: Enroll Faculty

Navigate to the Faculty Registration page on the dashboard to register a new user, or run the enrollment script directly.

```bash
python enroll.py
```

Follow the on-screen prompts to capture baseline images of the faculty member.

#### Step 3: Train the Classifier

After adding new faculty members, you must train the SVM classifier so the system can recognize them.

```bash
python train_lite.py
```

#### Step 4: Run the Attendance Kiosk

Start the main recognition loop. This is the interface that runs continuously to scan faces and record attendance.

```bash
python kiosk.py
```

## 7. Performance Optimization for Raspberry Pi 3B+

Because the Pi 3B+ has constrained processing power, running three concurrent neural networks (YuNet, MiniFAS, SFace) can introduce latency. You can override default variables at runtime to speed up the process.

To reduce the required frames for liveness and embedding analysis, start the kiosk using these environment variables.

```bash
ANTI_SPOOF_FRAMES=2 EMB_FRAMES=1 python kiosk.py
```

Additional configuration variables available in the code include:

* `DETECT_EVERY`: Skip face detection on some frames to save CPU cycles.
* `MIN_FACE_PX`: Ignore faces that are too far away.
* `COOLDOWN_SEC`: Time required before logging a checkout or duplicate scan.

## 8. Security Notes

* Do not commit the `known_faces/` directory or `attendance.db` to public version control.
* If deploying in a public location, restrict network access to the Flask dashboard to authorized administrative IP addresses.
* Regularly backup the `attendance.db` file to prevent data loss in the event of SD card failure.
