def view_profile(self):
    print(f"\n--- {self.username}'s Profile ---")
    if self.role == "provider":
        print(f"Location: {self.location}")
        print("Listings:")
        for idx, listing in enumerate(User.listings):
            if listing["provider"] == self:
                discounted_price = listing['price'] * (1 - listing['discount'] / 100)
                print(f"{idx + 1}. {listing['food_name']} - Quantity: {listing['quantity']} - "
                      f"Expires: {listing['expiration']} - Original Price: ${listing['price']:.2f} - "
                      f"Discounted Price: ${discounted_price:.2f}")
    elif self.role == "consumer":
        print("Favorites:")
        self.view_favorites()
        print("\nReserved Items:")
        self.view_reserved_items()
