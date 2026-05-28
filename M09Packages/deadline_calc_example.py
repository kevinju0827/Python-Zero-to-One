from datetime import datetime
from dateutil.relativedelta import relativedelta

DEADLINE = "2026-12-31 23:59:59"
LOG_FILE = "deadline_log.txt"

deadline = datetime.strptime(DEADLINE, "%Y-%m-%d %H:%M:%S")
now      = datetime.now()
diff     = relativedelta(deadline, now)

report_lines = [
    "=== Project Deadline Tracker ===",
    f"Checked at  : {now.strftime('%Y-%m-%d %H:%M:%S')}",
    f"Target date : {DEADLINE}",
]

if deadline > now:
    remaining = f"{diff.months}m {diff.days}d {diff.hours}h remaining"
    report_lines.append(f"Status      : ON TRACK — {remaining}")
else:
    report_lines.append("Status      : — DEADLINE PASSED")

for line in report_lines:
    print(line)

with open(LOG_FILE, mode="a", encoding="utf-8") as log:
    log.write("\n".join(report_lines) + "\n\n")

print(f"\nLog appended to {LOG_FILE}")
