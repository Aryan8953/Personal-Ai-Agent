import sys
from pathlib import Path

import speech_recognition as sr


# ==============================
# Project paths
# ==============================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PHASE_01_PATH = PROJECT_ROOT / "phase-01-ai-brain"
PHASE_02_PATH = PROJECT_ROOT / "phase-02-voice"
TOOLS_PATH = PROJECT_ROOT / "tools"

sys.path.insert(0, str(PHASE_01_PATH))
sys.path.insert(0, str(PHASE_02_PATH))
sys.path.insert(0, str(TOOLS_PATH))


# ==============================
# Imports
# ==============================

from brain import AIBrain
from tts import speak

from ai_tool_router import route_request
from tool_executor import execute_tool


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
# Tool handling
# ==============================

def handle_tool_request(
    user_input,
    decision,
    brain
):

    tool_name = decision.get("tool")

    arguments = decision.get(
        "arguments",
        {}
    )

    print(f"\n🛠️ Tool: {tool_name}")
    print(f"📦 Arguments: {arguments}")

    result = execute_tool(
        tool_name,
        arguments
    )

    print(f"💻 Result: {result}")

    # If the tool was screen inspection,
    # let the main AI turn the visual result
    # into a natural answer.

    if tool_name == "inspect_screen":

        prompt = f"""
The user asked:

{user_input}

The following information was obtained
from the user's current screen:

{result}

Answer the user's question naturally and directly.

Do not mention internal tools, tool execution,
screenshots, or model names unless the user
specifically asks about them.
"""

        return brain.chat(prompt)

    return result


# ==============================
# Main Assistant
# ==============================

def main():

    brain = AIBrain()

    print("================================")
    print("   Personal Vision Assistant")
    print("================================")
    print("Voice + AI + Vision + Tools + Piper")
    print("Say 'exit' to stop.\n")

    while True:

        text = listen()

        if not text:
            continue

        print(f"You: {text}")

        if text.lower().strip() == "exit":

            print("Goodbye!")
            break

        # ==========================
        # AI Tool Router
        # ==========================

        try:

            decision = route_request(text)

        except Exception as error:

            print(f"\nRouter error: {error}")

            decision = {
                "action": "NORMAL"
            }

        # ==========================
        # Tool request
        # ==========================

        if decision.get("action") == "TOOL":

            response = handle_tool_request(
                text,
                decision,
                brain
            )

        # ==========================
        # Normal conversation
        # ==========================

        else:

            response = brain.chat(text)

        # ==========================
        # Speak response
        # ==========================

        if response:

            print(f"\nAI: {response}")

            speak(response)

        else:

            print(
                "\nAI: I couldn't generate a response."
            )


if __name__ == "__main__":
    main()