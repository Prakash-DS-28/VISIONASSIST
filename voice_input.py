"""
voice_input.py
Captures a spoken command from the microphone and returns it as text.

Uses SpeechRecognition + Google's free web speech API (requires internet).
"""

import speech_recognition as sr


class VoiceInput:
    def __init__(
        self,
        energy_threshold: int = 50,
        pause_threshold: float = 0.8,
        device_index: int = None,
    ):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = energy_threshold
        self.recognizer.pause_threshold = pause_threshold
        self.recognizer.dynamic_energy_threshold = False  # keep threshold fixed and low

        # device_index=None uses the OS default input device.
        # Run this to list devices and find your headset's index:
        #   python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"
        self.mic = sr.Microphone(device_index=device_index)

        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        print(f"[voice_input] using energy_threshold = {self.recognizer.energy_threshold:.1f}")

    def listen(self, timeout: float = 8.0, phrase_time_limit: float = 6.0):
        with self.mic as source:
            print("[voice_input] listening now...")
            try:
                audio = self.recognizer.listen(
                    source, timeout=timeout, phrase_time_limit=phrase_time_limit
                )
            except sr.WaitTimeoutError:
                print("[voice_input] timed out waiting for speech")
                return None

        print("[voice_input] got audio, sending to Google...")
        try:
            text = self.recognizer.recognize_google(audio)
            return text.lower()
        except sr.UnknownValueError:
            print("[voice_input] Google could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"[voice_input] API request failed: {e}")
            return None


# Quick standalone test: python src/voice_input.py
if __name__ == "__main__":
    print("Available microphones:")
    for i, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"  [{i}] {name}")

    device_index = input("\nEnter the device index to use (or press Enter for default): ").strip()
    device_index = int(device_index) if device_index else None

    vi = VoiceInput(device_index=device_index)
    print("\nSay something like: 'find my water bottle'")
    result = vi.listen()
    print("Heard:", result)