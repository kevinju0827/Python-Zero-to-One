# M09 Requests

## The "Why?"

The modern world is built on **APIs** (Application Programming Interfaces). Whether you are checking the weather on your phone, logging into a website with Google, or fetching the latest stock prices, your device is making a "request" to a server. The `requests` library is the most popular way for Python to talk to the internet, allowing you to fetch live data from around the globe in just a few lines of code.

## Goals

Learn how to make HTTP GET requests, check response status codes to ensure success, and parse JSON data received from a web server.

## Core Concepts

Before we start pulling data from the internet, let's understand the key components of web requests.

### APIs and Endpoints
If a restaurant is a server, the **API (Application Programming Interface)** is the menu. It tells you what data is available to order. An **Endpoint** is the specific URL for a particular item on that menu. For example, `https://api.example.com/users` might be the endpoint to get a list of users, while `https://api.example.com/weather` gives you the weather.

### HTTP GET Requests
A "GET" request is exactly what your web browser does when you type in a URL and press Enter. You are sending a message to a server saying, "Please *get* the information at this address and send it back to me."

### Status Codes
Whenever you make a request, the server always replies with a 3-digit status code. This is a quick way to know if your request succeeded before you even look at the data:
* **200 OK**: Perfect! The server understood the request and is returning the data.
* **401 / 403 Forbidden**: You don't have permission to view this data (often requires an API key or login).
* **404 Not Found**: The endpoint or resource you are looking for does not exist.
* **500 Internal Server Error**: The server is broken or crashed on their end.

### The Response Object
When the server answers your request, Python packages everything into a `Response` object. You can extract different things from it:
* `response.status_code`: Gives you the 3-digit number.
* `response.text`: Returns the raw data as a giant, plain text string.
* `response.json()`: If the server sends back JSON data (which is the most common), this magical method instantly parses it and converts it directly into a highly usable Python Dictionary or List!

## Guided Practice

Imagine we are developing a terminal interface for a task management application. We need to fetch a user's to-do list from a server. For this practice, we will use **JSONPlaceholder**, a free API service that provides fake data for developers to test their code.

Our goal is to write a Python script that connects to this API, verifies a successful connection, parses the JSON data into a Python list, and then displays the first 5 tasks along with a summary of how many tasks are completed versus pending.

### Step 1: Setting up the Tools and Target
First, we must import the `requests` library. 
Next, we define our target **Endpoint URL**: `https://jsonplaceholder.typicode.com/todos`. 
This is the specific "menu item" on the server that contains the list of tasks.

### Step 2: Making the Request and Handling Network Errors
Internet connections are unpredictable. 
Therefore, we wrap our request in a `try-except` block. 
We use `requests.get()` to fetch the data and include a `timeout=10` parameter. 
This is a best practice that tells Python, "If the server doesn't respond within 10 seconds, stop trying." 
We also prepare to catch specific errors like `ConnectionError` (no internet) or `Timeout`.

### Step 3: Verifying the Status and Parsing Data
Once we receive a response, we check the `status_code`. 
If it is `200`, the request was successful. We then call the `.json()` method. 
This instantly transforms the raw JSON text from the web into a standard Python **List**, where each item is a **Dictionary** representing a single task.

### Step 4: Data Extraction and Statistics
Now that the data is in a usable Python format (let's call it `todos`):
1. Calculate Statistics: To provide a summary, we count the total number of tasks using `len()`. Then, we can use a loop or a "generator expression" to count how many tasks have their `'completed'` status set to `True`. Finally, we subtract the completed count from the total to find the number of pending tasks.
2. Display Top 5: We use a `for` loop with a slice (`todos[:5]`) to iterate through the first five items. By checking the `'completed'` key (which is a Boolean `True` or `False`), we can print a visual status like `[✓]` or `[ ]` next to the task title.

## Checkpoints

* [ ] **Interactive Pokédex**:
    Let's catch some data! The "PokéAPI" is a famous, free API used by developers to practice web requests. 
    Write an interactive script that uses `input()` to ask the user for a Pokémon's name (e.g., "squirtle" or "snorlax"). 
    Dynamically append their input to the base URL: `https://pokeapi.co/api/v2/pokemon/`. 
    Send a GET request to this dynamically generated URL. 
    If the request is successful (Status 200), parse the JSON response to extract and print that specific Pokémon's `height` and `weight`. 
    If the user types a name that does not exist, the API will return a 404 status code—use an `if/else` statement to catch this and print a friendly "Pokémon not found!" message instead of crashing the program.