"""
object_mapper.py
Maps free-form spoken phrases ("find my water bottle") to a known COCO class name
("bottle") that the detector can search for.

Keeps a small, hand-picked vocabulary of everyday indoor objects rather than
trying to cover all 80 COCO classes -- easier to keep reliable in a demo.
"""

# phrase keyword -> COCO class name (must match names in yolov8n.pt exactly)
KEYWORD_TO_COCO = {
    "bottle": "bottle",
    "water bottle": "bottle",
    "cup": "cup",
    "mug": "cup",
    "phone": "cell phone",
    "cell phone": "cell phone",
    "mobile": "cell phone",
    "laptop": "laptop",
    "bag": "backpack",
    "backpack": "backpack",
    "book": "book",
    "remote": "remote",
    "remote control": "remote",
    "keyboard": "keyboard",
    "mouse": "mouse",
    "chair": "chair",
    "clock": "clock",
    "scissors": "scissors",
    "umbrella": "umbrella",
    "handbag": "handbag",
}

# Only the COCO classes actually reachable via the map above -- used to validate
SUPPORTED_COCO_CLASSES = set(KEYWORD_TO_COCO.values())


class ObjectMapper:
    def __init__(self, detector):
        """
        Args:
            detector: an instance of Detector (src/detector.py), used to validate
                      that a mapped COCO name is really a class the model knows.
        """
        self.detector = detector

    def resolve(self, spoken_text: str):
        """
        Turn a spoken command into a target COCO class name + id.

        Args:
            spoken_text: raw text from voice_input.py, e.g. "find my water bottle"

        Returns:
            (class_name, class_id) if a known object was found in the phrase, else (None, None)
        """
        text = spoken_text.lower().strip()

        # Check multi-word phrases first (e.g. "water bottle" before "bottle")
        for phrase in sorted(KEYWORD_TO_COCO.keys(), key=len, reverse=True):
            if phrase in text:
                class_name = KEYWORD_TO_COCO[phrase]
                class_id = self.detector.class_id_for_name(class_name)
                if class_id is not None:
                    return class_name, class_id

        return None, None

    def supported_items_text(self):
        """Human-readable list for prompting the user, e.g. in a help message."""
        return ", ".join(sorted(SUPPORTED_COCO_CLASSES))
