import csv
import json

products = []

with open("inventories.csv", mode="r", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        products.append({
            "id":       int(row["id"]),
            "name":     row["name"],
            "price":    float(row["price"]),
            "quantity": int(row["quantity"]),
        })

print(f"Read {len(products)} products from CSV.")
print("Sample:", products[0])

with open("inventory.json", mode="w", encoding="utf-8") as f:
    json.dump(products, f, indent=4, ensure_ascii=False)

print("Exported to inventory.json")

with open("inventory.json", mode="r", encoding="utf-8") as f:
    loaded = json.load(f)

total_value = sum(p["price"] * p["quantity"] for p in loaded)
print(f"\nInventory summary: {len(loaded)} products, total value: ${total_value:,.2f}")
