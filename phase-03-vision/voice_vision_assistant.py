import sys
from pathlib import Path

import speech_recognition as sr

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PHASE_01_PATH = PROJECT_ROOT / "phase-01-ai-brain"
PHASE_02_PATH = PROJECT_ROOT / "phase-02-voice"

sys.path.append(str(PHASE_01_PATH))
sys.path.append(str(PHASE_02_PATH))

from brain import AIBrain
from tts import speak
from intent_router import needs_screen
from screen_context import get_screen_context


# ==============================
# Speech Recognition
# ==============================

recognizer = sr.Recognizer()


def listen():

    with sr.Microphone() as source:

        print("\n🎤 Listening...")

        try:

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=15
            )

        except sr.WaitTimeoutError:

            print("I didn't hear anything.")
            return None

    print("Processing speech...")

    try:

        text = recognizer.recognize_google(audio)

        return text.strip()

    except sr.UnknownValueError:

        print("I couldn't understand what you said.")
        return None

    except sr.RequestError as error:

        print(f"Speech recognition error: {error}")
        return None


# ==============================
# Main Assistant
# ==============================

def main():

    brain = AIBrain()

    print("================================")
    print("   Personal Vision Assistant")
    print("================================")
    print("Voice + Ollama + Vision + Piper")
    print("Say 'exit' to stop.\n")

    while True:

        text = listen()

        if not text:
            continue

        print(f"You: {text}")

        if text.lower() == "exit":

            print("Goodbye!")
            break

        # ==========================
        # Decide whether vision needed
        # ==========================

        if needs_screen(text):

            print("\n👁️ Looking at your screen...")

            screen_context = get_screen_context(text)

            prompt = f"""
The user asked:

{text}

Information obtained from the user's current screen:

{screen_context}

Answer the user's question naturally and directly.
Do not mention the vision model, screenshot, or internal
processing unless the user specifically asks.
"""

            response = brain.chat(prompt)

        else:

            response = brain.chat(text)

        # ==========================
        # Speak response
        # ==========================

        if response:

            print("\n🔊 Speaking...")

            speak(response)

        else:

            print("\nAI: I couldn't generate a response.")


if __name__ == "__main__":
    main()