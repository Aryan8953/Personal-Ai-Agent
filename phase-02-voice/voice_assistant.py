import sys
from pathlib import Path

import speech_recognition as sr

# Allow Python to import the Phase 1 AI Brain
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PHASE_01_PATH = PROJECT_ROOT / "phase-01-ai-brain"

sys.path.append(str(PHASE_01_PATH))

from brain import AIBrain


recognizer = sr.Recognizer()


def listen():

    with sr.Microphone() as source:

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

    print("Processing speech...")

    try:

        text = recognizer.recognize_google(audio)

        return text

    except sr.UnknownValueError:

        print("I couldn't understand what you said.")
        return None

    except sr.RequestError as error:

        print(f"Speech recognition error: {error}")
        return None


def main():

    brain = AIBrain()

    print("================================")
    print("    Personal Voice Assistant")
    print("================================")
    print("Speak naturally.")
    print("Say 'exit' to stop.\n")

    while True:

        text = listen()

        if not text:
            continue

        print(f"You: {text}")

        if text.lower().strip() == "exit":

            print("Goodbye!")
            break

        print("AI: ", end="", flush=True)

        response = brain.chat(text)

        if response is None:

            print(
                "\nAI: I couldn't connect to the AI model.\n"
            )

        else:

            print("\n")


if __name__ == "__main__":
    main()