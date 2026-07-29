# GestureSync

<p align="center">
  <img src="assets/splash_image.png" alt="GestureSync Banner" width="700"/>
</p>

<p align="center">
  <strong>A desktop application for hands-free computer interaction using Hand Gestures and Head Tracking.</strong>
</p>

---

## Overview

GestureSync is a desktop application that enables users to control a computer using a standard webcam instead of traditional input devices. By combining computer vision and machine learning, the system recognizes hand gestures and facial movements in real time to perform common mouse operations such as cursor movement, clicking, dragging, and scrolling.

The application provides two independent control modes:

- 🖐️ Hand Gesture Control
- 👤 Head Tracking Control

GestureSync is designed to provide an intuitive, accessible, and hardware-independent approach to human-computer interaction using only a webcam.

---

## Features

- 🎥 Real-time webcam-based interaction
- 🖐️ Hand gesture recognition
- 👤 Head tracking mouse control
- 🖱️ Cursor navigation
- 👆 Left Click & Right Click
- 📌 Drag and Drop
- 📜 Scroll Up & Scroll Down
- ⚡ Low-latency real-time processing
- 💻 Modern desktop interface built with PyQt5
- 🔒 Fully offline processing for enhanced privacy

---

## Supported Controls

### Hand Gesture Mode

- Cursor Navigation
- Left Click
- Right Click
- Drag and Drop
- Rest (Idle)

### Head Tracking Mode

- Cursor Movement
- Blink Detection
- Scroll Up
- Scroll Down
- Neutral Detection

---

## Technology Stack

### Programming Language

- Python

### Computer Vision

- OpenCV
- MediaPipe

### Machine Learning

- TensorFlow
- TensorFlow Lite
- MobileNetV2
- Convolutional Neural Networks (CNN)

### GUI

- PyQt5

### Automation

- PyAutoGUI

### Additional Libraries

- NumPy
- Pillow
- Matplotlib

---

## Project Structure

```text
GestureSyncApp/
│
├── assets/
│   ├── app_icon.ico
│   ├── cam_icon.png
│   ├── hand_icon.png
│   ├── head_icon.png
│   ├── splash_image.png
│   └── expression_pointer.tflite
│
├── Gesture_controller_2.py
├── livetrack.py
├── gui_app.py
├── convert.py
├── build_script.bat
├── ClearMemory.bat
├── requirements.txt
└── .gitignore
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/AnkithBinagekar/GestureSyncApp.git
cd GestureSyncApp
```

### Create a Virtual Environment

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

```bash
python gui_app.py
```

Select your preferred control mode from the home screen:

- Hand Gesture Control
- Head Tracking Control

---

## Hardware Requirements

### Minimum

- Intel Core i3 or equivalent
- 4 GB RAM
- HD Webcam (720p)
- Windows 10/11
- Python 3.10+

### Recommended

- Intel Core i5 / AMD Ryzen 5 or higher
- 8 GB RAM or more
- NVIDIA GPU (optional)
- 1080p Webcam

---

## Performance

GestureSync achieves:

- **93%** Head Tracking Accuracy
- **95%** Hand Gesture Recognition Accuracy
- Real-time gesture detection
- Low-latency processing

Performance may vary depending on system specifications, lighting conditions, and webcam quality. :contentReference[oaicite:2]{index=2}

---

## Applications

- Assistive Technology
- Accessibility Solutions
- Gesture-Based Human-Computer Interaction
- Touch-Free Desktop Control
- Smart Computing Interfaces

---

## Future Enhancements

- Voice Command Integration
- Custom Gesture Training
- Additional Gesture Support
- Cross-Platform Improvements
- Enhanced CPU Optimization
- Expanded Accessibility Features

These enhancements are consistent with the future scope outlined in the project report. :contentReference[oaicite:3]{index=3}

---

## Contributors

- Junaid Al Amin
- Kevin Saby Mundappallil
- Sarthak Sunil Patil

---

## Acknowledgements

GestureSync is built using several outstanding open-source technologies:

- OpenCV
- MediaPipe
- TensorFlow
- PyQt5
- PyAutoGUI

We sincerely appreciate the efforts of the open-source community for making these tools available.

---

## License

This project is currently distributed without a license.
