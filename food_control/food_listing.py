import json
import os

class FoodListing:
    def __init__(self, name, quantity, expiration_date, price, discount, reserved_by=None):
        self.name = name
        self.quantity = quantity
        self.expiration_date = expiration_date
        self.price = price
        self.discount = discount
        self.reserved_by = reserved_by

    def to_dict(self):
        return {
            "name": self.name,
            "quantity": self.quantity,
            "expiration_date": self.expiration_date,
            "price": self.price,
            "discount": self.discount,
            "reserved_by": self.reserved_by
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["name"],
            data["quantity"],
            data["expiration_date"],
            data["price"],
            data["discount"],
            data.get("reserved_by")
        )

class FoodListingManager:
    FILE_PATH = "tests/food_listings.json"

    def __init__(self):
        self.listings = self.load_listings()

    def load_listings(self):
        """Loads food listings from a file, with error handling."""
        if os.path.exists(self.FILE_PATH):
            try:
                with open(self.FILE_PATH, "r") as file:
                    return [FoodListing.from_dict(item) for item in json.load(file)]
            except json.JSONDecodeError:
                print("Error loading food listings: Invalid JSON format.")
                return []
            except Exception as e:
                print(f"Error loading food listings: {e}")
                return []
        return []

    def save_listings(self):
        """Saves the food listings to a file."""
        try:
            with open(self.FILE_PATH, "w") as file:
                json.dump([item.to_dict() for item in self.listings], file, indent=4)
        except Exception as e:
            print(f"Error saving food listings: {e}")

    def add_listing(self, listing):
        """Adds a food listing and saves it to the file."""
        self.listings.append(listing)
        self.save_listings()

    def get_listings_by_provider(self, provider_name):
        """Returns food listings for a specific provider."""
        return [listing for listing in self.listings if listing.reserved_by == provider_name]

    def update_listing(self, name, quantity=None, expiration_date=None, price=None, discount=None):
        """Updates a food listing based on the provided attributes."""
        for listing in self.listings:
            if listing.name == name:
                if quantity is not None:
                    listing.quantity = quantity
                if expiration_date is not None:
                    listing.expiration_date = expiration_date
                if price is not None:
                    listing.price = price
                if discount is not None:
                    listing.discount = discount
                self.save_listings()
                return True
        return False

    def reserve_food(self, name, consumer_name, quantity):
        """Reserves a specific quantity of food for a consumer."""
        for listing in self.listings:
            if listing.name == name and listing.quantity >= quantity:
                if listing.reserved_by:
                    print(f"Food item '{name}' is already reserved.")
                    return False
                listing.quantity -= quantity
                listing.reserved_by = consumer_name
                self.save_listings()
                print(f"{quantity} of '{name}' has been reserved for {consumer_name}.")
                return True
        print(f"Food item '{name}' not found or insufficient quantity.")
        return False

