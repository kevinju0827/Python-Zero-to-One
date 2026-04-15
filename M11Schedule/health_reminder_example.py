import schedule
import time
from datetime import datetime

def remind_stretch():
    """Function to be called by the scheduler."""
    # Get current time for the log display
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] Time to stand up and stretch!")

# 1. Schedule the job to run every 5 seconds
# This uses the 'schedule' library's readable syntax
schedule.every(5).seconds.do(remind_stretch)

print("--- Health Reminder Bot Started ---")
print("I will remind you every 5 seconds (for testing).")
print("Press Ctrl+C to exit the program.")

# 2. Keep the script running forever in a loop
try:
    while True:
        # This checks if any scheduled task is ready to run
        schedule.run_pending()
        
        # We sleep for 1 second in each loop to save CPU power
        time.sleep(1)
except KeyboardInterrupt:
    print("\nReminder bot stopped. Take care of your back!")
