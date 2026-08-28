import tempfile
import threading
import wave
from pathlib import Path

import pygame

from piper import PiperVoice
from text_cleaner import clean_for_speech


PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    PROJECT_ROOT
    / "phase-02-voice"
    / "models"
    / "en_US-lessac-low.onnx"
)


print("Loading Piper voice...")

voice = PiperVoice.load(
    str(MODEL_PATH)
)

print("Piper voice loaded.")


# ==========================================
# Audio system
# ==========================================

pygame.mixer.init()

speech_thread = None
stop_event = threading.Event()


# ==========================================
# Generate + play speech
# ==========================================

def _speak_worker(text):

    temp_file = tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    )

    temp_path = Path(
        temp_file.name
    )

    temp_file.close()


    try:

        # Generate WAV
        with wave.open(
            str(temp_path),
            "wb"
        ) as wav_file:

            voice.synthesize_wav(
                text,
                wav_file
            )


        # If interrupted during generation
        if stop_event.is_set():

            return


        # Load generated audio
        pygame.mixer.music.load(
            str(temp_path)
        )


        # Start playback
        pygame.mixer.music.play()


        # Wait while audio is playing
        while pygame.mixer.music.get_busy():

            if stop_event.is_set():

                pygame.mixer.music.stop()

                return

            stop_event.wait(
                timeout=0.02
            )


    finally:

        # Release audio file
        try:

            pygame.mixer.music.unload()

        except Exception:

            pass


        # Delete temporary WAV
        try:

            temp_path.unlink()

        except PermissionError:

            pass


# ==========================================
# Speak
# ==========================================

def speak(text):

    global speech_thread


    text = clean_for_speech(
        text
    )


    if not text:

        return


    # Stop previous speech
    stop_speaking()


    stop_event.clear()


    speech_thread = threading.Thread(
        target=_speak_worker,
        args=(text,),
        daemon=True
    )


    speech_thread.start()


# ==========================================
# Stop speech
# ==========================================

def stop_speaking():

    stop_event.set()

    pygame.mixer.music.stop()


# ==========================================
# Check speech state
# ==========================================

def is_speaking():

    return pygame.mixer.music.get_busy()

if __name__ == "__main__":

    speak(
        "This is a test of the new responsive text to speech system."
    )