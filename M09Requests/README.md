# M09 Requests

## The "Why?"

The modern world is built on **APIs** (Application Programming Interfaces). Whether you are checking the weather on your phone, logging into a website with Google, or fetching the latest stock prices, your device is making a "request" to a server. The `requests` library is the most popular way for Python to talk to the internet, allowing you to fetch live data from around the globe in just a few lines of code.

## Goals

Learn how to make HTTP GET requests, check response status codes to ensure success, and parse JSON data received from a web server.

## Core Concepts

### HTTP GET Requests
A "GET" request is like typing a URL into your browser. You are asking the server to "get" some information and send it back to you.

### Status Codes
Servers respond with a 3-digit number to tell you how the request went:
- **200 OK**: Success!
- **404 Not Found**: The resource doesn't exist.
- **500 Internal Error**: The server crashed.

### The Response Object
When you make a request, Python gives you a `Response` object.
- `response.status_code`: The status number.
- `response.json()`: Converts the response body directly into a Python list or dictionary.

## Guided Practice

We will use a free service called **JSONPlaceholder** to fetch a list of "To-Do" tasks for a specific user and display them in our console.

*   **Step 1: Install the `requests` library**
    (Remember to use your virtual environment from M07!)
    ```bash
    pip install requests
    ```

*   **Step 2: Create `todo_fetcher_example.py`**
    ```python
    import requests

    url = "https://jsonplaceholder.typicode.com/todos"

    try:
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            todos = response.json()
            
            print(f"Successfully fetched {len(todos)} items!")
            print("-" * 30)

            for task in todos[:5]:
                status = "[✓]" if task['completed'] else "[ ]"
                print(f"{status} {task['title']}")
        else:
            print(f"Error: API returned status code {response.status_code}")

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the internet.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    ```

## Checkpoints

* [ ] **User Profile Card**:
    Use `https://jsonplaceholder.typicode.com/users/1` to fetch a single user's information. Print their name, email, and the name of the company they work for.
* [ ] **Website Health Checker**:
    Ask the user for a URL. Use `requests.get()` to check if the site is up. If it returns status code 200, print "Site is Online!", otherwise print a warning.
* [ ] **Random Post Generator**:
    Fetch the list of posts from `https://jsonplaceholder.typicode.com/posts`. Use the `random` module (from M07) to pick one random post and print its title and body.