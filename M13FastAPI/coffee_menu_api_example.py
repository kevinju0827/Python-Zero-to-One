"""Guided Practice 1 — A small coffee-shop menu API.

Scenario: a single source of truth for a café's drinks list, served as
JSON so any future app (mobile, web, Slack bot) can fetch from it.

Run with:
    uvicorn coffee_menu_api_example:app --reload
or simply:
    python coffee_menu_api_example.py
Then open  http://127.0.0.1:8000/docs  to try the endpoints.
"""

from fastapi import FastAPI, HTTPException

app = FastAPI(title="Mini Coffee Menu API")

# In a real deployment this would live in a database (see Practice 3).
# A module-level dict is enough to learn the routing concepts.
MENU: dict[str, dict] = {
    "1": {"name": "Latte",      "price": 4.5, "in_stock": True},
    "2": {"name": "Espresso",   "price": 3.0, "in_stock": True},
    "3": {"name": "Cappuccino", "price": 4.0, "in_stock": False},
    "4": {"name": "Cold Brew",  "price": 5.0, "in_stock": True},
}


@app.get("/")
def read_root() -> dict:
    return {"message": "Welcome to the coffee shop API. See /docs for routes."}


@app.get("/menu")
def list_menu() -> dict:
    """Return the whole menu so a client can render it as a list."""
    return MENU


@app.get("/menu/search")
def search_menu(q: str) -> list[dict]:
    """Case-insensitive substring search on drink names.

    Important: this route must be DEFINED BEFORE /menu/{drink_id}.
    FastAPI matches routes top-down, so the literal '/menu/search' would
    otherwise be captured by the dynamic '{drink_id}' route.
    """
    needle = q.lower()
    return [drink for drink in MENU.values() if needle in drink["name"].lower()]


@app.get("/menu/{drink_id}")
def get_drink(drink_id: str) -> dict:
    drink = MENU.get(drink_id)
    if drink is None:
        # 404 is the correct semantic for 'I looked, nothing exists'.
        raise HTTPException(status_code=404, detail=f"Drink {drink_id} not found")
    return drink


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
