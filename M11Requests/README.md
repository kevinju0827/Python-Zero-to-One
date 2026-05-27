# M11 Web Requests

![Module 11 of 17](https://img.shields.io/badge/Module-11_of_17-6366f1?style=flat-square)
![Intermediate](https://img.shields.io/badge/Difficulty-Intermediate-facc15?style=flat-square)
![~2 hours](https://img.shields.io/badge/Time-~2_hours-60a5fa?style=flat-square)
![Prerequisites: M01–M10](https://img.shields.io/badge/Prerequisites-M01–M10-94a3b8?style=flat-square)

**Topics covered:** HTTP protocol · `requests` library · GET / POST / PATCH / DELETE · query parameters · headers · status codes · `raise_for_status()` · web scraping intro with BeautifulSoup

## The Why?

Every script you have written so far lives entirely on your machine — it reads local files, processes local data, and writes local output. The moment you connect to the web, your programs stop being isolated experiments and start being real networked applications.

When your weather app shows today's forecast, when a payment service validates your card, when you pull live stock prices into a spreadsheet — all of that communication follows a single protocol: **HTTP**. Python's `requests` library makes HTTP feel as natural as calling a function.

This module is the gateway to the entire "live data" portion of the course: every module from M12 onward either fetches from the web, serves to the web, or processes data that came from the web.

---

## Core Concepts

### How the Web Works: HTTP Request–Response

Every web interaction follows the same two-step pattern:

```
Client (your script) ──── HTTP Request ────▶ Server (API or website)
Client (your script) ◀─── HTTP Response ──── Server
```

**An HTTP Request contains:**
- **Method** — what action you want to perform:

  | Method | Meaning | Analogy |
  |--------|---------|---------|
  | `GET` | Retrieve data; change nothing | Reading a book |
  | `POST` | Submit new data to create a resource | Filling out a form |
  | `PUT` | Replace an existing resource entirely | Overwriting a saved file |
  | `PATCH` | Partially update an existing resource | Crossing out one line |
  | `DELETE` | Remove a resource | Tearing out a page |

- **URL** — the address of the resource (`https://api.example.com/users/42`)
- **Headers** — metadata (e.g., `Authorization: Bearer token123`)
- **Body** — data payload (used with POST/PUT/PATCH)

**An HTTP Response contains:**
- **Status code** — a three-digit number indicating outcome:

  | Range | Category | Common codes |
  |-------|----------|-------------|
  | 2xx | Success | `200 OK`, `201 Created` |
  | 3xx | Redirect | `301 Moved Permanently` |
  | 4xx | Client error | `404 Not Found`, `401 Unauthorized` |
  | 5xx | Server error | `500 Internal Server Error` |

- **Headers** — metadata about the response (e.g., `Content-Type: application/json`)
- **Body** — the actual content (JSON, HTML, or other data)

---

### Installing and Using `requests`

`requests` is not in the standard library — install it once:

```bash
pip install requests
```

Then import in any script:

```python
import requests
```

---

### GET — Fetching Data

```python
import requests

response = requests.get("https://jsonplaceholder.typicode.com/posts/1")

print(response.status_code)   # 200
print(response.json())        # Python dict from the JSON body
```

The `response` object holds everything the server sent back:
- `.status_code` — integer status code
- `.text` — raw body as a string
- `.json()` — parses the JSON body into a Python dict or list
- `.headers` — response headers as a dict

**With query parameters:**

```python
# Instead of building "?userId=1&_limit=3" manually:
params = {"userId": 1, "_limit": 3}
response = requests.get("https://jsonplaceholder.typicode.com/posts", params=params)
posts = response.json()   # A list of dicts
```

---

### POST, PATCH, DELETE

```python
# POST — create a new resource
new_post = {"title": "Hello", "body": "World", "userId": 1}
response = requests.post("https://jsonplaceholder.typicode.com/posts", json=new_post)
print(response.status_code)   # 201 Created

# PATCH — update specific fields only
update = {"title": "Updated Title"}
response = requests.patch("https://jsonplaceholder.typicode.com/posts/1", json=update)

# DELETE — remove a resource
response = requests.delete("https://jsonplaceholder.typicode.com/posts/1")
print(response.status_code)   # 200
```

---

### Error Handling — Defensive HTTP

Network calls can fail. Write defensive code:

```python
import requests

try:
    response = requests.get("https://api.example.com/data", timeout=10)
    response.raise_for_status()   # Raises exception for 4xx/5xx responses
    data = response.json()
except requests.exceptions.ConnectionError:
    print("Cannot connect. Check your internet.")
except requests.exceptions.Timeout:
    print("Request timed out.")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e.response.status_code}")
```

`raise_for_status()` is the cleanest pattern: it turns any 4xx/5xx response into a catchable exception, so you do not have to check every status code manually.

---

### Web Scraping Intro — HTML via `requests` + BeautifulSoup

Not every data source is a clean JSON API. Sometimes you need to extract data from a regular webpage (HTML). `requests` fetches the page; **BeautifulSoup** parses and navigates the HTML tree.

```bash
pip install beautifulsoup4
```

```python
import requests
from bs4 import BeautifulSoup

response = requests.get("https://books.toscrape.com/")
soup = BeautifulSoup(response.text, "html.parser")

# Find all article elements with class "product_pod"
books = soup.find_all("article", class_="product_pod")
for book in books:
    title = book.h3.a["title"]
    print(title)
```

> **Key principle:** `requests` fetches the data. BeautifulSoup understands its structure. Keep these responsibilities separate.

---

## Going Further

<details>
<summary>Authentication Headers</summary>

Many real APIs require a token:

```python
headers = {"Authorization": "Bearer YOUR_TOKEN_HERE"}
response = requests.get("https://api.example.com/private", headers=headers)
```

> Never commit real tokens to Git. Load them from environment variables:
> ```python
> import os
> token = os.environ.get("API_TOKEN")
> ```

</details>

<details>
<summary>Sessions — Reusing Connections and Headers</summary>

A `Session` object maintains persistent headers and connection pooling:

```python
session = requests.Session()
session.headers.update({"Authorization": "Bearer token"})
session.get("https://api.example.com/endpoint1")
session.get("https://api.example.com/endpoint2")
```

</details>

<details>
<summary>Handling Pagination</summary>

Most APIs return results in pages. Keep fetching until there is no "next" page:

```python
page = 1
while True:
    resp = requests.get(url, params={"page": page, "per_page": 100})
    data = resp.json()
    if not data:
        break
    process(data)
    page += 1
```

</details>

<details>
<summary>Respecting Robots.txt and Rate Limits</summary>

Before scraping a site, check `https://example.com/robots.txt` for scraping rules.
Add `time.sleep(1)` between requests to avoid overwhelming small servers.

</details>

---

## Guided Practice

We will build three small, self-contained scripts covering the full CRUD cycle, a live data API, and basic web scraping.

### Practice 1 — Full CRUD with JSONPlaceholder

[JSONPlaceholder](https://jsonplaceholder.typicode.com) is a free fake REST API — perfect for learning because you cannot break anything.

Create `jsonplaceholder_example.py`:

**Step 1 — Fetch a single post:**

```python
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

response = requests.get(f"{BASE_URL}/posts/1")
post = response.json()
print(f"Title: {post['title']}")
print(f"Body:  {post['body'][:80]}...")
```

**Step 2 — Filter multiple posts:**

```python
params = {"userId": 1, "_limit": 3}
response = requests.get(f"{BASE_URL}/posts", params=params)
for post in response.json():
    print(f"  ID {post['id']:>3} | {post['title'][:50]}")
```

**Step 3 — Create, update, delete:**

```python
# Create
new = {"title": "My Post", "body": "Content here.", "userId": 1}
resp = requests.post(f"{BASE_URL}/posts", json=new)
post_id = resp.json()["id"]
print(f"Created ID {post_id}, status {resp.status_code}")

# Update title only
resp = requests.patch(f"{BASE_URL}/posts/{post_id}", json={"title": "Updated"})
print(f"Updated: {resp.json()['title']}")

# Delete
resp = requests.delete(f"{BASE_URL}/posts/{post_id}")
print(f"Deleted, status {resp.status_code}")
```

### Practice 2 — Live Currency Converter

[Frankfurter](https://www.frankfurter.app/) provides live exchange rates with no API key.

Create `frankfurter_example.py`:

```python
import requests

try:
    response = requests.get(
        "https://api.frankfurter.app/latest",
        params={"from": "USD", "to": "EUR,JPY,TWD"},
        timeout=10
    )
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
    exit()

data  = response.json()
rates = data["rates"]

amount = float(input("Enter USD amount: $"))
print(f"\n${amount:.2f} USD =")
for currency, rate in rates.items():
    converted = amount * rate
    fmt = f"{converted:>12,.0f}" if currency == "JPY" else f"{converted:>12,.2f}"
    print(f"  {currency}: {fmt}")
```

### Practice 3 — Web Scraping Book Titles

Create `books_to_scrape_example.py`:

```python
import requests
from bs4 import BeautifulSoup

response = requests.get("https://books.toscrape.com/")
response.raise_for_status()

soup    = BeautifulSoup(response.text, "html.parser")
articles = soup.find_all("article", class_="product_pod")

print(f"Found {len(articles)} books:\n")
for i, article in enumerate(articles, start=1):
    title = article.h3.a["title"]
    price = article.find("p", class_="price_color").text
    print(f"  {i:>2}. {title:<50} {price}")
```

---

## Checkpoints

* [ ] **Live Earthquake Report**
  Taiwan's CWA Open Data platform provides real-time earthquake data at:
  `https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0015-001`
  Register for a free account at [opendata.cwa.gov.tw](https://opendata.cwa.gov.tw/userLogin) to get an Authorization key.
  Write a script that:
  1. Fetches the latest significant earthquake records.
  2. Prints each earthquake's location, magnitude, depth (km), and date/time.
  3. Prints a final line: "Strongest: M[X] at [location]."
  *(Hint: the earthquake list is nested several levels deep inside the response. Print `response.json()` first to explore the structure.)*

* [ ] **GitHub Repo Stats**
  Use the public GitHub API (no key needed for public data):
  `https://api.github.com/repos/{owner}/{repo}`
  Ask the user for an owner and repo name.
  Fetch and print: stars, forks, open issues, language, and last push date.
  Handle `404 Not Found` gracefully with a clear message.

* [ ] **News Headline Scraper**
  Choose any news website that does not require JavaScript to render headlines (check with your browser's View Source).
  Fetch the homepage with `requests`, parse it with BeautifulSoup, and extract the first 10 article headlines.
  Save them to `headlines.txt` with today's date as a header.
