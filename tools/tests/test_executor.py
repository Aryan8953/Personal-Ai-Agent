import sys
from pathlib import Path

TOOLS_PATH = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(TOOLS_PATH))

from tool_executor import execute_tool


print("Testing structured tool execution...")
print()

result = execute_tool(
    "launch_application",
    {
        "application": "notepad"
    }
)

print(result)