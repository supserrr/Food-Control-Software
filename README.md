# Food Waste Control Software

**`Overview`**

The **Food Waste Control Software** is a Python-based terminal application designed to minimize food waste by connecting restaurants and stores with surplus food to consumers looking for discounted food items. Inspired by the *Too Good To Go* platform, this project allows providers to list surplus food items and consumers to reserve these items at a discounted price.

**`Project Mission`**

The mission of this project is to reduce food waste and help consumers find affordable, good-quality food, contributing to both sustainability and community support. By facilitating the connection between food providers and consumers, this software encourages the responsible consumption of resources.

---

# Features

## Provider

- **Register and Login**: Providers sign up with a username, password, email, and location. Upon successful registration, they are automatically logged in.
- **List Food Items**: Add surplus food listings with details like item name, quantity, expiration date, price, and discount percentage.
- **View Profile**: Access a comprehensive profile displaying active listings, notifications of successful reservations, total earnings from sold items, and a stock summary.
- **Update Listings**: Easily update or modify existing food listings.
- **Earnings Report**: View a summary of earnings from sold food items.

## Consumer

- **Register and Login**: Consumers sign up with a username, email, and password, and are automatically logged in after registration.
- **View Listings**: Browse all available food listings or filter by specific criteria, like location.
- **Reserve Food**: Reserve food items by selecting the desired quantity.
- **View Cart**: Check reserved items in the cart and proceed to checkout when ready.
- **Checkout and Payment**: Complete purchases using Credit Card, PayPal, or Cash, with an order summary detailing the original and discounted prices.
- **View Profile**: Access a profile to view past orders, reserved items, and favorite providers.

---

# User Flow and Interaction

### Provider User Journey
1. **Registration/Login**: Providers enter their information to register or log in.
2. **Listing Items**: List surplus food items by specifying details such as name, quantity, price, and expiration date.
3. **Profile Management**: Check profile for earnings, notifications, and food stock summary.
4. **Updating Listings**: Update existing listings or view stock status.

### Consumer User Journey
1. **Registration/Login**: Sign up or log in to start reserving items.
2. **Browsing Listings**: Explore available food items and select preferred choices.
3. **Reservation**: Choose the quantity of items to reserve.
4. **Cart and Checkout**: Review reserved items in the cart and proceed to payment.
5. **Payment**: Complete the purchase using a preferred payment method.
6. **Profile Access**: Check profile for order history and reserved items.

---

# Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/supserrr/food-control-software.git
   ```

2. Navigate to the project directory:
   ```bash
   cd food-control-software
   ```

3. Set up a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/macOS
   venv\Scripts\activate     # For Windows
   ```

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the application:
   ```bash
   python3 run.py
   ```
