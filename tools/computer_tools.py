import time
import pyautogui


def move_mouse(x, y):

    pyautogui.moveTo(
        int(x),
        int(y),
        duration=0.2
    )

    return f"Moved mouse to ({x}, {y})."


def click_mouse(button="left"):

    if button not in ["left", "right", "middle"]:
        return f"Unsupported mouse button: {button}"

    pyautogui.click(
        button=button
    )

    return f"Clicked {button} mouse button."


def type_text(text):

    # Give newly opened applications time
    # to receive keyboard focus.
    time.sleep(1)

    pyautogui.write(
        str(text),
        interval=0.02
    )

    return "Text typed successfully."


def press_key(key):

    time.sleep(0.2)

    pyautogui.press(
        str(key)
    )

    return f"Pressed {key}."