import re


# ==========================================
# Known websites
# ==========================================

WEBSITES = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "github": "https://github.com",
}


# ==========================================
# Helpers
# ==========================================

def create_open_action(target):

    target = target.strip()

    if target.lower() in WEBSITES:

        return {
            "tool": "open_website",
            "arguments": {
                "url": WEBSITES[
                    target.lower()
                ]
            }
        }

    return {
        "tool": "launch_application",
        "arguments": {
            "application": target
        }
    }


def create_type_action(text):

    return {
        "tool": "type_text",
        "arguments": {
            "text": text.strip()
        }
    }


def create_press_action(key):

    return {
        "tool": "press_key",
        "arguments": {
            "key": key.strip()
        }
    }


# ==========================================
# Main parser
# ==========================================

def parse_command(user_input):

    text = user_input.strip()

    if not text:
        return None

    # Normalize whitespace
    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()


    # ======================================
    # OPEN + TYPE + PRESS
    # ======================================

    match = re.match(
        r"^open\s+(.+?)\s+and\s+(?:type|write)\s+(.+?)\s+and\s+press\s+(.+)$",
        text,
        re.IGNORECASE
    )

    if match:

        target = match.group(1)
        typed_text = match.group(2)
        key = match.group(3)

        return [
            create_open_action(target),
            create_type_action(typed_text),
            create_press_action(key)
        ]


    # ======================================
    # OPEN + TYPE
    # ======================================

    match = re.match(
        r"^open\s+(.+?)\s+and\s+(?:type|write)\s+(.+)$",
        text,
        re.IGNORECASE
    )

    if match:

        target = match.group(1)
        typed_text = match.group(2)

        return [
            create_open_action(target),
            create_type_action(typed_text)
        ]


    # ======================================
    # OPEN + PRESS
    # ======================================

    match = re.match(
        r"^open\s+(.+?)\s+and\s+press\s+(.+)$",
        text,
        re.IGNORECASE
    )

    if match:

        target = match.group(1)
        key = match.group(2)

        return [
            create_open_action(target),
            create_press_action(key)
        ]


    # ======================================
    # OPEN ONLY
    # ======================================

    match = re.match(
        r"^open\s+(.+)$",
        text,
        re.IGNORECASE
    )

    if match:

        target = match.group(1)

        return [
            create_open_action(target)
        ]


    # ======================================
    # TYPE / WRITE ONLY
    # ======================================

    match = re.match(
        r"^(?:type|write)\s+(.+)$",
        text,
        re.IGNORECASE
    )

    if match:

        return [
            create_type_action(
                match.group(1)
            )
        ]


    # ======================================
    # PRESS ONLY
    # ======================================

    match = re.match(
        r"^press\s+(.+)$",
        text,
        re.IGNORECASE
    )

    if match:

        return [
            create_press_action(
                match.group(1)
            )
        ]


    # ======================================
    # Not understood
    # ======================================

    return None


# ==========================================
# Parser tests
# ==========================================

if __name__ == "__main__":

    tests = [

        "open notepad",

        "open calculator",

        "open google",

        "open youtube",

        "open github",

        "open notepad and type hello",

        "open notepad and type hello and press enter",

        "open notepad and press enter",

        "type Personal AI Agent",

        "write Hello World",

        "press enter",

        "what is Python?",

        "tell me about artificial intelligence",

    ]


    for test in tests:

        print(
            "\n================================"
        )

        print(
            "Input:"
        )

        print(test)

        print(
            "\nParsed:"
        )

        result = parse_command(test)

        print(result)