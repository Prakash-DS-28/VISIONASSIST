# 🦾 VisionAssist

### *AI-Powered Object Finder for the Visually Impaired*

<p align="center">
  <img src="assets/logo.png" width="180"/>
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge\&logo=python)
![YOLOv8](https://img.shields.io/badge/YOLO-v8-green?style=for-the-badge)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-red?style=for-the-badge\&logo=opencv)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
![HackZen](https://img.shields.io/badge/HackZen-2026-orange?style=for-the-badge)

</p>

---

# 📌 Overview

**VisionAssist** is an AI-powered accessibility assistant that helps visually impaired individuals locate everyday objects using **Computer Vision**, **Artificial Intelligence**, and **Voice Guidance**.

The user simply asks for an object, such as:

> 🎤 *"Find my water bottle."*

The system detects the object in real time using **YOLOv8**, identifies its position, and provides spoken navigation instructions until the object is within reach.

---

# 🎯 Problem Statement

Visually impaired individuals often face difficulty locating common objects such as:

* 💧 Water Bottle
* 📱 Mobile Phone
* 💻 Laptop
* 🎒 Backpack
* 🪑 Chair
* ☕ Cup

Searching for these objects without assistance can be time-consuming and frustrating.

---

# 💡 Our Solution

VisionAssist combines:

* 🎤 Voice Commands
* 👁️ Real-Time Computer Vision
* 🧠 Artificial Intelligence
* 🔊 Voice Guidance

to help users quickly locate the requested object.

---

# ✨ Features

✅ Voice Command Support

✅ Real-Time Object Detection

✅ AI-Based Object Search

✅ Left / Right / Center Navigation

✅ Approximate Distance Estimation

✅ Voice Feedback

✅ Live Camera Detection

✅ Lightweight & Fast

---

# 🏗️ System Architecture

```text
                 User

                   │

         "Find my Bottle"

                   │

         Speech Recognition

                   │

         Object Extraction

                   │

           Webcam Input

                   │

          YOLOv8 Detection

                   │

        Requested Object Found?

            │             │
           No             Yes
            │              │
      Continue Search      │
                           ▼
                  Position Detection

                           ▼
                 Distance Estimation

                           ▼
                  Voice Navigation

                           ▼
                   Object Reached
```

---

# 🖥️ Tech Stack

| Technology        | Purpose              |
| ----------------- | -------------------- |
| Python            | Backend              |
| YOLOv8            | Object Detection     |
| OpenCV            | Camera Processing    |
| PyTorch           | Deep Learning        |
| pyttsx3           | Text-to-Speech       |
| SpeechRecognition | Voice Input          |
| NumPy             | Numerical Operations |

---

# 📁 Project Structure

```text
VisionAssist/
│
├── app.py
├── requirements.txt
├── README.md
│
├── models/
│   └── yolov8n.pt
│
├── src/
│   ├── detector.py
│   ├── navigator.py
│   ├── voice_input.py
│   ├── voice_output.py
│   ├── object_mapper.py
│   └── utils.py
│
├── assets/
│   ├── logo.png
│   └── screenshots/
│
├── outputs/
│
└── docs/
```

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/your-username/VisionAssist.git

cd VisionAssist
```

Install dependencies

```bash
pip install -r requirements.txt
```

Download the YOLOv8 model

```bash
# Place yolov8n.pt inside the models/ directory
```

Run the application

```bash
python app.py
```

---

# 🎤 Example Usage

User:

> "Find my water bottle."

Assistant:

> 🔍 Searching for water bottle...

> ✅ Bottle found.

> ⬅️ Move left.

> ⬆️ Move forward.

> ✅ Bottle is within reach.

---

# 📸 Demo

## Live Detection

*(Add screenshot here)*

```
assets/screenshots/demo.png
```

---

# 📊 Supported Objects

* Bottle
* Chair
* Backpack
* Cell Phone
* Laptop
* Cup
* Book
* Mouse
* Keyboard
* Person

---

# ⚙️ Requirements

### Hardware

* Webcam
* Microphone
* Speaker / Headphones
* Laptop/Desktop

### Software

* Python 3.10+
* OpenCV
* YOLOv8
* PyTorch

---

# 📈 Future Enhancements

* 🌍 Offline Voice Recognition
* 👓 Smart Glasses Integration
* 📱 Android Application
* 📍 Accurate Depth Estimation
* 🧭 Indoor Navigation
* 📖 OCR for Reading Text
* 🌐 Multi-language Voice Support
* 📳 Haptic Feedback

---

# 👨‍💻 Team

| Name     | Role                 |
| -------- | -------------------- |
| Member 1 | AI & Computer Vision |
| Member 2 | Backend Development  |
| Member 3 | UI / Documentation   |

---

# 🏆 HackZen 2026

Developed as part of the **HackZen 2026 Open Challenge**.

Our goal is to leverage Artificial Intelligence and Computer Vision to create accessible technology that empowers visually impaired individuals in their daily lives.

---

# 📜 License

This project is licensed under the **MIT License**.

---

<div align="center">

### ⭐ If you found this project interesting, consider giving it a Star ⭐

**Made with ❤️ using Python, OpenCV & YOLOv8**

</div>
