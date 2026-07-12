"""
app.py
VisionAssist -- "Find my [object]" voice-controlled object finder.

Flow:
  1. Wait for a voice command (e.g. "find my water bottle")
  2. Map the spoken phrase to a known COCO class via object_mapper
  3. Run YOLOv8 detection filtered to that class only
  4. When found, compute zone (left/center/right) + distance (near/medium/far)
  5. Speak the result; keep updating live guidance while the object stays in view
  6. Say "find <something else>" any time to search for a new object

Run: python app.py
"""

import time

import cv2

from src.detector import Detector
from src.object_mapper import ObjectMapper
from src.navigator import Navigator
from src.voice_input import VoiceInput
from src.voice_output import VoiceOutput
from src.utils import FPSCounter, draw_status_text


TRIGGER_WORD = "find"          # command must contain this to start a new search
NOT_FOUND_REMINDER_SEC = 4.0   # how often to say "still searching" if not found


def main():
    print("Loading detector...")
    detector = Detector(model_path="models/yolov8n.pt")
    mapper = ObjectMapper(detector)
    navigator = Navigator()
    voice_out = VoiceOutput()

    print("Loading microphone (speech recognition)...")
    voice_in = VoiceInput()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam.")

    fps_counter = FPSCounter()

    target_class_name = None
    target_class_id = None
    last_state_key = None
    last_not_found_time = 0.0

    voice_out.say("VisionAssist ready. Say find, followed by an object.", force=True)

    print("\nPress 'v' in the video window to speak a command, 'q' to quit.\n")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            fps = fps_counter.tick()
            status_lines = [f"FPS: {fps:.1f}"]

            if target_class_name:
                status_lines.append(f"Searching for: {target_class_name}")
            else:
                status_lines.append("No active search (press 'v' to speak a command)")

            # Only run detection when we actually have a target -- saves compute otherwise
            if target_class_name:
                detections = detector.detect(frame, target_class_ids=[target_class_id])
                frame = detector.draw_detections(frame, detections, highlight_class=target_class_name)

                if detections:
                    best = detections[0]  # highest confidence match
                    state_key = navigator.state_key(best)

                    # Speak only when the zone/distance actually changed (avoids spamming)
                    if state_key != last_state_key:
                        message = navigator.describe(best)
                        voice_out.say(message)
                        last_state_key = state_key
                else:
                    # Not found this frame -- periodically remind the user we're still looking
                    now = time.time()
                    if now - last_not_found_time > NOT_FOUND_REMINDER_SEC:
                        voice_out.say(f"Still searching for {target_class_name}")
                        last_not_found_time = now
                    last_state_key = None
            else:
                # No active search -- just show the raw feed
                pass

            frame = draw_status_text(frame, status_lines)
            cv2.imshow("VisionAssist", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            elif key == ord("v"):
                voice_out.say("Listening", force=True)
                spoken = voice_in.listen()
                print("Heard:", spoken)

                if spoken and TRIGGER_WORD in spoken:
                    class_name, class_id = mapper.resolve(spoken)
                    if class_name:
                        target_class_name = class_name
                        target_class_id = class_id
                        last_state_key = None
                        voice_out.reset()
                        voice_out.say(f"Searching for {class_name}", force=True)
                    else:
                        voice_out.say(
                            "Sorry, I don't recognize that object. "
                            f"Try one of: {mapper.supported_items_text()}",
                            force=True,
                        )
                elif spoken:
                    voice_out.say("Please start your command with the word find.", force=True)

    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
