class OrderItem:
    def __init__(self, name, price, quantity):
        self.name     = name
        self.price    = price
        self.quantity = quantity

    def total(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.name} x{self.quantity} @ ${self.price:.2f} = ${self.total():.2f}"


class Order:
    def __init__(self, order_id):
        self.order_id = order_id
        self.items    = []

    def add_item(self, item):
        self.items.append(item)

    def total(self):
        return sum(item.total() for item in self.items)

    def show(self):
        print(f"\n=== Order #{self.order_id} ===")
        if not self.items:
            print("  No items.")
            return
        for item in self.items:
            print(f"  {item}")
        print(f"  {'-' * 32}")
        print(f"  Total: ${self.total():.2f}")

    def __str__(self):
        return f"Order #{self.order_id} | {len(self.items)} item(s) | Total: ${self.total():.2f}"


class DiscountOrder(Order):
    def __init__(self, order_id, discount_rate):
        super().__init__(order_id)
        self.discount_rate = discount_rate

    def total(self):
        return super().total() * (1 - self.discount_rate)

    def show(self):
        print(f"\n=== Order #{self.order_id} (Discount: {self.discount_rate:.0%}) ===")
        if not self.items:
            print("  No items.")
            return
        for item in self.items:
            print(f"  {item}")
        subtotal = super().total()
        print(f"  {'-' * 32}")
        print(f"  Subtotal: ${subtotal:.2f}")
        print(f"  Discount: -${subtotal * self.discount_rate:.2f}")
        print(f"  Total:    ${self.total():.2f}")


if __name__ == "__main__":
    order = Order(1001)
    order.add_item(OrderItem("Laptop",      999.00, 1))
    order.add_item(OrderItem("Mouse",        29.99, 2))
    order.add_item(OrderItem("USB-C Cable",   9.99, 3))
    order.show()
    print(order)

    promo = DiscountOrder(1002, discount_rate=0.10)
    promo.add_item(OrderItem("Keyboard", 79.99, 1))
    promo.add_item(OrderItem("Monitor",  299.99, 1))
    promo.show()
