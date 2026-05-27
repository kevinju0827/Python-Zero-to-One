from datetime import datetime
from dateutil.relativedelta import relativedelta

# Define a project deadline
# In a real scenario, this might come from a database or user input
deadline_str = "2026-12-31 23:59:59"
deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M:%S")

# Get the current time
now = datetime.now()

# Calculate the difference using relativedelta (from python-dateutil)
# This handles months and days much better than standard subtraction
diff = relativedelta(deadline, now)

print("--- Project Deadline Tracker ---")
print(f"Target Date: {deadline_str}")
print(f"Current Date: {now.strftime('%Y-%m-%d %H:%M:%S')}")
print("-" * 32)

if deadline > now:
    print(f"Time remaining: {diff.years} years, {diff.months} months, {diff.days} days, {diff.hours} hours.")
else:
    print("The deadline has already passed!")
