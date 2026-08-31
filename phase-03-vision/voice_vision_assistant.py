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
# Tool → AI response
# ==============================

def process_tool_result(
    user_input,
    tool_name,
    result,
    brain
):

    # Vision result
    if tool_name == "inspect_screen":

        prompt = f"""
The user asked:

{user_input}

Information obtained from the user's screen:

{result}

Answer naturally and directly.

Do not mention internal tools, screenshots,
or model names unless the user asks.
"""

        return brain.chat(prompt)

    # Web result
    if tool_name == "search_web":

        prompt = f"""
The user asked:

{user_input}

Internet search results:

{result}

Answer naturally and accurately.

Rules:

- Use the search results for current information.
- Do not invent unsupported facts.
- If the results are insufficient, say so.
- Do not mention internal tools unless asked.
"""

        return brain.chat(prompt)

    # Computer/system tools
    return result


# ==============================
# Main assistant
# ==============================

def main():

    brain = AIBrain()

    print("================================")
    print("     Personal AI Assistant")
    print("================================")
    print("Voice + AI + Vision + Web + Tools")
    print("Say 'exit' to stop.\n")

    while True:

        text = listen()

        if not text:
            continue

        print(f"\nYou: {text}")

        if text.lower().strip() == "exit":

            print("Goodbye!")

            break

        # ==========================
        # AI decides what to do
        # ==========================

        try:

            decision = route_request(text)

            print(
                f"\n🧠 Decision: {decision}"
            )

        except Exception as error:

            print(
                f"\n❌ Router error: {error}"
            )

            decision = {
                "action": "NORMAL"
            }

        # ==========================
        # NORMAL
        # ==========================

        if decision.get("action") == "NORMAL":

            response = brain.chat(text)

        # ==========================
        # TOOL
        # ==========================

        else:

            tool_name = decision.get("tool")

            arguments = decision.get(
                "arguments",
                {}
            )

            print(
                f"🛠️ Tool: {tool_name}"
            )

            print(
                f"📦 Arguments: {arguments}"
            )

            result = execute_tool(
                tool_name,
                arguments
            )

            print(
                f"\n💻 Tool result:\n{result}"
            )

            response = process_tool_result(
                text,
                tool_name,
                result,
                brain
            )

        # ==========================
        # Response
        # ==========================

        if response:

            print(
                f"\nAI: {response}"
            )

            speak(response)

        else:

            print(
                "\nAI: I couldn't generate a response."
            )


if __name__ == "__main__":
    main()