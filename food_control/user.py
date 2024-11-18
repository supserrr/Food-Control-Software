import json
import re


def view_listings():
    print("\nAvailable Listings:")
    if not User.listings:
        print("No listings available.")
        return

    for idx, listing in enumerate(User.listings, start=1):
        discounted_price = listing['price'] * (1 - listing['discount'] / 100)
        print(f"{idx}. {listing['food_name']} - Quantity: {listing['quantity']} - "
              f"Expires: {listing['expiration']} - Original Price: ${listing['price']:.2f} - "
              f"Discounted Price: ${discounted_price:.2f}")


class User:
    users = []
    listings = []

    def __init__(self, username, email, password, role, location=None):
        self.username = username
        self.email = email
        self.password = password  # Store passwords in plain text
        self.role = role
        self.location = location
        self.reserved_items = []
        self.purchase_history = []  # Track past orders
        self.orders = []
        self.earnings = 0.0  # Initialize earnings for providers
        User.users.append(self)

    @staticmethod
    def is_valid_date(date_string):
        """Check if the given date string is in the format YYYY-MM-DD."""
        date_regex = r"^\d{4}-\d{2}-\d{2}$"
        return bool(re.match(date_regex, date_string))

    @classmethod
    def register(cls, username, email, password, role, location=None):
        for user in cls.users:
            if user.email == email:
                print("Email already registered.")
                return None

        user = cls(username, email, password, role, location)
        print(f"Registration successful! Logged in as {username}.")
        cls.save_data()
        return user

    @classmethod
    def login(cls, email, password):
        print("Attempting to log in...")  # Debug statement
        for user in cls.users:
            if user.email == email and user.password == password:
                print(f"Welcome back, {user.username}!")
                return user
        print("Invalid email or password.")
        return None

    @classmethod
    def load_data(cls):
        try:
            with open("tests/users.json", "r") as users_file:
                users_data = json.load(users_file)
                cls.users = [
                    User(
                        username=user_data['username'],
                        email=user_data['email'],
                        password=user_data['password'],
                        role=user_data['role'],
                        location=user_data.get('location')
                    ) for user_data in users_data
                ]
            with open("tests/listings.json", "r") as listings_file:
                cls.listings = json.load(listings_file)
        except FileNotFoundError:
            cls.users = []
            cls.listings = []

    @classmethod
    def save_data(cls):
        with open("tests/users.json", "w") as users_file:
            json.dump([user.__dict__ for user in cls.users], users_file, default=str)
        with open("tests/listings.json", "w") as listings_file:
            json.dump(cls.listings, listings_file)

    def menu(self):
        if self.role == "consumer":
            self.consumer_menu()
        elif self.role == "provider":
            self.provider_menu()

    def total_earnings(self):
        total = 0
        for listing in User.listings:
            if listing.get("quantity") < 1:
                total += listing["price"] * (1 - listing["discount"] / 100)
        return total

    def consumer_menu(self):
        while True:
            print("\n--- Consumer Menu ---")
            print("1. View Listings")
            print("2. Reserve Food")
            print("3. View Profile")
            print("4. Cart")
            print("5. Checkout")
            print("6. Logout")
            choice = input("Choose an option: ")
            if choice == "1":
                view_listings()
            elif choice == "2":
                self.reserve_food()
            elif choice == "3":
                self.view_profile()
            elif choice == "4":
                self.view_cart()
            elif choice == "5":
                self.checkout()
            elif choice == "6":
                print(f"Logging out {self.username}...")
                break
            else:
                print("Invalid choice, please try again.")

    def provider_menu(self):
        while True:
            print("\n--- Provider Menu ---")
            print("1. List Food")
            print("2. View Profile")
            print("3. Update Listings")
            print("4. Logout")
            choice = input("Choose an option: ")
            if choice == "1":
                self.list_food()
            elif choice == "2":
                self.view_profile()
            elif choice == "3":
                self.update_listing()
            elif choice == "4":
                print(f"Logging out {self.username}...")
                break
            else:
                print("Invalid choice, please try again.")

    def reserve_food(self):
        print("\nAvailable Listings for Reservation:")
        if not User.listings:
            print("No listings available.")
            return

        for idx, listing in enumerate(User.listings, start=1):
            print(f"{idx}. {listing['food_name']} - Quantity: {listing['quantity']}")

        choice = input("Enter the number of the item you want to reserve: ")
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(User.listings):
            print("Invalid selection.")
            return

        selected_listing = User.listings[int(choice) - 1]
        quantity_to_reserve = input("Enter the quantity to reserve: ")
        if not quantity_to_reserve.isdigit() or int(quantity_to_reserve) < 1:
            print("Invalid quantity.")
            return

        quantity_to_reserve = int(quantity_to_reserve)
        if quantity_to_reserve > selected_listing['quantity']:
            print("Not enough stock available.")
            return

        selected_listing['quantity'] -= quantity_to_reserve
        self.reserved_items.append({
            "food_name": selected_listing['food_name'],
            "quantity": quantity_to_reserve,
            "provider": selected_listing['provider'],
            "expiration": selected_listing['expiration']
        })
        print(f"You have reserved {quantity_to_reserve} of {selected_listing['food_name']}.")
        User.save_data()

    def view_cart(self):
        print("\n--- Your Cart ---")
        if not self.reserved_items:
            print("Your cart is empty.")
        else:
            for item in self.reserved_items:
                print(f"- {item['quantity']} of {item['food_name']} from {item['provider']} "
                      f"(Expires: {item['expiration']})")

    def list_food(self):
        food_name = input("Enter food name: ")
        quantity = input("Enter quantity: ")
        expiration = input("Enter expiration date (YYYY-MM-DD): ")
        price = input("Enter price: ")
        discount = input("Enter discount percentage: ")

        if not self.is_valid_date(expiration):
            print("Invalid expiration date format.")
            return

        food_listing = {
            "food_name": food_name,
            "quantity": int(quantity),
            "expiration": expiration,
            "price": float(price),
            "discount": float(discount),
            "provider": self.username
        }

        User.listings.append(food_listing)
        User.save_data()
        print(f"Food item '{food_name}' listed successfully.")

    def view_profile(self):
        print(f"\n--- Profile for {self.username} ---")
        print(f"Email: {self.email}")
        print("Past Orders:")
        if not self.purchase_history:
            print("No past orders.")
        else:
            for order in self.purchase_history:
                print(f"- {order['food_name']} x {order['quantity']} on {order['date']}")

    def checkout(self):
        if not self.reserved_items:
            print("Your cart is empty.")
            return

        total_cost = sum(
            item['quantity'] * next(l['price'] * (1 - l['discount'] / 100)
                                    for l in User.listings if l['food_name'] == item['food_name'])
            for item in self.reserved_items
        )

        print(f"Total cost: ${total_cost:.2f}")
        confirmation = input("Do you want to proceed with the payment? (yes/no): ")
        if confirmation.lower() != "yes":
            print("Checkout cancelled.")
            return

        for item in self.reserved_items:
            item['date'] = "2024-11-18"  # Example date
            self.purchase_history.append(item)

        self.reserved_items.clear()
        User.save_data()
        print("Payment successful. Thank you for your purchase!")


# Load data at the start
User.load_data()

