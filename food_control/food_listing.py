def list_food(self, food_name, quantity, expiration, price, discount):
    listing = {
        "provider": self,
        "food_name": food_name,
        "quantity": quantity,
        "expiration": expiration,
        "price": price,
        "discount": discount
    }
    User.listings.append(listing)
    print(f"{food_name} has been listed successfully.")

def reserve_food(self, food_name, quantity):
    for listing in User.listings:
        if listing["food_name"].lower() == food_name.lower() and listing["quantity"] >= quantity:
            listing["quantity"] -= quantity
            self.reserved_items.append({"food_name": food_name, "quantity": quantity, "price": listing["price"], "discount": listing["discount"]})
            print(f"Reserved {quantity} of {food_name}.")
            return
    print("Invalid food name or quantity exceeds available stock.")
