from app import mongo
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from .stock_service import StockService

class UserService:
    @staticmethod
    def register_user(data):
        """
        Register a new user.
        Expects data to contain 'username' and 'password'.
        Initializes user balance to 10000 and an empty portfolio.
        Stores user information in the users collection.
        Returns a success message upon successful registration.
        """
        user = {
            "username": data['username'],
            "password": generate_password_hash(data['password']),  # Hash the password
            "balance": 10000,
            "portfolio": []
        }
        mongo.db.users.insert_one(user)
        return {"message": "User registered successfully"}

    @staticmethod
    def get_user_id(username):
        """
        Fetch the user ID by username.
        Expects the 'username' as input.
        Returns the user ID if found, otherwise returns None.
        """
        user = mongo.db.users.find_one({"username": username}, {"_id": 1})
        if user:
            return user['_id']
        return None

    @staticmethod
    def verify_credentials(data):
        """
        Verify user credentials.
        Expects data to contain 'username' and 'password'.
        Returns the user ID if credentials are correct, otherwise returns None.
        """
        print(f"Received data: {data}")  # Debug: Log received data
        user = mongo.db.users.find_one({"username": data['username']})
        if user:
            print(f"User found: {user}")  # Debug: Log user data from DB
            if check_password_hash(user['password'], data['password']):
                print(f"Password match for user: {user['_id']}")  # Debug: Log successful password match
                return user['_id']
            else:
                print(f"Password mismatch for user: {user['_id']}")  # Debug: Log password mismatch
        else:
            print("User not found")  # Debug: Log user not found
        return None

    @staticmethod
    def get_user_by_id(user_id):
        """
        Fetch a user by user ID.
        Expects the 'user_id' as input.
        Returns the user document if found, otherwise returns None.
        """
        return mongo.db.users.find_one({"_id": ObjectId(user_id)})

    @staticmethod
    def get_portfolio(user_id):
        """
        Fetch the user's portfolio by user ID.
        Expects the 'user_id' as input.
        Converts user_id to ObjectId.
        Returns the user's portfolio if the user is found, otherwise returns an empty list.
        """
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)}, {"portfolio": 1})
        if user and 'portfolio' in user:
            portfolio = user['portfolio']
            for stock in portfolio:
                stock['price'] = StockService.get_stock_price(stock['stock_symbol'])
            return portfolio
        return []
    
    @staticmethod
    def get_balance(user_id):
        """
        Fetch the user's balance by user ID.
        Expects the 'user_id' as input.
        Converts user_id to ObjectId.
        Returns the user's balance if the user is found, otherwise returns an empty list.
        """
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)}, {"balance": 1})
        if user and 'balance' in user:
            return user['balance']
        return []
    
    @staticmethod
    def get_assets_value(user_id):
        """
        Fetch the user's total assets value by user ID.
        Expects the 'user_id' as input.
        Converts user_id to ObjectId.
        Returns the total value of the user's assets if the user is found, otherwise returns 0.
        """
        assets_value = 0
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)}, {"portfolio": 1})
        if user and 'portfolio' in user:
            portfolio = user['portfolio']
            for stock in portfolio:
                price = StockService.get_stock_price(stock['stock_symbol'])
                if price is not None:
                    assets_value += stock['quantity'] * price
        return assets_value