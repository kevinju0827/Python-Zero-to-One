import pyautogui
import time

# PyAutoGUI Safety Settings
# 1. Fail-Safe: Move mouse to any corner to abort the script
pyautogui.FAILSAFE = True

# 2. Add a pause between all PyAutoGUI commands to slow things down slightly
pyautogui.PAUSE = 0.5

print("--- Desktop Automation: Ghost Writer ---")
print("Important: You have 5 seconds to open a text editor (Notepad, etc.) and click inside it.")
print("To STOP the script at any time, move your mouse to the corner of the screen.")

# Countdown
for i in range(5, 0, -1):
    print(f"Starting in {i}...")
    time.sleep(1)

# Action 1: Type a header
pyautogui.write("### Python Automation Log ###", interval=0.1)
pyautogui.press('enter')

# Action 2: Type some body text
content = [
    "This script is controlling the keyboard.",
    "PyAutoGUI allows you to simulate human interactions.",
    "Perfect for repetitive tasks in legacy software."
]

for line in content:
    pyautogui.write(line, interval=0.05)
    pyautogui.press('enter')

# Action 3: Final message
pyautogui.write("Automation complete at " + time.strftime("%H:%M:%S"), interval=0.1)
pyautogui.press('enter')

print("Automation finished successfully.")
