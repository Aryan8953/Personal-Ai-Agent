import sys
import tempfile
import wave
from pathlib import Path
import webrtcvad


import speech_recognition as sr

from faster_whisper import WhisperModel

from interruption import MicrophoneMonitor
from tts import speak, stop_speaking, is_speaking


# ==============================
# Project Configuration
# ==============================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PHASE_01_PATH = PROJECT_ROOT / "phase-01-ai-brain"

sys.path.append(str(PHASE_01_PATH))

from brain import AIBrain


# ==============================
# Whisper Configuration
# ==============================

WHISPER_MODEL_SIZE = "base"

print("Loading Whisper model...")

whisper_model = WhisperModel(
    WHISPER_MODEL_SIZE,
    device="cpu",
    compute_type="int8"
)

print("Whisper model loaded.")


# ==============================
# Microphone Configuration
# ==============================

recognizer = sr.Recognizer()
vad = webrtcvad.Vad(2)


def contains_speech(audio):

    raw_audio = audio.get_raw_data(
        convert_rate=16000,
        convert_width=2
    )

    frame_size = int(
        16000 * 0.03 * 2
    )

    speech_frames = 0
    total_frames = 0

    for start in range(
        0,
        len(raw_audio),
        frame_size
    ):

        frame = raw_audio[
            start:start + frame_size
        ]

        if len(frame) != frame_size:
            continue

        total_frames += 1

        if vad.is_speech(
            frame,
            16000
        ):

            speech_frames += 1

    if total_frames == 0:
        return False

    speech_ratio = (
        speech_frames / total_frames
    )

    return speech_ratio >= 0.25

def listen():

    with sr.Microphone(
        sample_rate=16000
    ) as source:

        print("\nListening...")

        try:

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=15
            )

        except sr.WaitTimeoutError:

            print("I didn't hear anything.")

            return None


    # ==========================================
    # Save microphone audio
    # ==========================================

    temp_file = tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    )

    temp_path = Path(
        temp_file.name
    )

    temp_file.close()


    try:

        with wave.open(
            str(temp_path),
            "wb"
        ) as wav_file:

            wav_file.setnchannels(1)

            wav_file.setsampwidth(
                audio.sample_width
            )

            wav_file.setframerate(
                audio.sample_rate
            )

            wav_file.writeframes(
                audio.get_raw_data()
            )


        print("Processing speech...")


        # ==========================================
        # Whisper with stronger filtering
        # ==========================================

        segments, info = whisper_model.transcribe(

            str(temp_path),

            language="en",

            temperature=0.0,

            condition_on_previous_text=False,

            vad_filter=True,

            vad_parameters={
                "min_silence_duration_ms": 500
            }
        )


        texts = []


        for segment in segments:

            # Ignore likely silence
            if segment.no_speech_prob > 0.60:
                continue

            # Ignore very low-confidence segments
            if segment.avg_logprob < -1.0:
                continue

            text = segment.text.strip()

            if not text:
                continue

            texts.append(text)


        # ==========================================
        # No reliable speech
        # ==========================================

        if not texts:

            print(
                "No reliable speech detected."
            )

            return None


        text = " ".join(texts).strip()


        # ==========================================
        # Reject common hallucinations
        # ==========================================

        hallucinations = {
            "thank you",
            "thanks",
            "thanks for watching",
            "thank you for watching",
            "please subscribe",
            "subscribe",
            "you",
            "bye",
            "goodbye"
        }


        normalized = text.lower().strip(
            " .,!?-'\""
        )


        if normalized in hallucinations:

            print(
                "Ignored possible Whisper hallucination."
            )

            return None


        return text


    finally:

        try:

            temp_path.unlink()

        except PermissionError:

            pass
     


# ==============================
# Main Assistant
# ==============================

def main():

    brain = AIBrain()


    print("================================")
    print("    Personal Voice Assistant")
    print("================================")
    print("Local Whisper + Ollama + Piper")
    print("Barge-in enabled")
    print("Speak naturally.")
    print("Say 'exit' to stop.\n")


    while True:

        # ==========================
        # Listen for user command
        # ==========================

        text = listen()


        if not text:

            continue


        print(f"You: {text}")


        # ==========================
        # Exit command
        # ==========================

        if text.lower().strip() == "exit":

            print("Goodbye!")

            break


        # ==========================
        # AI Brain
        # ==========================

        print(
            "AI: ",
            end="",
            flush=True
        )


        response = brain.chat(text)


        # ==========================
        # AI Voice
        # ==========================

        if response:
            monitor = MicrophoneMonitor(
                 whisper_model
            )

            speak(response)

            monitor.start()

            interrupted_command = None

        try:
            while is_speaking():
                if monitor.interrupted():
                    print(
                    "\nStopping AI speech..."
                )

                    stop_speaking()

                    interrupted_command = monitor.get_text()
                

                    break

        finally:

            monitor.stop()


        if interrupted_command:
            print(
            f"You interrupted with: "
            f"{interrupted_command}"
        )

            print(
            "AI: ",
            end="",
            flush=True
        )

            new_response = brain.chat(
            interrupted_command
        )

            if new_response:
                speak(new_response)

                while is_speaking():
                    pass

        print()


        # ==========================
        # Error Handling
        # ==========================

        if response is None:

            print(
                "\nAI: I couldn't connect "
                "to the AI model.\n"
            )

        else:

            print("\n")
def transcribe_audio(audio):

    if audio is None:
        return None

    temp_file = tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    )

    temp_path = Path(temp_file.name)

    temp_file.close()

    try:

        with wave.open(
            str(temp_path),
            "wb"
        ) as wav_file:

            wav_file.setnchannels(1)

            wav_file.setsampwidth(
                audio.sample_width
            )

            wav_file.setframerate(
                audio.sample_rate
            )

            wav_file.writeframes(
                audio.get_raw_data()
            )

        segments, info = whisper_model.transcribe(
            str(temp_path)
        )

        text = ""

        for segment in segments:
            text += segment.text

        text = text.strip()

        return text if text else None

    finally:

        try:
            temp_path.unlink()

        except PermissionError:
            pass

if __name__ == "__main__":

    main()