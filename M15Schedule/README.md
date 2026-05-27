# M15 Scheduling

![Module 15 of 17](https://img.shields.io/badge/Module-15_of_17-6366f1?style=flat-square)
![Intermediate](https://img.shields.io/badge/Difficulty-Intermediate-facc15?style=flat-square)
![1.5 hours](https://img.shields.io/badge/Time-1.5_hours-60a5fa?style=flat-square)
![Prerequisites: M01–M14](https://img.shields.io/badge/Prerequisites-M01–M14-94a3b8?style=flat-square)

**Topics covered:** one-shot vs. long-running scripts · `time.sleep()` · `schedule` library · job registration · `run_pending()` loop · graceful Ctrl+C shutdown · OS-level schedulers

## The Why?

Every script you have built so far follows the same shape: it runs, does its work, and exits. You press Run; it finishes.

Real automation is different. A bank reconciles accounts at midnight without anyone pressing a button. An e-commerce site checks inventory levels every 10 minutes. A monitoring service pings your server every 30 seconds and alerts you the moment it goes down.

**Scheduling** is what turns one-off scripts into the kind of long-running automations that real teams rely on daily. Combined with everything you have already built — M11 to fetch live data, M12 to persist it, M10 to export reports — scheduling is the final piece that makes your programs act on time instead of waiting for you.

---

## Core Concepts

### One-Shot vs. Long-Running Scripts

```
One-shot:   run → do work → exit
Long-running: run → loop forever → wake up periodically → do work → sleep → repeat
```

Long-running scripts introduce concerns you have not faced before:

- **CPU usage:** a tight `while True:` loop with no sleep pins a CPU core at 100%. Always yield with `time.sleep()`.
- **Crash recovery:** an unhandled exception in a job can kill the entire scheduler. Wrap each job in `try/except`.
- **Graceful shutdown:** catch `KeyboardInterrupt` (Ctrl+C) so the program exits cleanly rather than printing a traceback.

---

### `time.sleep()` — The Simplest Scheduler

```python
import time

while True:
    print("Running job...")
    time.sleep(60)   # Pause for 60 seconds, then loop again
```

This works for "every N seconds" tasks but has limitations: you cannot easily say "every Monday at 8 AM", and if your job takes 15 seconds, the actual interval becomes 75, not 60. For anything beyond a simple heartbeat, use the `schedule` library.

---

### The `schedule` Library — Human-Readable Timing

```bash
pip install schedule
```

```python
import schedule
import time

def fetch_prices():
    print("Fetching latest prices...")

def send_report():
    print("Sending daily report...")

# Register jobs with human-readable rules
schedule.every(10).minutes.do(fetch_prices)
schedule.every().day.at("09:00").do(send_report)
schedule.every().monday.at("17:30").do(send_report)
```

`.do(function)` registers the job — it does NOT call it immediately.
You still need the main loop:

```python
try:
    while True:
        schedule.run_pending()   # Run any jobs that are due right now
        time.sleep(1)            # Heartbeat — check again in 1 second
except KeyboardInterrupt:
    print("\nScheduler stopped. Goodbye.")
```

The `time.sleep(1)` heartbeat balances responsiveness (jobs fire close to their scheduled time) with CPU friendliness (the loop does not spin constantly).

---

### Passing Arguments to Jobs

```python
def check_site(url):
    print(f"Checking {url}...")

schedule.every(30).seconds.do(check_site, url="https://example.com")
schedule.every(30).seconds.do(check_site, url="https://my-blog.dev")
```

Keyword arguments after the function are forwarded every time the job fires.

---

### Defensive Jobs — Don't Let One Failure Kill the Scheduler

```python
def fetch_weather():
    try:
        response = requests.get("https://weather.api/current", timeout=5)
        response.raise_for_status()
        print(f"Weather: {response.json()['description']}")
    except Exception as e:
        print(f"[weather] failed: {e}")   # Log it; don't crash the scheduler
```

This is the same defensive pattern from M08 (Error Handling) and M11 (requests), now applied to keep a long-running program alive through transient failures.

---

### When NOT to Use an In-Process Scheduler

The `schedule` library only runs while your Python program is running. Close the terminal or restart the machine, and no jobs fire.

For tasks that must run regardless of whether your script is open, use an **OS-level scheduler**:

| OS | Tool | Use case |
|----|------|---------|
| Linux / macOS | `cron` | `0 9 * * 1 python /path/to/script.py` |
| Windows | Task Scheduler | GUI or `schtasks` command |

With OS-level scheduling, Python scripts can be simple one-shot programs. The OS handles the "when."

---

## Going Further

<details>
<summary>Canceling a Job</summary>

```python
job = schedule.every(10).seconds.do(my_function)
schedule.cancel_job(job)   # Remove it from the scheduler
```

</details>

<details>
<summary>Run a Job Only Once</summary>

```python
def send_welcome_email():
    print("Sending welcome email...")
    return schedule.CancelJob   # Returning this cancels the job after it runs once

schedule.every(5).seconds.do(send_welcome_email)
```

</details>

<details>
<summary>Threading — Non-Blocking Jobs</summary>

If a job takes longer than the sleep interval, it will block the entire loop.
For long-running jobs, run them in a background thread:

```python
import threading

def long_job():
    time.sleep(30)   # Simulate slow work
    print("Done.")

def run_in_thread(job_func):
    thread = threading.Thread(target=job_func)
    thread.start()

schedule.every(10).seconds.do(run_in_thread, job_func=long_job)
```

</details>

<details>
<summary>Cron on macOS/Linux</summary>

Open a cron editor with `crontab -e`. This line runs `script.py` every day at 9 AM:

```
0 9 * * * /usr/bin/python3 /home/user/script.py
```

Format: `minute hour day-of-month month day-of-week command`

</details>

---

## Guided Practice

We will build a **website health monitor** — the same pattern used by commercial uptime services. The script pings a list of URLs on a schedule and alerts loudly if any are down.

**Scenario:** You run a small blog and a portfolio site. You want to know immediately if either goes down without manually refreshing them.

### Step 1 — Define a defensive `check_site()` function

Create `website_monitor_example.py`:

```python
import requests
import schedule
import time
from datetime import datetime

def check_site(url):
    timestamp = datetime.now().strftime("%H:%M:%S")
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"[{timestamp}] [OK]    {url}")
        else:
            print(f"[{timestamp}] [WARN]  {url} — HTTP {response.status_code}")
    except requests.exceptions.Timeout:
        print(f"[{timestamp}] [ALERT] {url} — Timed out")
    except requests.exceptions.ConnectionError:
        print(f"[{timestamp}] [ALERT] {url} — Connection failed")
    except requests.exceptions.RequestException as e:
        print(f"[{timestamp}] [ALERT] {url} — {e}")
```

### Step 2 — Register jobs

```python
schedule.every(30).seconds.do(check_site, url="https://www.python.org")
schedule.every(30).seconds.do(check_site, url="https://httpstat.us/200")
schedule.every(30).seconds.do(check_site, url="https://this-domain-does-not-exist-xyz.com")
```

The third URL is deliberately invalid — you will see `[ALERT]` on the very first run.

### Step 3 — Run the main loop

```python
print("Website monitor started. Press Ctrl+C to stop.\n")
check_site("https://www.python.org")   # Run once immediately on startup

try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print("\nMonitor stopped. Goodbye.")
```

### Step 4 — Test the failure path

While the script is running, temporarily disconnect your Wi-Fi.
You should see `[ALERT]` lines appear. Reconnect — `[OK]` resumes without restarting.
That is the practical payoff of defensive error handling in a long-running script.

---

## Checkpoints

* [ ] **Pomodoro Timer**
  Implement the [Pomodoro technique](https://en.wikipedia.org/wiki/Pomodoro_Technique): 25 minutes of focus, 5-minute break, × 4, then a 15-minute long break.
  Print a clear notification at each transition.
  Use **seconds** instead of minutes while testing (e.g., 25 seconds for "focus"), then switch to real minutes once it works.
  *(Hint: this is sequential timing, not interval scheduling — `time.sleep()` is the right tool here, not the `schedule` library. Recognizing which tool fits is part of the skill.)*

* [ ] **Auto Currency Snapshot to Database**
  Combine M11 + M12 + M15.
  Every 60 seconds, fetch the USD-to-EUR rate from `https://api.frankfurter.app/latest?from=USD&to=EUR`.
  Insert the rate and timestamp into a SQLite table `rate_history(id, fetched_at, rate)`.
  Print each value as it is stored.
  When the user presses Ctrl+C, print how many rows were collected this session.

* [ ] **Smart Morning Briefing File**
  Use `schedule` to run a job every weekday at 07:30 that writes a `briefing.txt` file containing:
  1. Today's date and day name.
  2. A weather summary (fetch from any key-free API).
  3. A random motivational quote from a local list you define.
  Wrap each API call in its own `try/except` so the file is always written even if one source fails.
  Test by temporarily scheduling every 30 seconds, then switch back to the real time.
