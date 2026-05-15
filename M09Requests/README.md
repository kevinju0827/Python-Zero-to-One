# M09 Requests

## The "Why?"

Every modern application talks to the outside world. When your phone's weather app displays today's forecast, when you log into a website, or when a payment system checks your bank balance—all of that communication happens over the internet through a standardized system called **HTTP**. Until now, your Python scripts have only been able to read and write files that already exist on your computer. In this module, you will learn how to reach beyond your machine and pull live data from anywhere on the web, turning your scripts into true networked applications.

Python's built-in tools are powerful, but they are deliberately low-level. The third-party **`requests`** library was built to make HTTP feel natural and readable in Python. It is one of the most downloaded Python packages in history for a reason: it turns what used to require dozens of lines of complex networking code into just one or two clean, expressive lines.

## Goals

By the end of this module, you should be able to:

* Explain what HTTP is and describe the roles of requests and responses in client-server communication.
* Identify the most common HTTP methods (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`) and describe when each one is appropriate.
* Explain what an HTTP status code is and what the major categories (2xx, 4xx, 5xx) mean.
* Install and import the `requests` library and use it to send HTTP requests from a Python script.
* Access the response status code, headers, raw text, and parsed JSON data from a response object.
* Pass query parameters and a JSON body in a request.
* Write defensive code that checks for errors before trusting a response.

## Core Concepts

### How the Internet Communicates: The HTTP Protocol

Before writing a single line of `requests` code, it is worth understanding the underlying system it relies on.

**HTTP** stands for **HyperText Transfer Protocol**. It is the agreed-upon set of rules that governs how two computers exchange information over the web. Think of it as the "language" that your browser and a remote server both agree to speak.

The communication always follows a simple pattern:

1. **The Client sends a Request.** Your browser, your script, or a mobile app is the *client*. It initiates the conversation by sending a structured message to a server, saying: "I want to *do something* with *this resource*."
2. **The Server sends a Response.** The *server* receives the request, processes it, and sends back a structured reply: "Here is the result of what you asked for."

This request-response cycle is the foundation of virtually all web communication.

#### Anatomy of an HTTP Request

Every HTTP request carries three key pieces of information:

* **Method**: A verb that tells the server *what action* you want to perform on the resource. The most common methods are:

  | Method   | Meaning                                     | Real-World Analogy                     |
  |----------|---------------------------------------------|----------------------------------------|
  | `GET`    | Retrieve data; do not change anything       | Reading a page in a book               |
  | `POST`   | Submit new data to be created on the server | Filling out and submitting a form      |
  | `PUT`    | Replace an existing resource entirely       | Overwriting a saved file               |
  | `PATCH`  | Partially update an existing resource       | Crossing out one line and rewriting it |
  | `DELETE` | Remove a resource                           | Tearing a page out of a book           |

* **URL (Uniform Resource Locator)**: The address that identifies *which resource* you are acting on. For example, `https://api.example.com/users/42` points to the user with ID 42.

* **Headers**: Optional metadata attached to the request. Think of them as a cover letter accompanying your main message. Common headers include `Content-Type` (telling the server what format your data is in) and `Authorization` (proving who you are with a token or key).

* **Body** (optional): The actual data payload, used mainly with `POST`, `PUT`, and `PATCH` requests. For example, when creating a new user, the body contains the new user's name and email.

#### Anatomy of an HTTP Response

The server's reply is equally structured:

* **Status Code**: A three-digit number that immediately tells you whether the request succeeded or failed. The number categories are:

  | Range | Category     | Meaning                                                                                                         |
  |-------|--------------|-----------------------------------------------------------------------------------------------------------------|
  | 2xx   | Success      | Everything worked. `200 OK` is the most common.                                                                 |
  | 3xx   | Redirection  | The resource has moved; follow the new address.                                                                 |
  | 4xx   | Client Error | *You* made a mistake. `404 Not Found` means the URL doesn't exist; `401 Unauthorized` means you need to log in. |
  | 5xx   | Server Error | The *server* had a problem. `500 Internal Server Error` is the most common.                                     |

* **Headers**: Metadata from the server, such as `Content-Type: application/json` which tells you the format of the data being returned.

* **Body**: The actual content of the response—often HTML (for webpages) or JSON (for APIs).

#### What is a REST API?

You will frequently hear the term **REST API** (or RESTful API). REST is a popular design style for building web services that follow a clean set of conventions:

* Resources are represented as URLs (e.g., `/users`, `/products/5`).
* HTTP methods carry meaning (`GET` to read, `POST` to create, etc.).
* Responses are typically in JSON format.

When a service follows these conventions, any client (your Python script, a browser, or a mobile app) can interact with it in a predictable way. Most of the services you will interact with in this module—and in the real world—are REST APIs.

---

### Installing and Using the `requests` Library

Unlike `csv` and `json` from M08, `requests` is **not** part of Python's standard library. You need to install it once before you can use it.

Open your terminal and run:

```bash
pip install requests
```

After installation, you can import it in any script:

```python
import requests
```

---

### Sending a GET Request

`GET` is the most fundamental operation—fetching data without changing anything. In `requests`, it is a single function call:

```python
import requests

response = requests.get('https://jsonplaceholder.typicode.com/posts/1')

print(response.status_code)  # 200
print(response.text)         # Raw response body as a plain string
print(response.json())       # Parsed directly into a Python dictionary
```

The `response` object is the heart of the library. It holds everything the server sent back. The three attributes above are the ones you will use most often:

* `response.status_code` — the HTTP status code (integer).
* `response.text` — the response body as a raw string.
* `response.json()` — a convenience method that calls `json.loads()` on `response.text` for you, returning a Python dictionary or list.

#### Adding Query Parameters

Many APIs let you filter or customize results by appending parameters to the URL. Instead of manually building ugly strings like `?userId=1&_limit=5`, you can pass a clean Python dictionary to the `params` argument:

```python
import requests

# Equivalent to: GET https://jsonplaceholder.typicode.com/posts?userId=1&_limit=3
params = {'userId': 1, '_limit': 3}
response = requests.get('https://jsonplaceholder.typicode.com/posts', params=params)

posts = response.json()
for post in posts:
    print(post['title'])
```

---

### Sending a POST Request

Use `POST` to send new data to a server and ask it to create a new resource. The data you want to send goes in the `json` argument as a Python dictionary. The `requests` library will automatically serialize it to JSON and set the correct `Content-Type` header for you.

```python
import requests

new_post = {
    'title': 'My First API Post',
    'body': 'This was sent from a Python script!',
    'userId': 1
}

response = requests.post(
    'https://jsonplaceholder.typicode.com/posts',
    json=new_post
)

print(response.status_code)  # 201 Created
print(response.json())       # The server echoes back the created resource
```

> **`json=` vs `data=`**: Always prefer `json=` when sending structured data to a REST API. Using `data=` sends form-encoded data (like an old HTML form), which most modern APIs do not expect.

---

### Sending PUT and PATCH Requests

Both `PUT` and `PATCH` are used to update existing resources. The key difference is scope:

* **`PUT`**: Replaces the entire resource. You must send *all* fields, even the ones you are not changing.
* **`PATCH`**: Updates only the fields you specify. Everything else on the server stays the same.

```python
import requests

# PUT: Replace the entire post
response_put = requests.put(
    'https://jsonplaceholder.typicode.com/posts/1',
    json={'id': 1, 'title': 'Updated Title', 'body': 'Updated body.', 'userId': 1}
)
print(response_put.status_code)  # 200 OK

# PATCH: Only update the title
response_patch = requests.patch(
    'https://jsonplaceholder.typicode.com/posts/1',
    json={'title': 'Just the Title Changed'}
)
print(response_patch.status_code)  # 200 OK
```

---

### Sending a DELETE Request

Use `DELETE` to ask the server to remove a resource. The response body is usually empty or a simple confirmation.

```python
import requests

response = requests.delete('https://jsonplaceholder.typicode.com/posts/1')
print(response.status_code)  # 200 OK (or 204 No Content on some APIs)
```

---

### Sending Request Headers

Some APIs require additional metadata in the request headers. The most common use case is authentication—proving your identity with an API key or token. You pass headers as a Python dictionary using the `headers` argument:

```python
import requests

headers = {
    'Authorization': 'Bearer YOUR_API_TOKEN_HERE',
    'Accept': 'application/json'
}

response = requests.get('https://api.example.com/private-data', headers=headers)
```

> **Security Warning**: Never hardcode real API tokens or passwords directly in your source code, especially if you plan to share it or push it to GitHub. A common practice is to load secrets from environment variables instead.

---

### Error Handling: Writing Defensive Code

A network call can fail for many reasons: the server is down, the URL is wrong, your internet connection drops, or the API returns an error code. Good Python scripts anticipate these failures and handle them gracefully rather than crashing.

**Method 1: Check the status code manually**

The simplest approach is to inspect `response.status_code` yourself and react accordingly.

```python
import requests

response = requests.get('https://jsonplaceholder.typicode.com/posts/99999')

if response.status_code == 200:
    print(response.json())
elif response.status_code == 404:
    print('Error: The requested resource was not found.')
else:
    print(f'Unexpected error. Status code: {response.status_code}')
```

**Method 2: Use `raise_for_status()`**

The `requests` library provides a built-in shortcut: calling `response.raise_for_status()` will automatically raise a `requests.exceptions.HTTPError` exception if the status code is 4xx or 5xx. This lets you write clean `try/except` blocks without manually checking every possible error code.

```python
import requests

try:
    response = requests.get('https://jsonplaceholder.typicode.com/posts/1')
    response.raise_for_status()  # Raises an exception for 4xx/5xx responses
    data = response.json()
    print(data['title'])
except requests.exceptions.HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
except requests.exceptions.ConnectionError:
    print('Could not connect to the server. Check your internet connection.')
except requests.exceptions.Timeout:
    print('The request timed out. The server took too long to respond.')
except requests.exceptions.RequestException as err:
    print(f'An unexpected error occurred: {err}')
```

Using `raise_for_status()` combined with a `try/except` block is considered best practice for any production-quality script.

---

## Guided Practice

In this practice, we will build three small, self-contained scripts that progressively introduce real-world scenarios. Each one focuses on a different aspect of working with `requests`.

### Practice 1: Exploring a REST API with JSONPlaceholder

**Scenario**: You are a developer learning a new API. Before writing any logic, it is common to explore the API interactively—fetching a single resource, listing multiple resources, and simulating a creation workflow to understand what the server expects and returns.

**Step 1: Fetch a single post**

Start by making a `GET` request for one specific post. Inspect the shape of the data the server returns. Pay attention to the keys in the dictionary.

**Step 2: Fetch all posts by a specific user**

Use the `params` argument to filter results. Ask for only the posts written by `userId` 1. Loop through the results and print each post's `id` and `title` on one line.

**Step 3: Simulate creating a new post**

Send a `POST` request with a new post payload. Check that the server responds with status code `201` and prints the newly created resource (including the server-assigned `id`) back to you.

**Step 4: Simulate deleting the post**

Use the `id` from the response in Step 3 to build a `DELETE` request URL. Confirm that the server returns `200` to indicate the deletion was accepted.

---

### Practice 2: Fetching Live Data from a Public REST API

**Service**: [Frankfurter](https://www.frankfurter.app/) — a free, open-source currency exchange rate API that requires no API key or registration.

**Scenario**: You are building a simple currency converter tool. The business team needs to know the current exchange rates from USD to a set of target currencies so they can generate daily financial reports.

**Step 1: Read the API documentation**

Before writing any code, visit `https://www.frankfurter.app/` and inspect the endpoint structure. Notice that `https://api.frankfurter.app/latest?from=USD` returns the latest rates from USD to all available currencies.

**Step 2: Make the request with query parameters**

Use the `params` argument to specify `from=USD` and `to=EUR,JPY,TWD`. This tells the API to return only the three currencies you care about, keeping the response small and focused.

**Step 3: Parse and display the results**

Call `.raise_for_status()` first. Then extract the `rates` dictionary from the JSON response and print a clean formatted report, like:

```
Exchange rates from USD (as of 2025-01-15):
  EUR: 0.9234
  JPY: 155.21
  TWD: 32.85
```

**Step 4: Calculate a conversion**

Ask the user (via `input()`) to enter an amount in USD. Multiply that amount by each rate and print what it converts to in each currency.

---

### Practice 3: Fetching Content from a Regular Webpage

Not everything on the internet is a JSON API. Sometimes you need to fetch the raw HTML content of a webpage—the first step in web scraping. The `requests` library handles this identically to API calls; the difference is in what comes back.

**Service**: [Books to Scrape](https://books.toscrape.com/) — a safe, legal, purpose-built website designed specifically for practicing web scraping.

> **Important note**: `requests` only fetches the raw HTML text. To actually *parse* and extract structured data from HTML (like a book title or price), you would use an additional library called `BeautifulSoup`, which is the topic of the next module. In this practice, we are only focused on the fetching step.

**Step 1: Send a GET request to the homepage**

Make a `GET` request to `https://books.toscrape.com/`. Use `raise_for_status()` to confirm the server responded successfully.

**Step 2: Inspect the response**

Print `response.status_code`, `response.headers['Content-Type']`, and the first 500 characters of `response.text`.

Notice how `Content-Type` is `text/html` instead of `application/json`. This is how you can tell whether you are talking to a webpage or an API.

**Step 3: Compare with a JSON API**

In a comment block at the bottom of your script, write a short answer to this question: *"Looking at `response.text`, why would it be difficult to extract just the list of book titles using only string methods? What kind of tool would make this easier?"* This reflection sets up the motivation for M10.

---

## Checkpoints

* [ ] **Live Earthquake Report**:
      Taiwan's government publishes real-time earthquake data through its open data platform.
      The endpoint `https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0015-001` provides recent significant earthquake records.

      > To use this API, you will need a free authorization token.
      > Visit [CWA Open Data](https://opendata.cwa.gov.tw/userLogin) and register for a free account to obtain your personal `Authorization` key.
      > Once you have it, pass it as a query parameter: `params={'Authorization': 'YOUR_KEY_HERE'}`.

      Write a script that:
      1. Fetches the latest earthquake records from the API.
      2. Extracts and loops through the list of earthquake events.
      3. For each earthquake, prints a formatted summary including: the earthquake's **location name**, its **magnitude**, its **depth** (in km), and the **date and time** it occurred.
      4. After printing all events, prints one final line showing the **strongest earthquake** in the current response (the one with the highest magnitude).

      *(Hint: Wrap your request in a `try/except` block using `raise_for_status()`. Inspect the raw JSON response structure carefully before writing your loop—the actual earthquake list is often nested several levels deep inside the response dictionary.)*