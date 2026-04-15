# M11 Schedule

## The "Why?"

The real power of programming lies in making the computer work for you while you are away. Instead of manually running a script to fetch data, back up files, or send a report, you can "schedule" it to run automatically at specific intervals—every 10 seconds, every hour, or at 3:00 AM every day. This is the foundation of automation, allowing systems to maintain themselves and perform repetitive tasks without human intervention.

## Goals

Learn how to use timing loops and third-party scheduling libraries to execute Python functions at precise intervals or specific times of the day.

## Core Concepts

### `time.sleep()`
The simplest way to schedule is to put a script in an infinite loop and tell it to "wait" for a certain number of seconds before continuing. This is great for very simple intervals.

### The `schedule` Library
For more complex timing (like "every Monday at 8 AM" or "every 10 minutes"), we use the `schedule` package. It uses a very readable, "human-like" syntax to define when tasks should happen.

```python
import schedule
import time

def job():
    print("Doing work...")

schedule.every(10).minutes.do(job)
schedule.every().day.at("10:30").do(job)
```

## Guided Practice

Let's build a **Health Reminder** bot. It will remind you to "Stand up and stretch!" every 5 seconds. We use seconds for quick testing, but in a real scenario, you would set this to 30 or 60 minutes.

*   **Step 1: Install the `schedule` library**
    ```bash
    pip install schedule
    ```

*   **Step 2: Create `health_reminder_example.py`**
    ```python
    import schedule
    import time
    from datetime import datetime

    def remind_stretch():
        # Get current time for the log
        now = datetime.now().strftime("%H:%M:%S")
        print(f"[{now}] Time to stand up and stretch!")

    # 1. Schedule the job to run every 5 seconds
    schedule.every(5).seconds.do(remind_stretch)

    print("--- Health Reminder Bot Started ---")
    print("Press Ctrl+C to stop the script.")

    # 2. Keep the script running in a loop
    try:
        while True:
            # Check if any scheduled task is ready to run
            schedule.run_pending()
            # Wait a short time before checking again to save CPU power
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping the reminder bot. Stay healthy!")
    ```

## Checkpoints

* [ ] **Log File Heartbeat**:
    Write a task that appends the current timestamp to a file named `heartbeat.log` every 10 seconds.
* [ ] **The Multi-Tasker**:
    Create two different functions: `task_a` which runs every 3 seconds, and `task_b` which runs every 7 seconds. Run them both simultaneously in the same script using one scheduler loop.
* [ ] **Website Monitor**:
    Combine this with M09 (Requests). Create a script that checks if a specific website is online every 60 seconds. If the site is down, print a warning to the console.