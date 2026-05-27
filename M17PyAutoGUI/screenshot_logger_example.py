"""Guided Practice 3 — Capture a timestamped screenshot every N seconds.

Scenario: debugging an issue that only happens 'sometimes during the
day'. Quietly snapshot the screen so when the next bug report comes
in, there's visual evidence of what was on the screen at the time.
"""

import os
import time
from datetime import datetime

import pyautogui
import schedule

os.chdir(os.path.dirname(os.path.abspath(__file__)))

pyautogui.FAILSAFE = True

OUTPUT_DIR = "screenshots"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def capture_now() -> None:
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = os.path.join(OUTPUT_DIR, f"{stamp}.png")
    try:
        pyautogui.screenshot(path)
        print(f"[{stamp}] saved {path}")
    except Exception as err:
        # Don't crash the scheduler over a transient screen-access issue.
        print(f"[{stamp}] screenshot failed: {err}")


# Snap immediately so the user gets visible feedback that the script runs.
capture_now()
# In real use you'd change this to every 5 minutes. 10s makes testing fast.
schedule.every(10).seconds.do(capture_now)

print("--- Screenshot logger started (Ctrl+C to stop) ---")
try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print("\nLogger stopped.")
