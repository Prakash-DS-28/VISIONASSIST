"""
navigator.py
Turns a raw detection box into simple, human-friendly guidance:
- zone: left / center / right (based on box x-position in frame)
- distance: near / medium / far (based on box height as a proxy -- no depth model needed)
"""


class Navigator:
    def __init__(self, near_ratio: float = 0.45, medium_ratio: float = 0.22):
        """
        Args:
            near_ratio: box_height / frame_height above this -> "near"
            medium_ratio: box_height / frame_height above this (but below near) -> "medium"
                          anything smaller -> "far"
        These are simple heuristics -- tune them by testing with a real bottle
        at a few known distances (e.g. 0.5m, 1.5m, 3m) and adjusting.
        """
        self.near_ratio = near_ratio
        self.medium_ratio = medium_ratio

    def get_zone(self, detection: dict) -> str:
        """Left / center / right based on box center x-position vs frame width."""
        cx, _ = detection["center"]
        _, w = detection["frame_shape"]

        left_bound = w / 3
        right_bound = 2 * w / 3

        if cx < left_bound:
            return "left"
        elif cx > right_bound:
            return "right"
        return "center"

    def get_distance(self, detection: dict) -> str:
        """Near / medium / far based on box height ratio (bigger box = closer)."""
        h, _ = detection["frame_shape"]
        ratio = detection["box_height"] / h

        if ratio >= self.near_ratio:
            return "near"
        elif ratio >= self.medium_ratio:
            return "medium"
        return "far"

    def describe(self, detection: dict) -> str:
        """Build a short spoken-friendly guidance string for a single detection."""
        zone = self.get_zone(detection)
        distance = self.get_distance(detection)

        zone_phrase = {
            "left": "on your left",
            "right": "on your right",
            "center": "straight ahead",
        }[zone]

        distance_phrase = {
            "near": "very close",
            "medium": "a few steps away",
            "far": "further away",
        }[distance]

        return f"{detection['class_name']} found {zone_phrase}, {distance_phrase}"

    def state_key(self, detection: dict) -> str:
        """A compact (zone, distance) key -- used by voice_output.py to detect state changes
        so it only speaks again when something meaningfully changed."""
        return f"{self.get_zone(detection)}|{self.get_distance(detection)}"
