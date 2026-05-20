# M15 FastAPI (Web Services)

## The "Why?"

Up to this point, you have been the **client**. In M09 you sent requests to JSONPlaceholder and Frankfurter; in M12 you posted prompts to Ollama. Someone else built the server, and you talked to it.

Now you will sit on the other side of the conversation. You will build the **server**—the program that listens for incoming requests, runs your Python logic, and returns structured JSON to whoever calls it. This is what makes it possible to share your work with the world. A mobile app, a JavaScript front-end, a spreadsheet macro in a colleague's Excel file, or even an LLM tool-call—any of them can become a client of your Python code once it is wrapped in an API.

**FastAPI** is, by a wide margin, the most popular modern Python framework for this job. It is fast (built on top of Starlette and Pydantic), it generates beautiful interactive documentation for you automatically, and its syntax is intentionally close to writing ordinary Python functions with type hints. Companies including Netflix, Uber, and Microsoft use it in production. By the end of this module, you will have built a small but real API of your own—the same architecture that powers the SaaS products you use every day.

## Goals

By the end of this module, you should be able to:

* Install FastAPI and Uvicorn and run a development server.
* Explain the role of FastAPI (the framework) vs. Uvicorn (the server that runs it).
* Define routes for `GET`, `POST`, `PUT`, and `DELETE` requests.
* Capture **path parameters** (`/items/{item_id}`) and **query parameters** (`?q=...&limit=...`).
* Use **Pydantic models** to validate the shape of request bodies for `POST`/`PUT`.
* Return correct HTTP status codes (`201 Created`, `404 Not Found`, etc.) using `HTTPException`.
* Read your API through the auto-generated Swagger UI at `/docs`.
* Combine FastAPI with M10 (SQLite) to expose a database over HTTP.

## Core Concepts

### FastAPI and Uvicorn: What Each One Does

A web API is two layers stacked on top of each other:

* **FastAPI** is the **framework**—the Python code where you describe the URLs your API responds to, the data it accepts, and the responses it returns. It does not actually open a network port by itself.
* **Uvicorn** is the **server**—the program that opens a TCP port (usually 8000), listens for incoming HTTP requests, hands each request to your FastAPI app, and sends the response back to the client.

In development you run them together. The standard command is:

```bash
uvicorn main:app --reload
```

The `--reload` flag restarts the server whenever you save a file, which makes the develop-test loop almost instant.

Install both with:

```bash
pip install fastapi "uvicorn[standard]"
```

---

### Your First Route

A FastAPI app is just a Python object decorated with route handlers:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, world!"}
```

`@app.get("/")` says: *"when someone makes a `GET` request to the root URL, call the function below."* The return value (a Python dict) is automatically serialized to JSON.

Run with `uvicorn main:app --reload`, then open `http://127.0.0.1:8000/` in a browser. You will see your JSON.

---

### Auto-Generated Docs: Your Best Friend

The single best feature of FastAPI is at `http://127.0.0.1:8000/docs`—an interactive Swagger UI generated automatically from your code. You can read every endpoint you have defined, try each one with sample inputs, and see the actual JSON response, all without writing a line of front-end code.

Get into the habit of opening `/docs` immediately after starting the server. It is the fastest way to confirm the API is doing what you think it is.

---

### Path Parameters

Anything in curly braces inside the URL is captured as an argument to your function:

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id, "name": "placeholder"}
```

The `: int` type hint is not cosmetic—FastAPI uses it to **validate** the input. If someone calls `/users/abc`, they will automatically get a clean 422 error response explaining that `user_id` must be an integer. You did not have to write that check yourself.

---

### Query Parameters

Function arguments that aren't part of the path become query parameters:

```python
@app.get("/search")
def search(q: str, limit: int = 10):
    return {"query": q, "limit": limit}
```

Calling `GET /search?q=python&limit=5` will invoke `search(q="python", limit=5)`. The default value (`= 10`) makes that parameter optional.

---

### Pydantic Models: Validated Request Bodies

For `POST` and `PUT` requests, the client typically sends a JSON object in the request body. You describe that object using a **Pydantic model**:

```python
from pydantic import BaseModel

class NewBook(BaseModel):
    title: str
    author: str
    rating: int

@app.post("/books")
def add_book(book: NewBook):
    return {"saved": book.title, "by": book.author}
```

Now, if a client sends `{"title": "Dune"}` with no `author` or `rating`, FastAPI rejects the request with a clear error message—again, without you writing the validation yourself.

Inside your function, `book` is a regular Python object: `book.title`, `book.author`, `book.rating`.

---

### Returning the Right Status Codes

By default, every successful response is `200 OK`. For other cases you have two tools:

* **Set the default status code per route**:
  ```python
  @app.post("/books", status_code=201)
  def add_book(book: NewBook): ...
  ```

* **Raise an `HTTPException` to signal a failure**:
  ```python
  from fastapi import HTTPException

  @app.get("/users/{user_id}")
  def get_user(user_id: int):
      if user_id not in database:
          raise HTTPException(status_code=404, detail="User not found")
      return database[user_id]
  ```

Returning the right status codes is the difference between an API people enjoy using and one they curse at. A 404 for "not found" lets clients reliably distinguish "nothing exists" from "the server is broken."

---

### Persisting Data: Combining FastAPI with SQLite

In real applications, your API is the doorway in front of a database. The pattern is straightforward: each route opens a SQLite connection, runs a query, and returns the result.

```python
import sqlite3
from fastapi import FastAPI

app = FastAPI()

def get_db():
    conn = sqlite3.connect("expenses.db")
    conn.row_factory = sqlite3.Row    # Returns dict-like rows instead of tuples
    return conn

@app.get("/expenses")
def list_expenses():
    conn = get_db()
    rows = conn.execute("SELECT * FROM expenses").fetchall()
    conn.close()
    return [dict(row) for row in rows]
```

The combination of M10 (SQL) and M15 (FastAPI) is the single most common backend pattern in the industry.

---

## Guided Practice

We will build a **mini coffee-shop menu API**—a service that exposes a café's drink list as JSON so any future client (a mobile app, a website, a Slack bot) can fetch from one source of truth. It exercises every FastAPI concept above: multiple routes, path parameters, query parameters, `HTTPException`, and the auto-generated `/docs` page.

**Scenario**: A friend opening a small café wants to publish their menu in a programmer-friendly format. We will build the simplest possible version—an in-memory dictionary served through a clean REST interface.

**Step 1: Define the data.** A module-level `MENU: dict[str, dict]` keyed by drink id. Each value holds `name`, `price`, and `in_stock`. In a real service this would come from M10's database (see this module's checkpoints), but a dict is enough to focus on routing.

**Step 2: Implement `GET /menu`.** Return the whole `MENU` dict. FastAPI serialises it to JSON automatically.

**Step 3: Implement `GET /menu/search?q=...`.** Take `q` as a query parameter (a function argument that isn't part of the path). Do a case-insensitive substring match on each drink's `name`. **Important**: this route must be defined *before* the `{drink_id}` route below—FastAPI matches routes top-down, so `/menu/search` would otherwise be captured as a drink id of `"search"`.

**Step 4: Implement `GET /menu/{drink_id}`.** `drink_id` becomes a function argument. If the id isn't in the dict, raise `HTTPException(status_code=404, detail="...")` instead of returning a plain dict—the right status code is what makes an API feel professional.

**Step 5: Run and explore `/docs`.** Run with `python coffee_menu_api_example.py` (or `uvicorn coffee_menu_api_example:app --reload`). Open `http://127.0.0.1:8000/docs`, expand each endpoint, click *"Try it out"* and execute. The auto-generated documentation page is the moment your code feels like a real online service.

The full implementation is in `coffee_menu_api_example.py`. Pay attention to the route order—it is the single most common gotcha for newcomers.

---

## Checkpoints

* [ ] **Personal Weather Proxy**:
      You want to build several small tools (a desktop widget, an LLM tool, a Slack bot) that all need weather data, but you don't want every one of them to hit the upstream API independently—if the upstream changes its URL or quota, you'd have to fix all of them. Build a *proxy* API:
      1. `GET /weather/{city}` accepts a city name, calls `https://goweather.xyz/weather/{city}` internally (recall M09), and returns the parsed JSON.
      2. On any failure to reach the upstream, return a 502 (`HTTPException(status_code=502, detail="Upstream weather service unavailable")`).
      3. `GET /weather` (no city) returns a 400 with `detail="Please provide a city in the path"`.
      *(Hint: the "proxy" pattern is one of the most common things APIs do in production—wrapping flaky third-party services in your own reliable interface. This is the same architecture used by API gateways like Kong or AWS API Gateway, just much smaller.)*

* [ ] **Habit Tracker REST API**:
      Re-implement the habit tracker from M10's last checkpoint as a REST API instead of a terminal script. Endpoints:
      * `POST /habits` — body `{"name": "exercise"}`. Creates a new habit. Returns 201 plus the habit row.
      * `POST /habits/{habit_id}/checkins` — marks the habit as done today. Returns 200, or 409 if today is already logged.
      * `GET /habits/{habit_id}/streak` — returns `{"habit": "exercise", "current_streak": 7}`.
      * `GET /habits` — returns the full list of habits with their current streaks.
      Persist everything in SQLite. Each endpoint should return the correct status code (201 on create, 404 on missing habit, 409 on duplicate check-in).
      *(Hint: a "REST API" is partly defined by *predictable* behavior—someone reading your endpoint list should be able to guess what each one does without asking you. That predictability is what makes a service feel professional.)*

* [ ] **Headless AI Polish Service**:
      Combine M12 + M15. Build an API in front of your Ollama email polisher:
      * `POST /polish` — body `{"text": "rough email..."}`. Internally calls the local Ollama API, returns `{"polished": "..."}`.
      * Time the call and return the elapsed seconds in the response: `{"polished": "...", "elapsed_seconds": 4.31}`.
      * If Ollama is unreachable, return a 503 with a clear `detail` field so clients know the model is offline.
      Once it works, point your M13 PySide app at this new endpoint instead of calling Ollama directly. You have just decoupled the **UI** from the **AI**—any new front-end (a web page, a mobile app, a Discord bot) can now share the same service. This separation of concerns is exactly how real software companies are structured.
