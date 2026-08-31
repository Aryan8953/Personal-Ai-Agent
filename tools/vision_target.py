import sys
import json
import ollama

from pathlib import Path


# ==============================
# Project paths
# ==============================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PHASE_03_PATH = PROJECT_ROOT / "phase-03-vision"

sys.path.insert(0, str(PHASE_03_PATH))


from screen_capture import capture_screen


# ==============================
# Vision model
# ==============================

VISION_MODEL = "llava:7b"


# ==============================
# Find target
# ==============================

def find_target(target):

    image_path = capture_screen()

    print(f"Screenshot: {image_path}")

    prompt = f"""
Look at this computer screenshot carefully.

Find this target:

{target}

Return ONLY valid JSON.

If the target is clearly visible:

{{
    "found": true,
    "target": "{target}",
    "x": 500,
    "y": 400
}}

The x and y values must represent the approximate
CENTER of the target in the screenshot.

If the target cannot be clearly identified:

{{
    "found": false,
    "target": "{target}",
    "x": null,
    "y": null
}}

Do NOT guess coordinates.
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

    result = response["message"]["content"].strip()

    print("\nVision response:")
    print(result)

    try:

        return json.loads(result)

    except json.JSONDecodeError:

        return {
            "found": False,
            "target": target,
            "x": None,
            "y": None
        }


# ==============================
# Test
# ==============================

if __name__ == "__main__":

    target = input("What should I find? ").strip()

    result = find_target(target)

    print("\nParsed result:")

    print(
        json.dumps(
            result,
            indent=2
        )
    )