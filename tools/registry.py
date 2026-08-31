from vision_tools import inspect_screen, click_at

from system_tools import (
    launch_application,
    open_website
)

from computer_tools import (
    move_mouse,
    click_mouse,
    type_text,
    press_key
)


TOOLS = {

    "launch_application": launch_application,

    "open_website": open_website,

    "move_mouse": move_mouse,

    "click_mouse": click_mouse,

    "type_text": type_text,

    "press_key": press_key,

    "inspect_screen": inspect_screen,

    "click_at": click_at,

}


TOOL_DESCRIPTIONS = {

    "launch_application": {
        "description": "Launch a permitted Windows application.",
        "arguments": {
            "application": "Application name"
        }
    },

    "open_website": {
        "description": "Open a website in the default browser.",
        "arguments": {
            "url": "Website URL"
        }
    },

    "move_mouse": {
        "description": "Move the mouse to a screen coordinate.",
        "arguments": {
            "x": "Horizontal screen coordinate",
            "y": "Vertical screen coordinate"
        }
    },

    "click_mouse": {
        "description": "Click the mouse.",
        "arguments": {
            "button": "left, right, or middle"
        }
    },

    "type_text": {
        "description": "Type text using the keyboard.",
        "arguments": {
            "text": "Text to type"
        }
    },

    "press_key": {
        "description": "Press a keyboard key.",
        "arguments": {
            "key": "Key name such as enter, esc, or tab"
        }
    },

    "inspect_screen": {
        "description": "Capture and inspect the current computer screen.",
        "arguments": {
            "question": "What you want to know about the screen"
        }
    },

    "click_at": {
        "description": "Click at a specific screen coordinate.",
        "arguments": {
            "x": "Horizontal screen coordinate",
            "y": "Vertical screen coordinate"
        }
    }

}


def get_tool(name):
    return TOOLS.get(name)


def list_tools():
    return list(TOOLS.keys())


def get_tool_descriptions():
    return TOOL_DESCRIPTIONS