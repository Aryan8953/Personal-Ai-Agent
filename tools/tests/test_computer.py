import sys
import time
from pathlib import Path

TOOLS_PATH = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS_PATH))

from computer_tools import type_text, press_key


print("Open Notepad manually.")
print("You have 5 seconds...")

time.sleep(5)

print(type_text("Hello from my Personal AI Agent!"))

print(press_key("enter"))

print(type_text("Computer control is working."))