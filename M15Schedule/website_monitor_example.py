"""Guided Practice 2 — A tiny uptime monitor.

Scenario: ping a list of personal sites every 30 seconds and shout
loudly when one of them is down. The same idea powers paid services
like UptimeRobot, but the core is 20 lines.
"""

import time
from datetime import datetime

import requests
import schedule

# Sites to keep an eye on. Add or remove as needed.
SITES = [
    "https://example.com",
    "https://www.python.org",
    "https://this-site-definitely-does-not-exist-12345.dev",  # designed to fail
]


def check_site(url: str) -> None:
    """One request, three possible outcomes, no exceptions allowed to escape."""
    now = datetime.now().strftime("%H:%M:%S")
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"[{now}] [OK]    {url}")
        else:
            print(f"[{now}] [WARN]  {url} returned {response.status_code}")
    except requests.exceptions.Timeout:
        print(f"[{now}] [ALERT] {url} timed out")
    except requests.exceptions.ConnectionError:
        print(f"[{now}] [ALERT] {url} could not be reached")
    except requests.exceptions.RequestException as err:
        print(f"[{now}] [ALERT] {url} failed: {err}")


# Register one job per site. Passing `url=...` keeps each call independent.
for site in SITES:
    schedule.every(30).seconds.do(check_site, url=site)

# Run every site once at start-up so we have an immediate baseline.
print("--- Website monitor started (Ctrl+C to stop) ---")
for site in SITES:
    check_site(site)

try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print("\nMonitor stopped.")
