import json
import os
import re

def save_data_to_file(file_path, data):
    """Saves data to a specified file, with error handling."""
    try:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Data successfully saved to {file_path}.")
    except IOError as e:
        print(f"Error saving data to file: {e}")

def load_data_from_file(file_path):
    """Loads data from a specified file, with error handling."""
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print(f"Error: The file {file_path} contains invalid JSON.")
        except Exception as e:
            print(f"Error loading data from file: {e}")
    return []

def clear_screen():
    """Clears the screen, works on both Windows and Unix-based systems."""
    os.system('cls' if os.name == 'nt' else 'clear')

def validate_email_format(email):
    """Validates email format using a regex."""
    # Basic regex for email validation
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(email_regex, email))

def validate_password_strength(password):
    """Validates password strength: at least 6 characters long."""
    if len(password) < 6:
        return False
    # Check for at least one digit, one uppercase letter, and one special character
    if not any(char.isdigit() for char in password):
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char in '!@#$%^&*()-_=+[]{}|;:,.<>?/~' for char in password):
        return False
    return True

