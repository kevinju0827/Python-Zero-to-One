# M15 FastAPI (Web Services)

## The "Why?"

If you want to share your Python logic with the world—maybe as the backend for a mobile app or a dashboard for your company—you need to build a **Web API**. **FastAPI** is currently the most popular modern framework for building these services. It is incredibly fast, easy to learn, and automatically generates interactive documentation for you. With FastAPI, you can turn your Python functions into "endpoints" that anyone with an internet connection can communicate with.

## Goals

Learn how to set up a web server, create "routes" (URLs), and handle data parameters sent to your server via the web.

## Core Concepts

### Uvicorn
FastAPI is the framework where you write your code, but **Uvicorn** is the actual "web server" that runs it. It listens for incoming web requests and hands them over to your Python functions.

### Path Parameters
You can capture values directly from the URL. For example, in `myapp.com/users/kevin`, "kevin" is a parameter that your script can capture and use to look up a specific user in a database.

### Automatic Documentation (Swagger)
One of FastAPI's best features is that it automatically creates a "Swagger" page (at `/docs`) where you can see all your available API endpoints and test them without writing any extra code.

## Guided Practice

We will build a **Digital Menu API** for a coffee shop. When someone visits our URL, we will send them a JSON list of our drinks and their prices.

*   **Step 1: Install FastAPI and Uvicorn**
    ```bash
    pip install fastapi uvicorn
    ```

*   **Step 2: Create `coffee_api_example.py`**
    ```python
    from fastapi import FastAPI

    app = FastAPI()

    # Sample Data (In a real app, this would come from M10 Database)
    menu = {
        "1": {"name": "Latte", "price": 4.5, "in_stock": True},
        "2": {"name": "Espresso", "price": 3.0, "in_stock": True},
        "3": {"name": "Cappuccino", "price": 4.0, "in_stock": False}
    }

    @app.get("/")
    def read_root():
        return {"message": "Welcome to the Python Coffee Shop API!"}

    @app.get("/items/{item_id}")
    def get_item(item_id: str):
        if item_id in menu:
            return menu[item_id]
        return {"error": "Item not found"}
    ```

*   **Step 3: Run the server**
    In your terminal, run:
    ```bash
    uvicorn coffee_api_example:app --reload
    ```
    Open your browser to `http://127.0.0.1:8000/docs` to see the interactive documentation.

## Checkpoints

* [ ] **The Personal Greeting API**:
    Create a new route `/hello/{name}` that returns a JSON message: `{"greeting": "Hello, [name]!"}`.
* [ ] **The Summation Service**:
    Create a route `/add/{num1}/{num2}` that takes two numbers from the URL, adds them together, and returns the result in JSON format.
* [ ] **Inventory Link**:
    Combine this with M08 (Data Format). Modify the API to read your `inventory.json` file and create a route `/inventory` that displays the entire list of products as a JSON response.