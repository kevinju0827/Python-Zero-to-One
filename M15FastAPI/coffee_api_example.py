from fastapi import FastAPI
import uvicorn

# 1. Create the FastAPI application instance
app = FastAPI()

# Sample Data (Mocking a database like M10)
menu = {
    "1": {"name": "Latte", "price": 4.5, "in_stock": True},
    "2": {"name": "Espresso", "price": 3.0, "in_stock": True},
    "3": {"name": "Cappuccino", "price": 4.0, "in_stock": False}
}

# 2. Define a root route (home page)
@app.get("/")
def read_root():
    return {"message": "Welcome to the Python Coffee Shop API!"}

# 3. Define a dynamic route using a Path Parameter {item_id}
@app.get("/items/{item_id}")
def get_item(item_id: str):
    """Retrieves coffee information based on its ID."""
    if item_id in menu:
        return menu[item_id]
    else:
        # Return a custom error message
        return {"error": "Item not found in our coffee menu."}

# 4. Entry point to run the app directly
# In a terminal, you would normally run: uvicorn coffee_api_example:app --reload
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
