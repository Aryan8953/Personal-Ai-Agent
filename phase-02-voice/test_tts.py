import time

from tts import speak, stop_speaking


speak(
    "This is a long sentence designed to test whether "
    "the speech controller can be interrupted while the "
    "assistant is talking."
)

time.sleep(3)

print("Stopping speech...")

stop_speaking()

print("Speech stopped.")