import requests

url = "https://jsonplaceholder.typicode.com/todos"
print(f"Connecting to {url}...")

todos = []

try:
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        todos = response.json()
    else:
        print(f"Failed to fetch data. Server status: {response.status_code}")
except requests.exceptions.ConnectionError:
    print("Error: Could not connect to the internet. Please check your connection.")
except requests.exceptions.Timeout:
    print("Error: The request timed out. The server took too long to respond.")

total_tasks = len(todos)
completed_count = sum(1 for task in todos if task['completed'])
pending_count = total_tasks - completed_count
print(f"Total tasks on server: {total_tasks}")
print(f"[✓] Completed: {completed_count}  |  [ ] Pending: {pending_count}")

print("\n--- Your Top 5 Tasks ---")
for task in todos[:5]:
    status = "[✓]" if task['completed'] else "[ ]"
    print(f"{status} {task['title']}")

