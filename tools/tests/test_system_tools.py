import sys
from pathlib import Path

TOOLS_PATH = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS_PATH))

from system_tools import launch_application


print("Testing system tools...")
print()

result = launch_application("notepad")

print(result)