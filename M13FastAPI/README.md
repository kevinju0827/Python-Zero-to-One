# M13 Web API (FastAPI)

![Module 13 of 16](https://img.shields.io/badge/Module-13_of_16-6366f1?style=flat-square)
![Intermediate](https://img.shields.io/badge/Difficulty-Intermediate-facc15?style=flat-square)
![~2 hours](https://img.shields.io/badge/Time-~2_hours-60a5fa?style=flat-square)
![Prerequisites: M01?12](https://img.shields.io/badge/Prerequisites-M01?12-94a3b8?style=flat-square)

**Topics covered:** FastAPI 繚 Uvicorn 繚 routes 繚 path/query parameters 繚 Pydantic models 繚 HTTP status codes 繚 `HTTPException` 繚 Swagger UI 繚 combining FastAPI with SQLite

## The Why?

Until now, you have always been the **client** ??in M11 you sent requests to JSONPlaceholder; you posted prompts to local APIs. Someone else built the server, and you called it.

This module flips the relationship. You will build the **server** ??the program that listens for incoming requests, executes your Python logic, and returns structured JSON to whoever calls it.

This is what makes your work shareable. A mobile app, a JavaScript frontend, a spreadsheet macro in a colleague's Excel file, or even an LLM tool-call ??any of them can become a client of your Python code once it is wrapped in an API.

**FastAPI** is the most popular modern Python framework for this job. It is fast, generates interactive documentation automatically, and its syntax is intentionally close to writing ordinary Python functions. Companies including Netflix, Uber, and Microsoft use it in production.

---

## Core Concepts

### FastAPI and Uvicorn ??Two Layers

| Component | Role |
|-----------|------|
| **FastAPI** | The framework ??defines routes, validates data, returns responses |
| **Uvicorn** | The server ??opens a TCP port, accepts connections, passes requests to FastAPI |

Install both:

```bash
pip install fastapi "uvicorn[standard]"
```

Start the server:

```bash
uvicorn main:app --reload
```

`--reload` restarts the server every time you save a file ??essential during development.

---

### Your First Route

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, world!"}
```

`@app.get("/")` says: when someone makes a `GET` request to `/`, call this function.
The return value (a Python dict) is automatically serialized to JSON.

Run with `uvicorn main:app --reload`, then open `http://127.0.0.1:8000/` in your browser.

---

### Auto-Generated Docs ??Your Best Friend

Open `http://127.0.0.1:8000/docs` as soon as the server starts.
You will see a **Swagger UI** with every endpoint listed, interactive forms to try each one, and the actual JSON responses ??all generated automatically from your code. No extra work required.

Make `/docs` your first stop after every change.

---

### Path Parameters

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"id": user_id, "name": "placeholder"}
```

The `: int` type hint is not cosmetic ??FastAPI validates it. Calling `/users/abc` returns a clean `422 Unprocessable Entity` error automatically.

---

### Query Parameters

Function arguments that are not part of the URL path become query parameters:

```python
@app.get("/search")
def search(q: str, limit: int = 10):
    return {"query": q, "limit": limit}
```

Calling `GET /search?q=python&limit=5` ??`search(q="python", limit=5)`.
Default values make parameters optional.

---

### Pydantic Models ??Validated Request Bodies

For `POST` and `PUT` requests, describe the expected JSON body with a Pydantic model:

```python
from pydantic import BaseModel

class NewBook(BaseModel):
    title:  str
    author: str
    rating: int

@app.post("/books", status_code=201)
def add_book(book: NewBook):
    return {"saved": book.title, "author": book.author}
```

If a client sends `{"title": "Dune"}` (missing `author` and `rating`), FastAPI rejects it with a clear error ??without you writing any validation logic.

---

### `HTTPException` ??Returning the Right Status Codes

```python
from fastapi import HTTPException

@app.get("/books/{book_id}")
def get_book(book_id: int):
    book = BOOKS.get(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail=f"Book {book_id} not found.")
    return book
```

Returning the correct status codes (`404` for "not found", `409` for "conflict", `201` for "created") is what makes an API feel professional to clients.

---

### Combining FastAPI with SQLite

The pattern: each route opens a database connection, runs a query, and returns the result.

```python
import sqlite3
from fastapi import FastAPI

app = FastAPI()

@app.get("/expenses")
def list_expenses():
    conn = sqlite3.connect("expenses.db")
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM expenses").fetchall()
    conn.close()
    return [dict(row) for row in rows]
```

The combination of M12 (SQL) and M13 (FastAPI) is the most common backend pattern in industry.

---

## Going Further

<details>
<summary>Dependency Injection ??Sharing a DB Connection</summary>

Rather than opening a connection in every route, use FastAPI's dependency system:

```python
from fastapi import Depends

def get_db():
    conn = sqlite3.connect("mydata.db")
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

@app.get("/items")
def list_items(db = Depends(get_db)):
    return db.execute("SELECT * FROM items").fetchall()
```

</details>

<details>
<summary>Lifespan Events (startup/shutdown)</summary>

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code here runs ONCE on startup
    print("Server starting??)
    yield
    # Code here runs ONCE on shutdown
    print("Server shutting down??)

app = FastAPI(lifespan=lifespan)
```

</details>

<details>
<summary>CORS ??Allowing Frontend Apps</summary>

If a JavaScript frontend at a different domain calls your API, you need to enable CORS:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Restrict to specific domains in production
    allow_methods=["*"],
    allow_headers=["*"],
)
```

</details>

<details>
<summary>Async Routes</summary>

FastAPI supports async/await for non-blocking I/O:

```python
import httpx

@app.get("/proxy/weather/{city}")
async def proxy_weather(city: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"https://goweather.xyz/weather/{city}")
    return resp.json()
```

</details>

---

## Guided Practice

We will build a **mini coffee-shop menu API** ??a service that exposes a caf矇's drink list as JSON so any future client (mobile app, website, Slack bot) can fetch from one source of truth.

### Step 1 ??Define the data

Create `coffee_menu_api_example.py`:

```python
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Coffee Shop Menu API")

MENU = {
    "latte":    {"name": "Latte",    "price": 120, "in_stock": True},
    "espresso": {"name": "Espresso", "price":  80, "in_stock": True},
    "matcha":   {"name": "Matcha",   "price": 140, "in_stock": False},
    "americano":{"name": "Americano","price":  90, "in_stock": True},
}
```

### Step 2 ??`GET /menu` ??return all items

```python
@app.get("/menu")
def get_menu():
    return MENU
```

### Step 3 ??`GET /menu/search?q=...`

Define this **before** the `{drink_id}` route ??FastAPI matches routes top-down, and `/menu/search` would otherwise be captured as a drink id of `"search"`.

```python
@app.get("/menu/search")
def search_menu(q: str):
    results = {
        k: v for k, v in MENU.items()
        if q.lower() in v["name"].lower()
    }
    return results
```

### Step 4 ??`GET /menu/{drink_id}`

```python
@app.get("/menu/{drink_id}")
def get_drink(drink_id: str):
    drink = MENU.get(drink_id)
    if drink is None:
        raise HTTPException(status_code=404, detail=f"Drink '{drink_id}' not found.")
    return drink
```

### Step 5 ??Run and explore `/docs`

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("coffee_menu_api_example:app", reload=True)
```

Start the server and open `http://127.0.0.1:8000/docs`.
Expand each endpoint, click **"Try it out"**, and execute.
Notice what happens when you search for a drink that does not exist ??the `404` error is returned cleanly.

---

## Checkpoints

* [ ] **Personal Weather Proxy**
  Build a proxy API so multiple tools can share one upstream source:
  1. `GET /weather/{city}` ??fetches from `https://goweather.xyz/weather/{city}` (M11) and returns the parsed JSON.
  2. `GET /weather` (no city) ??returns `400` with `detail="Please provide a city in the path"`.
  3. On any upstream failure, return `502` with `detail="Upstream service unavailable"`.
  *(The "proxy" pattern insulates your clients from upstream changes ??the same idea behind API gateways like AWS API Gateway.)*

* [ ] **Habit Tracker REST API**
  Re-implement the habit tracker from M12 as a REST API:
  - `POST /habits` ??creates a habit, returns `201` + the new row.
  - `POST /habits/{habit_id}/checkins` ??marks done today; returns `409` if already logged today.
  - `GET /habits/{habit_id}/streak` ??returns `{"habit": "exercise", "current_streak": 7}`.
  - `GET /habits` ??returns all habits with their current streaks.
  Persist everything in SQLite.

* [ ] **AI Polish Service**
  Combine M16 (Ollama) + M13 (FastAPI):
  - `POST /polish` ??body `{"text": "rough draft??}`. Calls local Ollama, returns `{"polished": "??, "elapsed_seconds": 3.2}`.
  - If Ollama is unreachable, return `503` with a clear `detail`.
  Once working, update your M14 PySide app to call this endpoint instead of calling Ollama directly. You have just decoupled the UI from the AI ??any future frontend can share the same service.
