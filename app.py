from user import User
from utils import get_valid_float, get_valid_int

def user_menu(user):
    if user.role == "provider":
        print("\n1. List Food\n2. View Profile\n3. Logout")
    elif user.role == "consumer":
        print("\n1. View Listings\n2. Reserve Food\n3. View Profile\n4. Checkout\n5. Logout")
    return input("Choose an option: ")

def run_app():
    logged_in = False
    user = None

    while True:
        if not logged_in:
            print("\nWelcome to the Food Waste Control App!")
            print("1. Register\n2. Login\n3. Exit")
            choice = input("Choose an option: ")

            if choice == '1':  # Register
                username = input("Enter username: ")
                email = input("Enter email: ")
                password = input("Enter password: ")
                role = input("Enter role (provider/consumer): ").strip().lower()
                location = input("Enter location (for providers only): ") if role == "provider" else None
                user = User.register(username, email, password, role, location)
                logged_in = True

            elif choice == '2':  # Login
                email = input("Enter email: ")
                password = input("Enter password: ")
                user = User.login(email, password)
                logged_in = bool(user)

            elif choice == '3':  # Exit
                print("Exiting the application.")
                break

            else:
                print("Invalid option. Please try again.")
        else:
            action = user_menu(user)

            if action == '1' and user.role == "provider":  # List food for providers
                food_name = input("Enter food name: ")
                quantity = get_valid_int("Enter quantity: ")
                expiration = input("Enter expiration date (YYYY-MM-DD): ")
                price = get_valid_float("Enter original price: ")
                discount = get_valid_float("Enter discount percentage: ")
                user.list_food(food_name, quantity, expiration, price, discount)

            elif action == '2' and user.role == "provider":  # View profile for providers
                user.view_profile()

            elif action == '3' and user.role == "provider":  # Logout for providers
                print("Logging out...")
                logged_in = False

            elif action == '1' and user.role == "consumer":  # View listings for consumers
                location = input("Enter location to filter by (or press Enter for all): ").strip()
                location = location if location else None
                user.view_listings(location)

            elif action == '2' and user.role == "consumer":  # Reserve food for consumers
                food_name = input("Enter the name of the food item you wish to reserve: ")
                quantity = get_valid_int(f"Enter quantity for {food_name}: ")
                user.reserve_food(food_name, quantity)

            elif action == '3' and user.role == "consumer":  # View profile for consumers
                user.view_profile()

            elif action == '4' and user.role == "consumer":  # Checkout for consumers
                user.checkout()

            elif action == '5' and user.role == "consumer":  # Logout for consumers
                print("Logging out...")
                logged_in = False

            else:
                print("Invalid choice. Please try again.")

# Start the application
run_app()
