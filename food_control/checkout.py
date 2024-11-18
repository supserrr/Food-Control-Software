def checkout(self):
    if not self.reserved_items:
        print("No items to checkout.")
        return

    print("\n--- Order Summary ---")
    total_amount = 0
    for item in self.reserved_items:
        discounted_price = item['price'] * (1 - item['discount'] / 100)
        item_total = discounted_price * item['quantity']
        total_amount += item_total
        print(f"{item['food_name']} - Quantity: {item['quantity']} - Original Price: ${item['price']:.2f} - "
              f"Discounted Price: ${discounted_price:.2f} - Subtotal: ${item_total:.2f}")
    print(f"\nTotal amount to pay: ${total_amount:.2f}")

    payment_choice = input("Choose a payment option (1-Credit Card, 2-PayPal, 3-Cash): ").strip()

    if payment_choice == '1':
        card_number = input("Enter your credit card number: ")
        print("Processing payment...")
    elif payment_choice == '2':
        paypal_email = input("Enter PayPal email: ")
        print("Processing PayPal payment...")
    elif payment_choice == '3':
        print("Payment by cash selected.")
    else:
        print("Invalid payment option.")
        return

    confirmation = input("Confirm payment? (Y/N): ").strip().upper()
    if confirmation == 'Y':
        print("Checkout successful! Thank you for your purchase.")
        self.reserved_items.clear()
    else:
        print("Checkout canceled.")
