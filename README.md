# Food Waste Control Software

**`Overview`**

The **Food Waste Control Software** is a Python-based terminal application designed to minimize food waste by connecting restaurants and stores with surplus food to consumers looking for discounted food items. Inspired by the *Too Good To Go* platform, this project allows providers to list surplus food items and consumers to reserve these items at a discounted price.

**`Project Mission`**

This project aims to reduce food waste and help consumers find affordable, good-quality food, contributing to both sustainability and community support. By facilitating the connection between food providers and consumers, this software encourages the responsible consumption of resources.

---

# Features

**`Provider`**

- **Register and Login**: Providers can register with a username, password, and location. Upon registration, providers are automatically logged in.
- **List Food Items**: Providers can add surplus food listings, including details like item name, quantity, expiration date, price, and discount percentage.
- **View Profile**: Providers can see all their food listings in their profile, with original and discounted prices displayed.

**`Consumers`**

- **Register and Login**: Consumers register with a username, password, and email. They are automatically logged in after registration.
- **View Listings**: Consumers can view all available food listings or filter them by location.
- **Reserve Food**: Consumers can reserve food items, specifying the quantity they want to reserve.
- **Favorites**: Consumers can add providers to their list of favorites and view them in their profile.
- **Checkout**: Consumers can review their reserved items, including an order summary with original and discounted prices. They can proceed to payment via various methods (Credit Card, PayPal, or Cash).
- **Payment Options**: Provides Credit Card, PayPal, and Cash options to complete checkout transactions.

---

# Installation and Setup

**Prerequisites**
- Python 3.x

# Installation
 **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/food-waste-control-software.git

   cd food-waste-control-software

   python3 app.py
