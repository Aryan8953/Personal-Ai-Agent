import mss
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

OUTPUT_PATH = (
    PROJECT_ROOT
    / "phase-03-vision"
    / "screen_test.png"
)


def capture_screen():

    with mss.mss() as screen:

        monitor = screen.monitors[1]

        screenshot = screen.grab(monitor)

        mss.tools.to_png(
            screenshot.rgb,
            screenshot.size,
            output=str(OUTPUT_PATH)
        )

    print(f"Screenshot saved to: {OUTPUT_PATH}")


if __name__ == "__main__":

    capture_screen()