from food_control.user import User

def main():
    print("\n--- Welcome to the Food Waste Control System ---")
    while True:
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")


def register():
    username = input("Enter your username: ")
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    role = input("Enter your role (consumer/provider): ")

    # Optional: Request location if needed
    location = input("Enter your location (optional): ") or None

    user = User.register(username, email, password, role, location)
    if user:
        user_menu(user)


def login():
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    user = User.login(email, password)
    if user:
        user_menu(user)


def user_menu(user):
    """Displays the menu for the logged-in user."""
    if user is None:
        print("No user logged in.")
        return  # Handle appropriately if no user is logged in

    if user.role == "consumer":
        consumer_menu(user)
    elif user.role == "provider":
        provider_menu(user)


def consumer_menu(user):
    """Menu for the consumer."""
    while True:
        print("\n--- Consumer Menu ---")
        print("1. View Listings")
        print("2. Reserve Food")
        print("3. View Profile")
        print("4. Cart")
        print("5. Logout")
        choice = input("Choose an option: ")

        if choice == "1":
            view_listings()
        elif choice == "2":
            reserve_food(user)
        elif choice == "3":
            consumer_profile(user)
        elif choice == "4":
            view_cart(user)
        elif choice == "5":
            print(f"Logging out {user.username}...")
            break
        else:
            print("Invalid choice, please try again.")


def provider_menu(user):
    """Menu for the provider."""
    while True:
        print("\n--- Provider Menu ---")
        print("1. List Food")
        print("2. View Profile")
        print("3. Update Listings")
        print("4. Logout")
        choice = input("Choose an option: ")

        if choice == "1":
            list_food(user)
        elif choice == "2":
            provider_profile(user)
        elif choice == "3":
            update_listings(user)
        elif choice == "4":
            print(f"Logging out {user.username}...")
            break
        else:
            print("Invalid choice, please try again.")


def view_listings():
    """Function to view food listings."""
    if not User.listings:
        print("No listings available.")
    for idx, listing in enumerate(User.listings, start=1):
        discounted_price = listing['price'] * (1 - listing['discount'] / 100)
        print(f"{idx}. {listing['food_name']} - Quantity: {listing['quantity']} - Expires: {listing['expiration']} "
              f"- Original Price: ${listing['price']:.2f} - Discounted Price: ${discounted_price:.2f}")


def reserve_food(user):
    """Reserve food items."""
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

    # Add to reserved items before reducing stock
    user.reserved_items.append({
        "food_name": selected_listing['food_name'],
        "quantity": quantity_to_reserve,
        "provider": selected_listing['provider'],
        "expiration": selected_listing['expiration']
    })

    # Do not reduce stock until checkout
    print(f"You have reserved {quantity_to_reserve} of {selected_listing['food_name']}.")
    User.save_data()


def view_cart(user):
    """Display items in the cart."""
    print("\n--- Your Cart ---")
    if not user.reserved_items:
        print("Your cart is empty.")
        return

    for item in user.reserved_items:
        print(f"{item['food_name']} - Quantity: {item['quantity']} - Expires: {item['expiration']}")

    checkout_option = input("\nDo you want to proceed to checkout? (y/n): ")
    if checkout_option.lower() == 'y':
        checkout(user)


def checkout(user):
    """Handle the checkout process."""
    if not user.reserved_items:
        print("Your cart is empty!")
        return

    total_cost = 0
    provider_earnings = {}

    # Calculate total cost and prepare to update earnings
    for item in user.reserved_items:
        food = next(f for f in User.listings if f['food_name'] == item['food_name'])
        discounted_price = food['price'] * (1 - food['discount'] / 100)
        cost = discounted_price * item['quantity']
        total_cost += cost

        # Track earnings for each provider
        provider = food['provider']
        if provider in provider_earnings:
            provider_earnings[provider] += cost
        else:
            provider_earnings[provider] = cost

    print(f"\nTotal cost: ${total_cost:.2f}")

    # Simulate payment methods
    print("\n--- Choose Payment Method ---")
    print("1. Credit Card")
    print("2. PayPal")
    print("3. Cash")
    payment_choice = input("Choose a payment method (1/2/3): ")
    if payment_choice in ['1', '2', '3']:
        print("Payment successful!")

        # Deduct quantities from stock and update provider earnings
        for item in user.reserved_items:
            food = next(f for f in User.listings if f['food_name'] == item['food_name'])
            food['quantity'] -= item['quantity']

        # Update total earnings for each provider
        for provider_name, earnings in provider_earnings.items():
            provider = next(u for u in User.users if u.username == provider_name)  # Corrected here
            provider.earnings += earnings  # Add earnings to the provider's total

        user.purchase_history.append(user.reserved_items)  # Add to past orders
        user.reserved_items.clear()  # Clear cart after successful checkout

        # Save user data to persist the changes (assuming User.save_data() handles persistence)
        User.save_data()

        print("Thank you for your purchase!")
    else:
        print("Invalid payment method.")


def consumer_profile(user):
    """Display the consumer's profile."""
    print("\n--- Profile ---")
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    print(f"Past Orders:")
    if user.purchase_history:
        for order in user.purchase_history:
            print(f"- {order}")
    else:
        print("No past orders.")
    print(f"Reserved Items:")
    if user.reserved_items:
        for item in user.reserved_items:
            print(f"- {item['food_name']} ({item['quantity']}) from {item['provider']} - Expires: {item['expiration']}")
    else:
        print("No items reserved.")


def provider_profile(user):
    print(f"--- {user.username}'s Profile ---")
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")

    # Display total earnings for the provider
    print(f"Total Earnings: ${user.total_earnings():.2f}")

    print("\nStock Summary:")
    if user.listings:
        for listing in user.listings:
            print(f"{listing['food_name']} ({listing['quantity']} left)")
    else:
        print("No stock available.")

    print("\nNotifications:")
    print("No new notifications.")


def list_food(user):
    """Allow provider to list food items."""
    food_name = input("Enter food name: ")
    quantity = input("Enter quantity: ")
    expiration = input("Enter expiration date (YYYY-MM-DD): ")
    price = float(input("Enter price: "))
    discount = float(input("Enter discount percentage: "))

    if not quantity.isdigit() or int(quantity) <= 0:
        print("Invalid quantity.")
        return

    user.listings.append({
        "food_name": food_name,
        "quantity": int(quantity),
        "expiration": expiration,
        "price": price,
        "discount": discount,
        "provider": user.username
    })

    User.save_data()  # Assuming this method persists the listings

    print(f"{food_name} has been listed successfully.")


def update_listings(user):
    """Allow provider to update food listings."""
    print("\n--- Update Listings ---")
    if not user.listings:
        print("No listings available.")
        return

    for idx, listing in enumerate(user.listings, start=1):
        print(f"{idx}. {listing['food_name']} - Quantity: {listing['quantity']}")

    choice = input("Enter the number of the listing you want to update: ")
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(user.listings):
        print("Invalid selection.")
        return

    selected_listing = user.listings[int(choice) - 1]
    new_quantity = input(f"Enter new quantity for {selected_listing['food_name']}: ")
    if not new_quantity.isdigit() or int(new_quantity) < 0:
        print("Invalid quantity.")
        return

    selected_listing['quantity'] = int(new_quantity)
    User.save_data()  # Save the updated listings
    print(f"{selected_listing['food_name']} has been updated to {new_quantity} items.")


if __name__ == "__main__":
    main()