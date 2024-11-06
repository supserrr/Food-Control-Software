class User:
    users = []
    listings = []

    def __init__(self, username, email, password, role, location=None):
        self.username = username
        self.email = email
        self.password = password
        self.role = role
        self.location = location
        self.favorites = []
        self.reserved_items = []
        User.users.append(self)

    @classmethod
    def register(cls, username, email, password, role, location=None):
        user = cls(username, email, password, role, location)
        print(f"Registration successful! Logged in as {username}.")
        return user

    @classmethod
    def login(cls, email, password):
        for user in cls.users:
            if user.email == email and user.password == password:
                print(f"Welcome back, {user.username}!")
                return user
        print("Invalid email or password.")
        return None
