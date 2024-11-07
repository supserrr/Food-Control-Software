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
