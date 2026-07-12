"""
voice_output.py
Text-to-speech feedback using pyttsx3 (offline, no API key, low latency).

Includes a simple cooldown so the same message isn't repeated every frame --
only speaks again when the state actually changes or the cooldown expires.
"""

import time
import pyttsx3


class VoiceOutput:
    def __init__(self, rate: int = 170, volume: float = 1.0, cooldown_sec: float = 3.0):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", rate)
        self.engine.setProperty("volume", volume)

        self.cooldown_sec = cooldown_sec
        self._last_message = None
        self._last_spoken_time = 0.0

    def say(self, text: str, force: bool = False):
        """
        Speak text, but skip repeating the exact same message within the cooldown window.

        Args:
            text: message to speak
            force: speak immediately regardless of cooldown/duplicate check
        """
        now = time.time()
        is_duplicate = text == self._last_message
        within_cooldown = (now - self._last_spoken_time) < self.cooldown_sec

        if not force and is_duplicate and within_cooldown:
            return

        self.engine.say(text)
        self.engine.runAndWait()

        self._last_message = text
        self._last_spoken_time = now

    def reset(self):
        """Clear dedup state -- call when starting a new search for a different object."""
        self._last_message = None
        self._last_spoken_time = 0.0


# Quick standalone test: python src/voice_output.py
if __name__ == "__main__":
    vo = VoiceOutput()
    vo.say("Bottle found, straight ahead, a few steps away")
