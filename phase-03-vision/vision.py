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


def analyze_screen(question):

    capture_screen()

    response = ollama.chat(
        model=VISION_MODEL,
        messages=[
            {
                "role": "user",
                "content": question,
                "images": [str(IMAGE_PATH)]
            }
        ]
    )

    return response["message"]["content"]


if __name__ == "__main__":

    question = input(
        "What do you want me to see? "
    )

    print("\nCapturing screen...")

    answer = analyze_screen(question)

    print("\nVision AI:")
    print(answer)