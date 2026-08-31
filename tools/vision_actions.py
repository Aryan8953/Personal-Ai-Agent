import pyautogui

from vision_target import find_target
from safety import validate_tool_call


def locate_target(target):

    result = find_target(target)

    if not result.get("found"):
        return {
            "success": False,
            "message": f"Could not find '{target}'."
        }

    x = result.get("x")
    y = result.get("y")

    if x is None or y is None:
        return {
            "success": False,
            "message": "Vision returned invalid coordinates."
        }

    # Validate coordinates before doing anything
    allowed, message = validate_tool_call(
        "click_at",
        {
            "x": x,
            "y": y
        }
    )

    if not allowed:
        return {
            "success": False,
            "message": message
        }

    return {
        "success": True,
        "target": target,
        "x": int(x),
        "y": int(y)
    }


def click_target(target):

    result = locate_target(target)

    if not result["success"]:
        return result

    x = result["x"]
    y = result["y"]

    print()
    print(f"🎯 Target: {target}")
    print(f"📍 Coordinates: ({x}, {y})")

    confirmation = input(
        "Click this location? (yes/no): "
    ).strip().lower()

    if confirmation != "yes":
        return {
            "success": False,
            "message": "Click cancelled."
        }

    pyautogui.click(x, y)

    return {
        "success": True,
        "message": f"Clicked '{target}' at ({x}, {y})."
    }


if __name__ == "__main__":

    target = input(
        "What should I click? "
    ).strip()

    result = click_target(target)

    print()
    print(result)