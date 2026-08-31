import sys
from pathlib import Path

TOOLS_PATH = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(TOOLS_PATH))

from registry import list_tools, get_tool


print("Available tools:")
print(list_tools())

print()

tool = get_tool("launch_application")

if tool:

    print(tool("calculator"))

else:

    print("Tool not found.")