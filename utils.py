"""
utils.py
Small shared helpers used across the app -- kept minimal on purpose.
"""

import time
import cv2


class FPSCounter:
    """Simple rolling FPS counter for on-screen display during the demo recording."""

    def __init__(self):
        self._last_time = time.time()
        self._fps = 0.0

    def tick(self) -> float:
        now = time.time()
        dt = now - self._last_time
        self._last_time = now
        self._fps = 1.0 / dt if dt > 0 else 0.0
        return self._fps

    @property
    def fps(self) -> float:
        return self._fps


def draw_status_text(frame, lines, origin=(10, 25), line_height=22, color=(255, 255, 255)):
    """Draw a stack of status lines (e.g. FPS, current command, search state) on a frame."""
    x, y = origin
    for i, line in enumerate(lines):
        cv2.putText(
            frame, line, (x, y + i * line_height),
            cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 1, cv2.LINE_AA,
        )
    return frame
