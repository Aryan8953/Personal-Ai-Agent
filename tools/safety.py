ALLOWED_TOOLS = {
    "launch_application",
    "open_website",
    "move_mouse",
    "click_mouse",
    "type_text",
    "press_key",
    "inspect_screen",
}


def validate_tool_call(tool_name, arguments):

    if tool_name not in ALLOWED_TOOLS:
        return False, f"Tool '{tool_name}' is not allowed."

    if not isinstance(arguments, dict):
        return False, "Tool arguments must be a dictionary."

    # Mouse coordinate validation
    if tool_name == "move_mouse":

        if "x" not in arguments or "y" not in arguments:
            return False, "Mouse movement requires x and y."

        try:
            x = int(arguments["x"])
            y = int(arguments["y"])
        except (TypeError, ValueError):
            return False, "Mouse coordinates must be numbers."

        if x < 0 or y < 0:
            return False, "Mouse coordinates cannot be negative."

    # Mouse button validation
    if tool_name == "click_mouse":

        button = arguments.get("button", "left")

        if button not in {"left", "right", "middle"}:
            return False, "Unsupported mouse button."

    # Text validation
    if tool_name == "type_text":

        if "text" not in arguments:
            return False, "Text is required."

        if not isinstance(arguments["text"], str):
            return False, "Text must be a string."

        if len(arguments["text"]) > 1000:
            return False, "Text is too long."

    # Keyboard validation
    if tool_name == "press_key":

        if "key" not in arguments:
            return False, "Key is required."

    return True, "Tool call approved."

    if tool_name == "click_at":
        if "x" not in arguments or "y" not in arguments:
            return False, "Click requires x and y."

        try:
            x = int(arguments["x"])
            y = int(arguments["y"])
        except (TypeError, ValueError):
            return False, "Click coordinates must be numbers."

        if x < 0 or y < 0:
            return False, "Click coordinates cannot be negative."