import ollama
import mss
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

IMAGE_PATH = (
    PROJECT_ROOT
    / "phase-03-vision"
    / "screen_current.png"
)

VISION_MODEL = "llava:7b"


def capture_screen():

    with mss.MSS() as screen:

        monitor = screen.monitors[1]

        screenshot = screen.grab(monitor)

        mss.tools.to_png(
            screenshot.rgb,
            screenshot.size,
            output=str(IMAGE_PATH)
        )


def get_screen_context(question):

    capture_screen()

    response = ollama.chat(
        model=VISION_MODEL,
        messages=[
            {
                "role": "user",
                "content": (
                    "Analyze the screenshot carefully. "
                    "Answer the user's question using only "
                    "information visible on the screen.\n\n"
                    f"User question: {question}"
                ),
                "images": [str(IMAGE_PATH)]
            }
        ]
    )

    return response["message"]["content"]