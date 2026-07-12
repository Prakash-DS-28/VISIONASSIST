# VisionAssist

Voice-controlled object finder for accessibility. Say **"find my water bottle"**,
and VisionAssist listens, searches the live camera feed using computer vision,
and speaks back where the object is (left / center / right, and how far).
Problem Statement

Losing track of everyday objects — a water bottle, phone, keys, remote — is a
small daily friction for most people, but a real accessibility barrier for
visually impaired users, who cannot visually scan a room to relocate items.
Existing assistive solutions are typically either expensive dedicated hardware
(smart glasses, specialized sensors) or apps that require pointing a phone
camera and reading on-screen text — neither is fast, hands-free, nor genuinely
usable by someone who can't see the screen in the first place.

Objective

Build a lightweight, hands-free, voice-in / voice-out system that lets a user
ask for an object by name and receive spoken, directional guidance to it in
real time — using only a standard webcam and pretrained, off-the-shelf
computer vision models, deployable on ordinary consumer hardware with no
specialized sensors and no model training required.

Proposed Solution

VisionAssist runs a continuous voice-in / vision / voice-out loop:


Listen — the user speaks a command ("find my water bottle")
Understand — the phrase is mapped to a known object category ("bottle")
See — a real-time object detector scans the webcam feed, filtered to
just that category, so it isn't distracted by irrelevant objects
Localize — the detected object's position and size in the frame are
converted into simple spatial guidance: left / center / right, and
near / medium / far
Speak — the guidance is read aloud immediately, and continues updating
live as the object or the user moves, until the user asks to find something
else


The entire pipeline is built on pretrained, open-source models — no custom
training, no labeled dataset collection, and no cloud infrastructure beyond a
single free speech-to-text API call per voice command.

Technologies Used

ComponentTechnologyObject detectionUltralytics YOLOv8n — pretrained on COCODeep learning backendPyTorchComputer vision / video I/OOpenCVSpeech-to-textSpeechRecognition (Google Web Speech API)Text-to-speechpyttsx3 (fully offline)LanguagePython 3

Dataset

No custom dataset or training was required. Object detection uses
YOLOv8n pretrained on the COCO dataset
(80 everyday object classes — bottle, cup, cell phone, laptop, backpack, book,
chair, and more), used directly via Ultralytics' pretrained weights.

Methodology / Model Architecture

                ┌───────────────┐
   Microphone → │ voice_input.py │ → raw speech → text (Google Speech API)
                └───────┬────────┘
                        ▼
                ┌────────────────┐
                │ object_mapper  │  "water bottle" → COCO class "bottle"
                └───────┬────────┘
                        ▼
     Webcam → ┌──────────────────┐
     frames   │   detector.py     │  YOLOv8n inference, filtered to
              │   (YOLOv8n, COCO) │  the requested class only
              └───────┬───────────┘
                        ▼
                ┌────────────────┐
                │  navigator.py   │  bounding box → zone (L/C/R)
                │                 │  + distance (near/med/far)
                └───────┬────────┘
                        ▼
                ┌────────────────┐
   Speaker  ←   │ voice_output.py │  spoken guidance, de-duplicated
                └────────────────┘  so it only re-announces on change

Key design decisions:


Class-filtered detection — once a target object is known, YOLO is asked
to detect only that class, improving speed and avoiding false alarms from
unrelated objects in frame.
Bounding-box-based distance estimate — instead of a separate depth model
(extra latency, extra failure point), distance is approximated from how much
of the frame the object's bounding box occupies: a larger box means the
object is closer. This is a well-established lightweight heuristic that
avoids needing monocular depth estimation for a real-time, resource-constrained
demo.
State-change-only speech — guidance is only re-spoken when the object's
zone or distance actually changes, preventing the assistant from repeating
itself every frame.


Installation & Setup Instructions

bashgit clone <your-repo-url>
cd VisionAssist
pip install -r requirements.txt


Note: pyaudio can require an extra system package on some platforms:


Windows: pip install pipwin && pipwin install pyaudio
macOS: brew install portaudio && pip install pyaudio
Linux: sudo apt-get install portaudio19-dev espeak-ng alsa-utils && pip install pyaudio




models/yolov8n.pt (pretrained weights, ~6MB) auto-downloads on first run if
not already present in the repo.

Usage Instructions

bashpython app.py


Press v in the video window, then speak a command, e.g.:
"find my water bottle", "find my phone", "find my keyboard"
VisionAssist confirms the search target out loud, then announces the
object's location once detected — continuing to update live as it or you
move.
Say "find" followed by a different object at any time to switch targets.
Press q to quit.


Supported objects (demo vocabulary): bottle, cup/mug, cell phone, laptop,
backpack/bag, book, remote, keyboard, mouse, chair, clock, scissors, umbrella,
handbag — easily extended by adding entries to KEYWORD_TO_COCO in
src/object_mapper.py.

Results and Outputs


Real-time detection at interactive frame rates on standard CPU hardware
(tested at 416px YOLO inference resolution — no GPU required)
Accurate left/center/right + near/medium/far spoken guidance for
in-vocabulary objects across typical indoor lighting and clutter conditions
Hands-free operation validated end-to-end: voice command → detection →
spoken directional guidance, with no screen interaction required
Demo video: see demo/ folder (or linked Drive submission)


Future Scope


Open-vocabulary detection (e.g. YOLO-World) to recognize arbitrary
object names beyond COCO's fixed 80 classes
Personalized object recognition to distinguish "my" bottle from
someone else's identical one
True monocular depth estimation for finer-grained distance accuracy,
replacing the current bounding-box-size proxy
Door and staircase detection to extend the system toward full indoor
navigation assistance, not just object-finding
Offline speech recognition (e.g. Vosk) as a fallback for use without
an internet connection


References


Ultralytics YOLOv8 — https://github.com/ultralytics/ultralytics
COCO Dataset — https://cocodataset.org/
SpeechRecognition (Python library) — https://github.com/Uberi/speech_recognition
pyttsx3 (Python library) — https://github.com/nateshmbhat/pyttsx3