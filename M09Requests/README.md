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

In this practice, you will build three small, self-contained scripts. Each one introduces a real-world scenario and a different aspect of working with `requests`. Work through them in order—each one builds on the ideas from the last.

> **Before you start**: Make sure you have installed the `requests` library. Open your terminal and run:
> ```bash
> pip install requests
> ```
> Then create a new `.py` file for each practice below.

---

### Practice 1: Exploring a REST API with JSONPlaceholder

**What is JSONPlaceholder?**
[JSONPlaceholder](https://jsonplaceholder.typicode.com) is a free, fake REST API that behaves like a real server—but it doesn't actually store any changes. This makes it perfect for learning: you can freely send GET, POST, PUT, and DELETE requests without breaking anything.

**What you will build**: A script that walks through the complete CRUD cycle (Create, Read, Update, Delete) on a collection of fake blog posts.

---

#### Step 1: Fetch a single post

Create a new file called `jsonplaceholder_example.py`. Start by importing `requests` and making your very first API call.

```python
import requests

BASE_URL = 'https://jsonplaceholder.typicode.com'

response = requests.get(f'{BASE_URL}/posts/1')

print(response.status_code)
print(response.json())
```

Run this. You should see something like:

```
200
{'userId': 1, 'id': 1, 'title': 'sunt aut facere...', 'body': '...'}
```

**What just happened?**
- `requests.get(...)` sent an HTTP GET request to the server, just like a browser visiting a URL.
- The server replied with a **status code** of `200`, meaning "everything worked."
- `.json()` converted the server's response (which was a JSON string) into a regular Python dictionary—so you can access it with keys like `response.json()['title']`.

Now add a few more print lines to display specific fields cleanly:

```python
post = response.json()
print(f'Title: {post["title"]}')
print(f'Body : {post["body"][:80]}...')  # Only print the first 80 characters
```

---

#### Step 2: Fetch multiple posts with a filter

The `/posts` endpoint returns *all* 100 posts by default. Most real APIs let you filter results using **query parameters**—extra options you append to the URL. Instead of building the URL string manually (which gets messy), pass a Python dictionary to the `params` argument:

```python
params = {
    'userId': 1,
    '_limit': 3   # Ask for at most 3 results
}
response = requests.get(f'{BASE_URL}/posts', params=params)

posts = response.json()
print(f'Got {len(posts)} posts')

for post in posts:
    print(f'  ID {post["id"]:>3} | {post["title"]}')
```

Expected output (titles may vary):

```
Got 3 posts
  ID   1 | sunt aut facere repellat provident occaecati excepturi optio reprehenderit
  ID   2 | qui est esse
  ID   3 | ea molestias quasi exercitationem repudiandae...
```

**What just happened?**
- `requests` automatically built the URL `https://jsonplaceholder.typicode.com/posts?userId=1&_limit=3` from your `params` dictionary.
- The response is now a **list** of dictionaries, so we loop through it with `for`.

> **Tip**: `{post["id"]:>3}` is a formatting instruction that right-aligns the number in a column 3 characters wide. This is just cosmetic—don't worry about it if it's unfamiliar.

---

#### Step 3: Create a new post (POST)

So far you have only *read* data. Now send new data to the server to create a resource. The data goes in the `json=` argument as a Python dictionary—`requests` handles all the conversion to JSON automatically.

```python
new_post = {
    'title': 'My First API Post',
    'body': 'This was created by sending a POST request from Python!',
    'userId': 1
}

response = requests.post(f'{BASE_URL}/posts', json=new_post)

print(f'Status code: {response.status_code}')   # Expect 201, not 200
created_post = response.json()
print(f'Server gave it ID: {created_post["id"]}')
print(f'Title: {created_post["title"]}')
```

Expected output:

```
Status code: 201
Server gave it ID: 101
Title: My First API Post
```

**What just happened?**
- `201 Created` (not `200 OK`) is the standard success code for a `POST` that creates something new. Real-world APIs often return different 2xx codes to communicate *what kind* of success happened.
- The server echoed back the new resource, including the ID it assigned. Save this for the next step:

```python
new_post_id = created_post['id']
```

---

#### Step 4: Update and delete the post

First, use `PATCH` to update just the title (leaving all other fields untouched):

```python
partial_update = {'title': 'Updated With PATCH'}
response = requests.patch(f'{BASE_URL}/posts/{new_post_id}', json=partial_update)

updated = response.json()
print(f'New title : {updated["title"]}')
print(f'Body still: {updated.get("body", "(empty)")}')  # Should be unchanged
```

Then delete the post entirely:

```python
response = requests.delete(f'{BASE_URL}/posts/{new_post_id}')
print(f'Delete status: {response.status_code}')   # Expect 200
print(f'Response body: {response.text}')           # Expect {}
```

**What just happened?**
- `PATCH` only sends the fields you want to change. The server merges your changes with the existing data. (Contrast with `PUT`, which *replaces* the entire resource.)
- A `DELETE` request targets a specific resource by putting its ID in the URL path: `/posts/101`.

> **Reminder**: JSONPlaceholder does not actually store any changes. The IDs and data are simulated. In a real API, the post would have been genuinely saved and then genuinely deleted.

---

### Practice 2: Fetching Live Data from a Public REST API

**What is Frankfurter?**
[Frankfurter](https://www.frankfurter.app/) is a free, open-source currency exchange rate API. It requires **no API key and no registration**—just send a request and get real, live data back.

**What you will build**: A simple currency converter that fetches today's exchange rates and lets the user convert any USD amount to EUR, JPY, and TWD.

---

#### Step 1: Explore the API before writing any code

Before touching Python, open your browser and paste this URL into the address bar:

```
https://api.frankfurter.app/latest?from=USD&to=EUR,JPY,TWD
```

You should see raw JSON in your browser, like this:

```json
{
  "amount": 1.0,
  "base": "USD",
  "date": "2025-01-15",
  "rates": {
    "EUR": 0.9234,
    "JPY": 155.21,
    "TWD": 32.85
  }
}
```

**This step matters.** Always inspect an API's raw response before you write code to parse it. Notice the structure: the exchange rates are inside a nested key called `"rates"`.

---

#### Step 2: Make the request with query parameters

Create a new file called `frankfurter_example.py`:

```python
import requests

BASE_URL = 'https://api.frankfurter.app'

params = {
    'from': 'USD',
    'to': 'EUR,JPY,TWD'
}

try:
    response = requests.get(f'{BASE_URL}/latest', params=params)
    response.raise_for_status()   # Stop immediately if the server returns an error
except requests.exceptions.ConnectionError:
    print('ERROR: Could not connect. Check your internet connection.')
    exit()
except requests.exceptions.HTTPError as err:
    print(f'ERROR: Server returned an error: {err}')
    exit()

data = response.json()
print(data)
```

---

#### Step 3: Parse and display a formatted report

You confirmed the data arrives correctly. Now extract the parts you need:

```python
base_currency = data['base']        # 'USD'
rate_date     = data['date']        # e.g. '2025-01-15'
rates         = data['rates']       # {'EUR': 0.9234, 'JPY': 155.21, 'TWD': 32.85}

print(f'Exchange rates from {base_currency} (as of {rate_date}):')
for currency, rate in rates.items():
    print(f'  {currency:<5} : {rate:>10.4f}')
```

Expected output:

```
Exchange rates from USD (as of 2025-01-15):
  EUR   :     0.9234
  JPY   :   155.2100
  TWD   :    32.8500
```

**Unpacking the format strings:**
- `{currency:<5}` — left-align the currency code in a 5-character-wide column.
- `{rate:>10.4f}` — right-align the number, show exactly 4 decimal places, in a 10-character-wide column.

These are purely cosmetic. Your output will look slightly different if you omit the formatting, and that is completely fine.

---

#### Step 4: Build an interactive converter

Ask the user to type an amount, then calculate how much it is worth in each currency:

```python
try:
    amount_str = input('\nEnter an amount in USD to convert: $ ')
    amount_usd = float(amount_str)   # input() always returns a string—convert it!
except ValueError:
    print('ERROR: Please enter a valid number.')
    exit()

print(f'\n$ {amount_usd:.2f} USD is equivalent to:')
for currency, rate in rates.items():
    converted = amount_usd * rate
    if currency == 'JPY':
        print(f'  {currency}: {converted:>12,.0f}')    # JPY has no decimal places
    else:
        print(f'  {currency}: {converted:>12,.2f}')
```

Try entering `100`. You should see:

```
$ 100.00 USD is equivalent to:
  EUR:         92.34
  JPY:       15,521
  TWD:      3,285.00
```

> **Common mistake**: Forgetting to convert `input()` to a number. `input()` *always* returns a string, even if the user types `100`. You cannot multiply a string by a decimal rate. Wrapping it in `float()` converts it—and the `try/except` block catches the error if the user types something like `"abc"` instead.

---

### Practice 3: Fetching Content from a Regular Webpage

Not everything on the internet is a JSON API. Sometimes you need to fetch the raw HTML of a webpage—this is the first step of **web scraping**. The `requests` library works identically whether the server sends back JSON or HTML; the difference only becomes visible when you look at `response.text`.

**Service**: [Books to Scrape](https://books.toscrape.com/) — a free, safe website built *specifically* for practising web scraping. You will never be blocked.

> **Important**: In this practice, we will fetch the HTML using `requests` and then use a library called `BeautifulSoup` to parse it. This serves as a bridge into the next module (M10). 
> 
> Before starting, ensure you have BeautifulSoup installed:
> ```bash
> pip install beautifulsoup4
> ```

---

#### Step 1: Send a GET request to the homepage

Create a new file called `books_to_scrape_example.py`:

```python
import requests

TARGET_URL = '[https://books.toscrape.com/](https://books.toscrape.com/)'

try:
    response = requests.get(TARGET_URL)
    response.raise_for_status()
    print('Request successful!')
except requests.exceptions.ConnectionError:
    print('ERROR: Could not connect.')
    exit()
except requests.exceptions.HTTPError as err:
    print(f'ERROR: {err}')
    exit()

```

If you see `Request successful!`, the server responded normally.

---

#### Step 2: Inspect the response metadata

Now look at *what kind* of data came back:

```python
print(f'Status Code   : {response.status_code}')
print(f'Content-Type  : {response.headers.get("Content-Type")}')
print(f'Content-Length: {response.headers.get("Content-Length", "Not provided")}')

```

Expected output:

```
Status Code   : 200
Content-Type  : text/html; charset=utf-8
Content-Length: Not provided

```

Notice **`Content-Type: text/html`**. This is the key difference from a JSON API, which would return `application/json`. The `Content-Type` header tells you the format of the data—always check it when you are unsure what a server sends back.

---

#### Step 3: Preview the raw HTML

```python
print(response.text[:500])
print(f'... (total: {len(response.text):,} characters)')

```

You will see something like:

```html
<!DOCTYPE html>
<html>
    <head>
        <title>All products | Books to Scrape - Sandbox</title>
        ...
    </head>
    <body>
        ...

```

This is the raw HTML source of the page—exactly the same thing your browser downloads when you visit the URL, before it renders it visually.

---

#### Step 4: Try to find a book title using string methods

Let's try to locate a specific book title inside the raw HTML using Python's built-in `.find()`:

```python
search_term = 'Tipping the Velvet'
position = response.text.find(search_term)

if position != -1:
    # Show 250 characters around the match to see its context
    surrounding = response.text[position - 100 : position + 150]
    print(f'Found at character position {position}:')
    print(surrounding)
else:
    print('Title not found.')

```

You will find the title—but look at what surrounds it:

```html
<article class="product_pod">
  <h3><a href="catalogue/tipping-the-velvet_999/index.html"
         title="Tipping the Velvet">Tipping the ...</a></h3>

```

The text you want is buried inside nested HTML tags. Now ask yourself: how would you extract *all 20 book titles* from this page using only `.find()` or `.split()`? You would need to handle inconsistent whitespace, varying tag attributes, and truncated text (the `<a>` tag shows a shortened version). String methods become brittle and unmaintainable very quickly.

---

#### Step 5: The Better Way — Using BeautifulSoup

Instead of treating HTML like a giant, messy string, we use `BeautifulSoup`. It understands the *tree structure* of HTML, allowing us to navigate directly to the tags we want.

Add this to the bottom of your script to extract all 20 book titles instantly:

```python
from bs4 import BeautifulSoup

# 1. Pass the raw HTML to BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# 2. Find all <article> tags that have the class 'product_pod'
articles = soup.find_all('article', class_='product_pod')

print(f'\nFound {len(articles)} books! Extracting titles:\n')

# 3. Loop through them and extract the exact text we need
for index, article in enumerate(articles, start=1):
    title = article.h3.a['title']
    print(f'{index:>2}. {title}')

```

Expected output:

```
Found 20 books! Extracting titles:

 1. A Light in the Attic
 2. Tipping the Velvet
 3. Soumission
 4. Sharp Objects
 ...
20. It's Only the Himalayas

```

> **Key takeaway for this practice**: `requests` is responsible for *getting the data*. A separate library (`BeautifulSoup`) is responsible for *understanding and navigating* that data. These are two separate jobs, and keeping them separate makes your code cleaner and significantly more robust.

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