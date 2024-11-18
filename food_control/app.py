import json
from food_control.food_listing import FoodListing, FoodListingManager
from food_control.checkout import Checkout
from food_control.utils import save_data_to_file, load_data_from_file

class User:
    def __init__(self, name, email, role):
        self.name = name
        self.email = email
        self.role = role
        self.cart = []
        self.orders = []
        self.listings = []

    @classmethod
    def register(cls):
        name = input("Enter your username: ").strip()
        email = input("Enter your email: ").strip()
        password = input("Enter your password: ").strip()
        role = input("Enter your role (consumer/provider): ").strip().lower()
        location = input("Enter your location (optional): ").strip()
        user = cls(name, email, role)

        # Save user data to file
        users = load_from_file("tests/users.json")  # Load existing users
        users.append(user.__dict__)  # Append the new user to the list
        save_to_file("tests/users.json", users)  # Save back to file

        print(f"Registration successful! Logged in as {name}.")
        return user  # Return the user object after registration

    @classmethod
    def login(cls):
        email = input("Enter your email: ").strip()
        password = input("Enter your password: ").strip()

        # Load all users from file
        users = load_from_file("tests/users.json")
        for entry in users:
            if entry["email"] == email:
                return cls(entry["name"], entry["email"], entry["role"])  # Ensure 'name' is set
        print("Invalid login credentials.")
        return None

    def view_listings(self):
        manager = FoodListingManager()
        data = manager.listings
        if data:
            print("\nAvailable Listings:")
            for index, item in enumerate(data, start=1):
                print(f"{index}. {item.name} - Quantity: {item.quantity} - Expires: {item.expiration_date} "
                      f"- Original Price: ${item.price} - Discount: {item.discount}%")
        else:
            print("No listings available.")

    def reserve_food(self):
        food_name = input("Enter food name: ").strip()
        try:
            quantity = int(input("Enter quantity: ").strip())
            # Simulating food reservation logic here...
            manager = FoodListingManager()
            food_item = next((item for item in manager.listings if item.name == food_name), None)
            if food_item and food_item.quantity >= quantity:
                food_item.quantity -= quantity
                print(f"Successfully reserved {quantity} of {food_name}.")
                self.cart.append((food_name, quantity))  # Add to cart
            else:
                print("Insufficient quantity or food not found.")
        except ValueError:
            print("Invalid quantity. Please enter a valid number.")

    def view_profile(self):
        print(f"\n--- {self.name}'s Profile ---\nEmail: {self.email}")
        if self.orders:
            print("\nPast Orders:")
            for order in self.orders:
                print(f"- {order}")
        else:
            print("\nPast Orders:\nNo past orders.")

    def view_cart(self):
        if not self.cart:
            print("\n--- Your Cart ---\nYour cart is empty.")
        else:
            print("\n--- Your Cart ---")
            for item in self.cart:
                print(f"{item[0]} - Quantity: {item[1]}")
            checkout = input("Would you like to proceed to checkout? (y/n): ").strip().lower()
            if checkout == 'y':
                self.checkout()

    def checkout(self):
        # Placeholder checkout functionality
        print("Processing checkout...")
        total_price = 0
        for food_name, quantity in self.cart:
            manager = FoodListingManager()
            food_item = next((item for item in manager.listings if item.name == food_name), None)
            if food_item:
                total_price += food_item.price * quantity
        print(f"Total Price: ${total_price}")
        self.orders.append(f"Total: ${total_price}")
        self.cart.clear()

    def list_food(self):
        name = input("Enter food name: ").strip()
        try:
            quantity = int(input("Enter quantity: ").strip())
            expiry_date = input("Enter expiration date (YYYY-MM-DD): ").strip()
            price = float(input("Enter price: ").strip())
            discount = float(input("Enter discount (%): ").strip())
            listing = FoodListing(name, quantity, expiry_date, price, discount)
            manager = FoodListingManager()
            manager.add_listing(listing)
            print("Food listed successfully.")
        except ValueError:
            print("Invalid input. Please try again.")

    def view_notifications(self):
        # Placeholder for notifications
        print("\n--- Notifications ---")
        # Notifications can be displayed here, such as order confirmations.
        pass

    def update_listings(self):
        manager = FoodListingManager()
        if manager.listings:
            print("Select a listing to update:")
            for index, item in enumerate(manager.listings, start=1):
                print(f"{index}. {item.name}")
            try:
                choice = int(input("Enter your choice: ").strip())
                if 1 <= choice <= len(manager.listings):
                    # Implement update logic here
                    item = manager.listings[choice - 1]
                    print(f"Updating {item.name}")
                    new_price = float(input(f"Enter new price for {item.name}: ").strip())
                    new_quantity = int(input(f"Enter new quantity for {item.name}: ").strip())
                    item.price = new_price
                    item.quantity = new_quantity
                    print(f"Updated {item.name} - Price: ${item.price} - Quantity: {item.quantity}")
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Invalid choice. Please enter a valid number.")
        else:
            print("No listings to update.")
