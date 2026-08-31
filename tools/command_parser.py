import re


WEBSITES = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "github": "https://github.com",
}


def parse_command(user_input):

    text = user_input.strip()

    if not text:
        return None

    actions = []

    # ==========================================
    # Normalize spaces
    # ==========================================

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    # ==========================================
    # OPEN + TYPE + PRESS
    # ==========================================

    match = re.match(
        r"^open\s+(.+?)\s+and\s+(?:type|write)\s+(.+?)\s+and\s+press\s+(.+)$",
        text,
        re.IGNORECASE
    )

    if match:

        target = match.group(1).strip()
        typed_text = match.group(2).strip()
        key = match.group(3).strip()

        # Open application or website
        if target.lower() in WEBSITES:

            actions.append({
                "tool": "open_website",
                "arguments": {
                    "url": WEBSITES[target.lower()]
                }
            })

        else:

            actions.append({
                "tool": "launch_application",
                "arguments": {
                    "application": target
                }
            })

        # Type
        actions.append({
            "tool": "type_text",
            "arguments": {
                "text": typed_text
            }
        })

        # Press
        actions.append({
            "tool": "press_key",
            "arguments": {
                "key": key
            }
        })

        return actions

    # ==========================================
    # OPEN + TYPE / WRITE
    # ==========================================

    match = re.match(
        r"^open\s+(.+?)\s+and\s+(?:type|write)\s+(.+)$",
        text,
        re.IGNORECASE
    )

    if match:

        target = match.group(1).strip()
        typed_text = match.group(2).strip()

        # Open application or website
        if target.lower() in WEBSITES:

            actions.append({
                "tool": "open_website",
                "arguments": {
                    "url": WEBSITES[target.lower()]
                }
            })

        else:

            actions.append({
                "tool": "launch_application",
                "arguments": {
                    "application": target
                }
            })

        # Type
        actions.append({
            "tool": "type_text",
            "arguments": {
                "text": typed_text
            }
        })

        return actions

    # ==========================================
    # OPEN + PRESS
    # ==========================================

    match = re.match(
        r"^open\s+(.+?)\s+and\s+press\s+(.+)$",
        text,
        re.IGNORECASE
    )

    if match:

        target = match.group(1).strip()
        key = match.group(2).strip()

        if target.lower() in WEBSITES:

            actions.append({
                "tool": "open_website",
                "arguments": {
                    "url": WEBSITES[target.lower()]
                }
            })

        else:

            actions.append({
                "tool": "launch_application",
                "arguments": {
                    "application": target
                }
            })

        actions.append({
            "tool": "press_key",
            "arguments": {
                "key": key
            }
        })

        return actions

    # ==========================================
    # OPEN ONLY
    # ==========================================

    match = re.match(
        r"^open\s+(.+)$",
        text,
        re.IGNORECASE
    )

    if match:

        target = match.group(1).strip()

        if target.lower() in WEBSITES:

            return [{
                "tool": "open_website",
                "arguments": {
                    "url": WEBSITES[target.lower()]
                }
            }]

        return [{
            "tool": "launch_application",
            "arguments": {
                "application": target
            }
        }]

    # ==========================================
    # TYPE / WRITE ONLY
    # ==========================================

    match = re.match(
        r"^(?:type|write)\s+(.+)$",
        text,
        re.IGNORECASE
    )

    if match:

        return [{
            "tool": "type_text",
            "arguments": {
                "text": match.group(1).strip()
            }
        }]

    # ==========================================
    # PRESS ONLY
    # ==========================================

    match = re.match(
        r"^press\s+(.+)$",
        text,
        re.IGNORECASE
    )

    if match:

        return [{
            "tool": "press_key",
            "arguments": {
                "key": match.group(1).strip()
            }
        }]

    return None


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    tests = [

        "open notepad",

        "open notepad and type hello",

        "open notepad and type hello and press enter",

        "type Personal AI Agent",

        "press enter",

        "open google",

        "open youtube",

        "open github",

    ]

    for test in tests:

        print("\n================================")

        print("Input:")
        print(test)

        print("\nParsed:")

        print(
            parse_command(test)
        )