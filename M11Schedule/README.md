# M11 Schedule

## The "Why?"

Almost every business depends on something running on time, without a human pushing a button. A bank closes the books at midnight. An e-commerce site emails a "your cart is waiting" reminder 24 hours after a customer abandons checkout. A monitoring system pings the production server every 30 seconds to confirm it is still alive. A weather app fetches new data every 10 minutes so its forecast stays fresh. In each case, *time itself* is part of the program's logic.

Up to this point, your scripts have followed the same shape: you press run, they do their work, and they exit. In this module, you will learn how to write Python programs that **stay alive** and act on a schedule—reacting to the clock instead of waiting for you. Combined with what you have already learned (M09 to fetch live data, M10 to persist it, M08 to export reports), scheduling is the final ingredient that turns one-off scripts into the kind of long-running automations that real teams rely on.

## Goals

By the end of this module, you should be able to:

* Explain the difference between a "one-shot" script and a "long-running" scheduled script.
* Use `time.sleep()` to build a basic interval loop.
* Install and use the `schedule` library to express human-readable timing rules (every minute, every Monday, every day at 09:30, etc.).
* Structure a scheduled program around the `schedule.run_pending()` + `time.sleep()` loop pattern.
* Gracefully stop a long-running script with `KeyboardInterrupt` handling.
* Combine scheduling with M09 (`requests`) and M10 (`sqlite3`) to build practical automations.
* Recognize the limits of in-process schedulers and know when an OS-level scheduler (cron, Task Scheduler) is more appropriate.

## Core Concepts

### From One-Shot to Long-Running Scripts

Most of the scripts you have written so far follow a "linear" flow: import, do something, exit. A scheduled program is structurally different—it never voluntarily exits. It sits in a loop, periodically waking up to check whether any of its registered jobs are due, running them when they are, and then going back to sleep.

This shape introduces new concerns you haven't faced before:

* **CPU usage**: A tight `while True:` loop with no sleep will pin one CPU core at 100%. You must yield with `time.sleep()`.
* **Crashes and recovery**: A job that throws an unhandled exception can take down the entire scheduler. Each job should defend itself with `try/except`.
* **Graceful shutdown**: The user needs a way to stop the program. The standard convention is to catch `KeyboardInterrupt` (raised when the user presses Ctrl+C) and exit cleanly.

---

### `time.sleep()`: The Simplest Possible Scheduler

Python's built-in `time.sleep(seconds)` pauses the script for the given duration. With a `while True` loop, you have everything you need for the simplest possible scheduler:

```python
import time

while True:
    print("Doing work...")
    time.sleep(60)   # Wait one minute, then do it again
```

This works for "every N seconds" tasks, but it has limits: you can't easily say "every Monday at 8 AM," and if your work itself takes 15 seconds, your *actual* interval becomes 75 seconds, not 60. For anything beyond a simple heartbeat, you want a real scheduling library.

---

### The `schedule` Library: Human-Readable Timing Rules

The third-party `schedule` package lets you describe *when* a function should run in English-like syntax, then takes care of figuring out *when next* to call it.

Install once:

```bash
pip install schedule
```

Define jobs using its fluent API:

```python
import schedule

def fetch_prices():
    print("Fetching latest prices...")

def send_morning_report():
    print("Sending the morning email...")

schedule.every(10).minutes.do(fetch_prices)
schedule.every().day.at("09:00").do(send_morning_report)
schedule.every().monday.at("17:30").do(send_morning_report)
```

Calling `.do(some_function)` *registers* the job but does not run it. You still need a loop that periodically asks the scheduler whether anything is due:

```python
import time

while True:
    schedule.run_pending()   # Run every job that is due right now
    time.sleep(1)            # Wait a second before checking again
```

The `time.sleep(1)` is the heartbeat—a balance between responsiveness (jobs running close to their target time) and CPU friendliness (the script not spinning needlessly).

---

### Passing Arguments to Scheduled Jobs

A scheduled function often needs context: which user to email, which file to back up, which URL to ping. `schedule` lets you forward arguments through `.do()`:

```python
def check_site(url):
    print(f"Checking {url}...")

schedule.every(60).seconds.do(check_site, url="https://example.com")
schedule.every(60).seconds.do(check_site, url="https://my-blog.dev")
```

The keyword arguments after the function are passed through every time the job fires.

---

### Defensive Jobs: Don't Let One Failure Kill the Whole Scheduler

If a scheduled job raises an unhandled exception, `schedule` will let it propagate, which can crash your loop. In any real automation, wrap the *body* of each job in a `try/except`:

```python
def fetch_weather():
    try:
        # ... network call that might fail ...
        pass
    except Exception as e:
        print(f"[weather] failed: {e}")   # Log it, but don't crash the scheduler
```

This is the same instinct you learned in M06 (Error Handling) and M09 (`raise_for_status`), applied here to keep long-running programs alive across transient failures.

---

### Graceful Shutdown

When the user presses Ctrl+C, Python raises a `KeyboardInterrupt` exception. Catch it at the top of your loop to print a friendly message and clean up:

```python
try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print("\nScheduler stopped by user. Goodbye.")
```

---

### When NOT to Use an In-Process Scheduler

The `schedule` library only runs while your Python program is running. If you close the terminal, restart your computer, or the script crashes, no jobs will fire. For tasks that absolutely must run regardless of whether your script is open (nightly backups, weekly reports), an **operating-system level scheduler** is the right tool:

* **Linux / macOS**: `cron`
* **Windows**: Task Scheduler

These call your Python script for you on a schedule, so the script itself can be a simple one-shot program. Knowing when to reach for which tool is part of growing as a developer.

---

## Guided Practice

We will build a **website health monitor**—the same pattern that powers commercial uptime services like UptimeRobot. The script pings a list of URLs on a schedule and shouts loudly when one is down. It exercises every concept above: the `schedule` library, defensive `try/except` wrappers, and graceful Ctrl+C shutdown.

**Scenario**: You run a small blog and a personal portfolio site. You want to know *immediately* if either of them goes down—without manually visiting them.

**Step 1: Define a defensive `check_site(url)` function.** Inside a `try/except`, call `requests.get(url, timeout=5)`. Print `[OK]` on a 200 response, `[WARN]` on any other status code, and `[ALERT]` on `Timeout`, `ConnectionError`, or any other `RequestException`. Catch everything—if one URL throws an unhandled error, the whole scheduler dies.

**Step 2: Register one job per URL.** Use the same function but pass the URL as a keyword argument so each scheduled job is independent:

```python
schedule.every(30).seconds.do(check_site, url="https://example.com")
schedule.every(30).seconds.do(check_site, url="https://www.python.org")
```

**Step 3: Run the main loop.** A `while True` that calls `schedule.run_pending()` and then `time.sleep(1)`—the sleep prevents the loop from pinning your CPU at 100%. Wrap the loop in `try/except KeyboardInterrupt` so pressing Ctrl+C exits cleanly with a goodbye message instead of an ugly traceback.

**Step 4: Test the failure path.** While the script runs, briefly disconnect your Wi-Fi. You should see `[ALERT]` lines appear, and when the network comes back, `[OK]` lines should resume without you restarting the script. That is the practical payoff of defensive error handling.

The full implementation is in `website_monitor_example.py`. The third URL in the file is deliberately a non-existent domain so you can see the alert path on the very first run.

---

## Checkpoints

* [ ] **Pomodoro Timer Coach**:
      You want to use the [Pomodoro technique](https://en.wikipedia.org/wiki/Pomodoro_Technique)—25 minutes of focused work followed by a 5-minute break, repeated four times, then a longer 15-minute rest. Build a script that prints a clear notification to the terminal at each transition (`"Focus time! 25 minutes starting now."` / `"Take a 5-minute break."`).
      Requirements:
      1. Use **seconds** instead of minutes during development so you can actually test the cycle (e.g., 25 seconds for "focus", 5 seconds for "break"). Then switch to real minutes once it works.
      2. Loop through the full four-pomodoro cycle and then exit naturally with a "Session complete, great job!" message.
      *(Hint: this is a sequential timer, not an interval scheduler—`time.sleep()` is actually a better fit here than the `schedule` library. Use this as practice for recognizing when each tool is appropriate.)*

* [ ] **Auto Currency Snapshot to Database**:
      Combine M09 + M10 + M11. Every 60 seconds, your script should:
      1. Fetch the latest USD-to-EUR exchange rate from `https://api.frankfurter.app/latest?from=USD&to=EUR`.
      2. Insert the rate into a SQLite table `rate_history(id, fetched_at, rate)`.
      3. Print the value it just stored.
      4. Keep running until the user presses Ctrl+C, at which point it should print how many rows were collected during this session.
      This is exactly the architecture a hobby trading dashboard or a personal finance tracker would use. The 60-second interval makes it safe to leave running while you work on other things.

* [ ] **Smart Morning Briefing**:
      You want a personal "morning briefing" that runs every weekday at 07:30 and writes a short report to `briefing.txt`. The report should include:
      1. Today's date and weekday name.
      2. The current weather forecast for your city (fetch from any free API—`https://goweather.xyz/weather/Taipei` works without a key).
      3. A motivational quote (fetch from `https://api.quotable.io/random`).
      Requirements:
      * Schedule it only for weekdays using `schedule.every().monday.at("07:30").do(...)` etc. (or look up how to use a single rule for all weekdays).
      * Wrap each API call in its own `try/except`. If the weather API fails, the briefing should still be generated with the parts that succeeded—don't let one failed call ruin the report.
      * For testing, temporarily change the schedule to every 30 seconds, confirm the output, then switch back.
      *(Hint: think about what you would do if you were sick and could only check email once a day—how much would you trust a script that has been doing this silently for weeks? That trust is built by defensive error handling.)*
