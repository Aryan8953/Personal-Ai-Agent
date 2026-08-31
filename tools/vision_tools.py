import sys
from pathlib import Path

import ollama
import pyautogui


# ==============================
# Paths
# ==============================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PHASE_03_PATH = PROJECT_ROOT / "phase-03-vision"

sys.path.insert(0, str(PHASE_03_PATH))

from screen_capture import capture_screen


# ==============================
# Configuration
# ==============================

VISION_MODEL = "llava:7b"


# ==============================
# Screen inspection
# ==============================

def inspect_screen(question):

    image_path = capture_screen()

    prompt = f"""
You are a desktop vision assistant.

Look carefully at the provided screenshot.

Answer this question:

{question}

Rules:

- Describe only what is actually visible.
- Do not invent information.
- If something cannot be determined, say so.
- Be concise.
- If the question asks for an application, identify the application if its interface is visible.
- If the question asks about a file, only name it if it is clearly visible.
"""

    response = ollama.chat(
        model=VISION_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
                "images": [str(image_path)]
            }
        ]
    )

    return response["message"]["content"].strip()


# ==============================
# Mouse
# ==============================

def click_at(x, y):

    screen_width, screen_height = pyautogui.size()

    x = int(x)
    y = int(y)

    if x < 0 or y < 0:
        return "Click blocked: negative coordinates."

    if x >= screen_width or y >= screen_height:
        return "Click blocked: coordinates outside the screen."

    pyautogui.click(x, y)

    return f"Clicked at ({x}, {y})."


# ==============================
# Test
# ==============================

if __name__ == "__main__":

    question = input(
        "What do you want me to see? "
    ).strip()

    print("\n👁️ Looking at your screen...\n")

    answer = inspect_screen(question)

    print(answer)