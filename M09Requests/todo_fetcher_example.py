import requests

# The URL of the API endpoint (a free, fake REST API for testing)
url = "https://jsonplaceholder.typicode.com/todos"

print(f"Connecting to {url}...")

# Make the GET request to the server
try:
    response = requests.get(url, timeout=10)

    # Check the status code (200 means OK/Success)
    if response.status_code == 200:
        # Parse the JSON response into a Python list
        todos = response.json()
        
        print("\n--- Your Top 5 Tasks ---")
        # Loop through the first 5 items in the list
        for task in todos[:5]:
            status = "[✓]" if task['completed'] else "[ ]"
            print(f"{status} {task['title']}")
        
        print("-" * 24)
        print(f"Total tasks available on server: {len(todos)}")
    else:
        print(f"Failed to fetch data. Server responded with status: {response.status_code}")

except requests.exceptions.ConnectionError:
    print("Error: Could not connect to the internet. Please check your connection.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
