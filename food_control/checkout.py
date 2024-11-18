import json
import os

class Checkout:
    FILE_PATH = "tests/orders.json"
    PROVIDER_EARNINGS_PATH = "tests/provider_earnings.json"  # Path for provider earnings file

    def __init__(self):
        self.orders = self.load_orders()
        self.provider_earnings = self.load_provider_earnings()

    def load_orders(self):
        """Loads orders from a file, handles JSON and file errors."""
        if os.path.exists(self.FILE_PATH):
            try:
                with open(self.FILE_PATH, "r") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                print("Error: The file contains invalid JSON.")
            except Exception as e:
                print(f"Error loading orders: {e}")
        return []

    def load_provider_earnings(self):
        """Loads provider earnings from a file."""
        if os.path.exists(self.PROVIDER_EARNINGS_PATH):
            try:
                with open(self.PROVIDER_EARNINGS_PATH, "r") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                print("Error: The file contains invalid JSON.")
            except Exception as e:
                print(f"Error loading provider earnings: {e}")
        return {}

    def save_orders(self):
        """Saves orders to a file, with error handling."""
        try:
            with open(self.FILE_PATH, "w") as file:
                json.dump(self.orders, file, indent=4)
            print("Orders saved successfully.")
        except Exception as e:
            print(f"Error saving orders: {e}")

    def save_provider_earnings(self):
        """Saves provider earnings to a file."""
        try:
            with open(self.PROVIDER_EARNINGS_PATH, "w") as file:
                json.dump(self.provider_earnings, file, indent=4)
            print("Provider earnings saved successfully.")
        except Exception as e:
            print(f"Error saving provider earnings: {e}")

    def add_order(self, order):
        """Adds an order to the orders list, updates provider earnings, and saves data."""
        if self.validate_order(order):
            self.orders.append(order)
            self.update_provider_earnings(order)
            self.save_orders()
            self.save_provider_earnings()
        else:
            print("Invalid order. Cannot be added.")

    def update_provider_earnings(self, order):
        """Updates the provider's earnings based on the order's total cost."""
        provider_name = order['provider_name']
        total_cost = order['total_cost']

        if provider_name in self.provider_earnings:
            self.provider_earnings[provider_name] += total_cost
        else:
            self.provider_earnings[provider_name] = total_cost

    def validate_order(self, order):
        """Validates the order before adding."""
        required_fields = ['consumer_name', 'food_name', 'quantity', 'total_cost', 'provider_name']
        return all(field in order for field in required_fields)

    def generate_receipt(self, order):
        """Generates a receipt for a single order."""
        return f"Receipt for {order['consumer_name']}:\n" \
               f"Food: {order['food_name']}\n" \
               f"Quantity: {order['quantity']}\n" \
               f"Total Cost: ${order['total_cost']:.2f}\n" \
               f"Thank you for your purchase!"

    def generate_multiple_items_receipt(self, orders):
        """Generates a receipt for multiple items."""
        receipt = "Your Purchase Receipt:\n"
        total_cost = 0
        for order in orders:
            receipt += f"\nFood: {order['food_name']}\n" \
                       f"Quantity: {order['quantity']}\n" \
                       f"Total Cost: ${order['total_cost']:.2f}\n"
            total_cost += order['total_cost']
        receipt += f"\nTotal for all items: ${total_cost:.2f}\n" \
                   "Thank you for your purchase!"
        return receipt

