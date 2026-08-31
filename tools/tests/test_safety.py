import sys
from pathlib import Path

TOOLS_PATH = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(TOOLS_PATH))

from tool_executor import execute_tool


print("Test 1: Valid tool")

print(
    execute_tool(
        "press_key",
        {
            "key": "enter"
        }
    )
)

print()

print("Test 2: Invalid tool")

print(
    execute_tool(
        "delete_everything",
        {}
    )
)

print()

print("Test 3: Invalid mouse coordinates")

print(
    execute_tool(
        "move_mouse",
        {
            "x": -100,
            "y": 200
        }
    )
)