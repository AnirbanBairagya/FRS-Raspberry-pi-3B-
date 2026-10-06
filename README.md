# Face Recognition Attendance System using Raspberry Pi 3B+

## Overview

This part of the project is the **Raspberry Pi 3B+ hardware module** for the Face Recognition Attendance System.

The Raspberry Pi operates as the on-site attendance unit. It connects to a **Logitech HD 720p USB webcam**, captures faces, performs face recognition using the configured recognition system, and records attendance according to the project's software configuration.

This README covers **only the Raspberry Pi 3B+ module**.

It does **not** describe laptop-side development, laptop execution, development environments, or laptop configuration.

---

## 1. Purpose of the Raspberry Pi Module

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

The objective is to make the Raspberry Pi function as a self-contained attendance terminal.

---

# 2. Hardware Requirements

The Raspberry Pi module requires the following hardware.

| Component | Purpose |
| --- | --- |
| Raspberry Pi 3B+ | Main processing unit |
| Logitech HD 720p USB Webcam | Captures faces |
| microSD Card | Raspberry Pi operating system and project files |
| Raspberry Pi Power Supply | Provides stable power |
| Monitor/Display | Initial setup and troubleshooting |
| Keyboard | Initial setup and troubleshooting |
| Mouse | Initial setup and troubleshooting |
| USB storage device | Optional, for transferring project files |
| Network connection | Required if the configured application needs network services |

### Recommended camera

**Logitech HD 720p USB Webcam**

The webcam should be connected to one of the Raspberry Pi's USB ports.

---

# 3. Raspberry Pi 3B+ Role

The Raspberry Pi is responsible for running the deployed attendance application.

Its responsibilities are:

1. Initialize the camera.
2. Capture frames from the webcam.
3. Process the captured frames.
4. Detect faces.
5. Compare detected faces against the registered face data.
6. Determine the recognized identity.
7. Apply the attendance logic.
8. Save or transmit the attendance information according to the configured application.
9. Continue operating as an attendance terminal.

The Raspberry Pi is therefore the **execution device at the attendance location**.

---

# 4. Hardware Connection

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

### Connection procedure

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

---

# 5. Raspberry Pi Software Environment

The Raspberry Pi should contain the complete runtime environment required by the attendance application.

The deployed project should contain the application source code together with the required configuration and runtime files.

A typical deployed structure may look like:

```text
face-attendance/
│
├── README.md
├── requirements.txt
├── main.py
│
├── src/
│   ├── camera/
│   ├── face_detection/
│   ├── face_recognition/
│   └── attendance/
│
├── data/
│   ├── known_faces/
│   └── attendance/
│
├── models/
│
├── config/
│
└── logs/
```

> The exact filenames and directories must match the actual project structure deployed on the Raspberry Pi.

Do not create or rename directories only because they appear in this example. The project's actual software structure is the source of truth.

---

# 6. Operating System

The Raspberry Pi must run a Raspberry Pi-compatible Linux operating system supported by the project's dependencies.

Before deploying the application, verify:

```bash
uname -a
```

and:

```bash
cat /etc/os-release
```

These commands help identify the installed operating system and version.

Also verify the Raspberry Pi model:

```bash
cat /proc/device-tree/model
```

The expected hardware should identify the board as a Raspberry Pi 3 Model B Plus / Raspberry Pi 3B+.

---

# 7. Verify the Webcam

After connecting the Logitech webcam, check whether Linux detects it.

Run:

```bash
lsusb
```

The webcam should appear in the USB device list.

You can also check available video devices:

```bash
ls /dev/video*
```

A working camera commonly appears as:

```text
/dev/video0
```

The actual device number may differ if multiple cameras or video devices are connected.

---

# 8. Camera Verification

Before starting the complete attendance application, verify that the camera can capture images.

If the project uses OpenCV, the camera is generally accessed through a video device such as:

```text
/dev/video0
```

A basic camera test should verify:

- Camera opens successfully.
- Frames are received.
- Frames have the expected resolution.
- The image is not completely black.
- The camera remains stable during continuous capture.

The Logitech webcam is specified as a **720p-class camera**, but the application should use the resolution supported by the actual camera and the Raspberry Pi processing capability.

---

# 9. Camera Resolution

The project should use a resolution appropriate for the Raspberry Pi 3B+.

A higher resolution provides more image detail but increases:

- CPU processing
- memory usage
- frame-processing time
- image-transfer overhead

For an attendance terminal, the camera configuration should provide sufficient facial detail without unnecessarily increasing processing requirements.

A typical target may be:

```text
1280 × 720
```

if the webcam and application can maintain reliable processing at that resolution.

If recognition performance becomes slow, the deployed configuration may use a lower resolution.

The selected resolution should be documented in the project's camera configuration.

---

# 10. Face Recognition Workflow

The Raspberry Pi application follows the general pipeline below:

```text
Camera
   │
   ▼
Frame Capture
   │
   ▼
Face Detection
   │
   ▼
Face Region
   │
   ▼
Face Encoding / Feature Extraction
   │
   ▼
Comparison With Registered Faces
   │
   ▼
Identity Match
   │
   ▼
Attendance Decision
   │
   ▼
Attendance Record
```

Each stage has a separate purpose.

### 10.1 Frame Capture

The webcam continuously provides image frames to the application.

### 10.2 Face Detection

The application identifies areas of the frame that contain human faces.

### 10.3 Face Feature Processing

The detected face is processed using the configured face-recognition implementation.

### 10.4 Face Matching

The generated representation is compared with the registered face data.

### 10.5 Identity Identification

If the comparison satisfies the configured recognition threshold, the application identifies the corresponding registered person.

### 10.6 Attendance Processing

After successful recognition, the attendance module applies the project's attendance rules.

For example, the system may prevent the same person from being marked repeatedly within a configured period.

---

# 11. Registered Face Data

The Raspberry Pi must have access to the face data required by the deployed recognition system.

Depending on the implementation, this may include:

```text
Known face images
        or
Face encodings
        or
Precomputed face embeddings
        or
A database containing registered identities
```

The exact format depends on the project's implementation.

Each registered person should have a consistent identity mapping.

For example:

```text
Face Data
    │
    ├── Student ID
    ├── Student Name
    └── Face Representation
```

The recognition system should use the same identity information when creating attendance records.

---

# 12. Attendance Recording

After successful recognition, the application records the attendance event.

A record may contain information such as:

```text
Student ID
Student Name
Date
Time
Recognition Status
```

The actual fields depend on the project's implementation.

A typical attendance flow is:

```text
Face recognized
      │
      ▼
Identify student
      │
      ▼
Check attendance condition
      │
      ├── Already recorded
      │       │
      │       ▼
      │   Do not duplicate
      │
      └── Not recorded
              │
              ▼
        Create attendance entry
```

---

# 13. Duplicate Attendance Prevention

The attendance system should prevent accidental repeated entries caused by continuous camera frames.

For example, the camera may recognize the same person across many consecutive frames:

```text
Frame 1 → Student A
Frame 2 → Student A
Frame 3 → Student A
Frame 4 → Student A
Frame 5 → Student A
```

Without duplicate handling, this could create multiple attendance records.

Therefore, the attendance logic should determine whether an attendance event for that person has already been recorded according to the project's configured rules.

---

# 14. Raspberry Pi Performance Considerations

The Raspberry Pi 3B+ has considerably less processing power than a modern desktop computer.

Face recognition can be computationally expensive.

Therefore, the Raspberry Pi deployment should avoid unnecessary processing.

Important considerations include:

- Camera resolution
- Number of frames processed per second
- Face detection frequency
- Number of registered faces
- Recognition algorithm
- Image preprocessing
- Memory usage
- Background processes
- Storage performance
- Network dependency

The application should process only what is required for reliable attendance operation.

---

# 15. Recommended Processing Strategy

For an embedded attendance terminal, the application can avoid performing expensive recognition on every camera frame.

For example:

```text
Camera
  │
  ▼
Frame 1 ──► Process
Frame 2 ──► Skip
Frame 3 ──► Skip
Frame 4 ──► Process
Frame 5 ──► Skip
Frame 6 ──► Skip
Frame 7 ──► Process
```

The exact frame-processing strategy must match the project's implementation.

The purpose is to balance:

```text
Recognition Accuracy
        +
System Responsiveness
        +
Raspberry Pi CPU Usage
```

---

# 16. Power Requirements

A stable power supply is important.

Unexpected shutdowns can cause:

- Application interruption
- Corrupted files
- Incomplete attendance writes
- Filesystem problems
- Loss of unsaved data

The Raspberry Pi should therefore be powered using a suitable, stable power supply.

Avoid repeatedly disconnecting power while the operating system is running.

When possible, shut down the Raspberry Pi cleanly:

```bash
sudo shutdown -h now
```

or:

```bash
sudo poweroff
```

---

# 17. Storage

The Raspberry Pi's microSD card contains the operating system and deployed application.

The card may also contain:

- Application files
- Face data
- Configuration
- Logs
- Attendance records
- Required models

Monitor available storage:

```bash
df -h
```

If the application continuously creates images, logs, or attendance files, storage usage should be monitored regularly.

---

# 18. Network Configuration

The Raspberry Pi may require network access depending on the application's architecture.

Possible uses include:

- Synchronizing attendance data
- Accessing a remote database
- Communicating with an API
- Downloading required resources
- Remote administration

Check network connectivity with:

```bash
ip addr
```

and, where appropriate:

```bash
ping -c 4 8.8.8.8
```

Network access should not be assumed to be available unless the deployed application requires it.

If the attendance system is designed to work offline, attendance recording should follow the project's offline-storage design.

---

# 19. Python Environment

If the attendance application is Python-based, use the project's configured Python environment.

Check the Python version:

```bash
python3 --version
```

Check pip:

```bash
python3 -m pip --version
```

If the project contains a `requirements.txt`, its dependencies should be installed according to the project's deployment procedure.

Example:

```bash
python3 -m pip install -r requirements.txt
```

The actual installation command may differ depending on the project's environment and dependency requirements.

---

# 20. Important Raspberry Pi Dependency Consideration

Some computer-vision and face-recognition libraries can require native system packages or architecture-specific builds.

The Raspberry Pi 3B+ uses an ARM-based processor.

Therefore, dependencies must be compatible with:

```text
Raspberry Pi 3B+
        +
Installed Linux distribution
        +
Installed Python version
        +
ARM architecture
```

Do not assume that a Python package working on another computer will automatically work on the Raspberry Pi.

The Raspberry Pi deployment should use versions that are compatible with its architecture and operating-system environment.

---

# 21. Starting the Attendance Application

The exact startup command depends on the project's entry point.

For example, if the application's main file is:

```text
main.py
```

the application may be started with:

```bash
python3 main.py
```

If the project uses another entry point, use that project's documented startup command.

Before starting the application, verify:

```text
✓ Raspberry Pi is powered correctly
✓ Webcam is connected
✓ Webcam is detected
✓ Required project files exist
✓ Face data is available
✓ Required dependencies are installed
✓ Required configuration is present
✓ Network is available if required
```

---

# 22. Application Startup Checklist

Use the following checklist when starting the Raspberry Pi attendance terminal.

```text
[ ] Raspberry Pi powered on
[ ] Operating system booted
[ ] Webcam connected
[ ] Webcam detected
[ ] Camera device available
[ ] Project directory available
[ ] Python environment available
[ ] Required dependencies installed
[ ] Face data available
[ ] Configuration available
[ ] Attendance storage available
[ ] Network available if required
[ ] Attendance application started
```

---

# 23. Operational Flow

Once the system is running, the normal operation should be:

```text
             START
                │
                ▼
       Initialize Raspberry Pi
                │
                ▼
          Initialize Camera
                │
                ▼
         Capture Camera Frame
                │
                ▼
           Detect Face
                │
          ┌─────┴─────┐
          │           │
       No Face      Face Found
          │           │
          │           ▼
          │     Process Face
          │           │
          │           ▼
          │      Face Matching
          │           │
          │      ┌─────┴─────┐
          │      │           │
          │   Unknown     Recognized
          │      │           │
          │      │           ▼
          │      │     Attendance Check
          │      │           │
          │      │           ▼
          │      │      Record/Skip
          │      │
          └──────┴───────────┐
                             │
                             ▼
                       Continue Loop
```

The system remains in the processing loop until the application is stopped.

---

# 24. Stopping the Application

The application should be stopped using its supported shutdown mechanism.

If the application is running in a terminal and supports keyboard interruption, a common method is:

```text
Ctrl + C
```

After stopping the application, the Raspberry Pi itself can be shut down cleanly using:

```bash
sudo shutdown -h now
```

Do not disconnect the power immediately while the operating system is writing data.

---

# 25. Troubleshooting

## 25.1 Webcam Not Detected

Check:

```bash
lsusb
```

Then:

```bash
ls /dev/video*
```

If no video device appears:

1. Check the USB connection.
2. Try another USB port.
3. Restart the Raspberry Pi.
4. Check whether another application is using the camera.
5. Check system logs for USB/video errors.

---

## 25.2 Camera Opens but No Image Appears

Possible causes include:

- Incorrect camera device
- Camera already being used
- Unsupported resolution
- Incorrect camera backend
- Insufficient USB/power stability
- Application configuration problem

Check available video devices:

```bash
ls /dev/video*
```

Verify that the application is using the correct device.

---

## 25.3 Recognition Is Slow

Possible causes include:

- High camera resolution
- Processing every frame
- Too many registered faces
- Computationally expensive recognition model
- Other processes consuming CPU
- Insufficiently optimized image processing

Check CPU usage:

```bash
top
```

or:

```bash
htop
```

If necessary, review the configured camera resolution and frame-processing frequency.

---

## 25.4 Raspberry Pi Becomes Unresponsive

Check system resource usage:

```bash
free -h
```

and:

```bash
df -h
```

Also inspect CPU usage:

```bash
top
```

Potential causes include:

- Excessive memory usage
- High CPU utilization
- Storage problems
- Background processes
- Application memory leaks
- Insufficient power

---

## 25.5 Attendance Is Not Being Saved

Check:

1. Attendance directory exists.
2. Application has permission to write.
3. Storage is not full.
4. Database/file path is correct.
5. Required configuration is loaded.
6. Application logs contain no write errors.

Check storage:

```bash
df -h
```

Check directory permissions:

```bash
ls -la
```

---

## 25.6 Unknown Person Is Being Detected

Possible causes include:

- Person is not registered.
- Face data is missing.
- Lighting is poor.
- Face is too far from the camera.
- Face is partially blocked.
- Recognition threshold is inappropriate.
- Registered face data does not sufficiently represent the person's appearance.

The system should not automatically create a new identity solely because an unknown face appears.

---

# 26. Camera Placement

The webcam should be positioned so that faces are clearly visible.

Recommended placement:

```text
        Webcam
          │
          ▼
      ┌───────┐
      │ Face  │
      │       │
      └───────┘
```

Avoid:

- Strong backlighting
- Very dark environments
- Excessive camera angle
- Camera obstruction
- Extremely large distance from the subject
- Very close positioning that cuts off the face

Consistent camera placement improves recognition reliability.

---

# 27. Lighting

Lighting has a direct effect on face detection and recognition.

The attendance area should provide reasonably consistent illumination.

Avoid placing the camera directly toward a strong light source.

A suitable setup should allow the face to remain clearly visible:

```text
       Light
         ↓
      Person
         ↑
      Webcam
```

The exact lighting arrangement depends on the physical installation location.

---

# 28. Privacy and Data Handling

The Raspberry Pi processes facial information and attendance information.

The project team should therefore handle stored face data and attendance records responsibly.

Important practices include:

- Store only required data.
- Protect access to the Raspberry Pi.
- Restrict access to face data.
- Restrict access to attendance records.
- Avoid unnecessary storage of raw camera footage.
- Do not expose sensitive files through public network services.
- Follow the organization's applicable privacy and data-retention requirements.

The camera should be used for the intended attendance purpose only.

---

# 29. Security

The Raspberry Pi should not be treated as an unsecured device.

Recommended practices include:

- Use a strong account password.
- Avoid unnecessary services.
- Keep the operating system and required packages maintained according to the project's maintenance policy.
- Restrict physical access where possible.
- Protect the microSD card and stored face data.
- Do not expose administrative services unnecessarily.
- Do not store credentials directly in source code when a safer configuration mechanism is available.

---

# 30. Logging

The deployed application should provide sufficient logs to troubleshoot the Raspberry Pi installation.

Useful information may include:

```text
Application started
Camera initialized
Camera disconnected
Face detected
Face recognized
Unknown face detected
Attendance recorded
Attendance already exists
Application error
```

Logs should not unnecessarily contain sensitive facial data or credentials.

---

# 31. Maintenance Checklist

Periodically verify:

```text
[ ] Raspberry Pi boots normally
[ ] Webcam works correctly
[ ] Camera lens is clean
[ ] Camera position is correct
[ ] Recognition works
[ ] Attendance records are being created
[ ] Storage has sufficient free space
[ ] Logs do not contain repeated errors
[ ] Network works if required
[ ] Power supply is stable
[ ] Face data is available
[ ] Application configuration is intact
```

---

# 32. Deployment Verification

Before using the Raspberry Pi for real attendance, perform a complete test.

### Step 1 — Boot Test

Confirm that the Raspberry Pi starts correctly.

### Step 2 — Camera Test

Confirm that the Logitech webcam is detected.

### Step 3 — Face Detection Test

Place a registered person's face in front of the camera.

Confirm that the application detects the face.

### Step 4 — Recognition Test

Confirm that the correct registered identity is returned.

### Step 5 — Attendance Test

Confirm that an attendance record is created.

### Step 6 — Duplicate Test

Remain in front of the camera for several frames.

Confirm that the system does not incorrectly create repeated attendance entries.

### Step 7 — Unknown Face Test

Use an unregistered face.

Confirm that the system handles it according to the configured unknown-person behavior.

### Step 8 — Restart Test

Restart the Raspberry Pi and verify that the application can be started again successfully.

---

# 33. Final Raspberry Pi Deployment Checklist

Before handing the Raspberry Pi to the project team for operation:

```text
HARDWARE
[ ] Raspberry Pi 3B+ available
[ ] microSD card installed
[ ] Stable power supply connected
[ ] Logitech HD 720p webcam connected
[ ] Camera physically positioned correctly

OPERATING SYSTEM
[ ] Raspberry Pi OS/Linux boots correctly
[ ] Raspberry Pi model verified
[ ] Required system packages installed

APPLICATION
[ ] Project files present
[ ] Python version verified
[ ] Required dependencies installed
[ ] Configuration present
[ ] Face data present
[ ] Attendance storage configured

CAMERA
[ ] USB webcam detected
[ ] Video device available
[ ] Camera opens successfully
[ ] Frames are captured correctly
[ ] Resolution is appropriate

RECOGNITION
[ ] Registered face detected
[ ] Registered identity recognized
[ ] Unknown face handled correctly
[ ] Recognition performance acceptable

ATTENDANCE
[ ] Attendance record created
[ ] Date/time recorded correctly
[ ] Duplicate attendance handled
[ ] Attendance data persists correctly

SYSTEM
[ ] Storage has sufficient free space
[ ] Network works if required
[ ] Logs are functioning
[ ] Raspberry Pi shuts down cleanly
[ ] Physical access is controlled
```

---

# 34. Quick Reference Commands

### Check Raspberry Pi model

```bash
cat /proc/device-tree/model
```

### Check operating system

```bash
cat /etc/os-release
```

### Check Python

```bash
python3 --version
```

### Check USB devices

```bash
lsusb
```

### Check camera devices

```bash
ls /dev/video*
```

### Check IP/network interfaces

```bash
ip addr
```

### Check storage

```bash
df -h
```

### Check memory

```bash
free -h
```

### Check CPU/process usage

```bash
top
```

### Shut down safely

```bash
sudo shutdown -h now
```

---

# 35. System Architecture Summary

The Raspberry Pi module can be understood as five major layers:

```text
┌───────────────────────────────────────────┐
│             Attendance Layer              │
│       Attendance decision & records       │
├───────────────────────────────────────────┤
│           Recognition Layer               │
│       Face comparison / identification    │
├───────────────────────────────────────────┤
│             Detection Layer               │
│              Face detection               │
├───────────────────────────────────────────┤
│              Camera Layer                  │
│       Logitech HD 720p USB Webcam        │
├───────────────────────────────────────────┤
│             Hardware Layer                │
│              Raspberry Pi 3B+             │
└───────────────────────────────────────────┘
```

The complete Raspberry Pi operation is therefore:

```text
                Raspberry Pi 3B+
                       │
                       ▼
              Logitech HD Webcam
                       │
                       ▼
              Capture Frames
                       │
                       ▼
              Face Detection
                       │
                       ▼
             Face Recognition
                       │
                       ▼
             Attendance Record
```

---

# 36. Important Notes for Project Members

1. **The Raspberry Pi 3B+ is the target embedded hardware for this module.**
2. **The Logitech HD 720p USB webcam is the camera used by the attendance terminal.**
3. Camera detection should always be verified before troubleshooting the recognition software.
4. Recognition performance depends on camera quality, lighting, face position, processing configuration, and the recognition implementation.
5. Raspberry Pi 3B+ resources are limited, so unnecessary CPU and memory usage should be avoided.
6. The actual project directory structure and filenames should always take precedence over examples in this README.
7. Do not modify recognition thresholds, camera settings, model files, or attendance logic without understanding their effect on the complete system.
8. Attendance records and facial data should be protected from unauthorized access.
9. The Raspberry Pi should be shut down cleanly when it is not intended to remain powered.
10. Any hardware-specific change should be tested on the actual Raspberry Pi 3B+ before being considered part of the deployment.

---

# 37. Purpose of This Module

The Raspberry Pi 3B+ module provides the **physical execution platform** for the Face Recognition Attendance System.

Its complete responsibility is to connect the camera, process the captured facial information, identify registered individuals using the configured recognition system, and operate the attendance-recording workflow reliably in the intended physical environment.

```text
                FACE RECOGNITION
                       +
                 ATTENDANCE
                       │
                       ▼
              ┌─────────────────┐
              │ Raspberry Pi 3B+│
              └────────┬────────┘
                       │
                       ▼
              Logitech HD Webcam
                       │
                       ▼
              Face Detection
                       │
                       ▼
             Face Recognition
                       │
                       ▼
             Attendance Record
```

This README is intended to give project members a common understanding of the **Raspberry Pi hardware deployment, its role, operating workflow, verification procedure, troubleshooting, and maintenance requirements**.
