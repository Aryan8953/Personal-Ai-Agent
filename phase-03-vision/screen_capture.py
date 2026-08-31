import mss
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

OUTPUT_PATH = (
    PROJECT_ROOT
    / "phase-03-vision"
    / "screen_current.png"
)


def capture_screen():

    print("Capturing screen...")

    with mss.MSS() as screen:

        monitor = screen.monitors[1]

        screenshot = screen.grab(monitor)

        mss.tools.to_png(
            screenshot.rgb,
            screenshot.size,
            output=str(OUTPUT_PATH)
        )

    return OUTPUT_PATH