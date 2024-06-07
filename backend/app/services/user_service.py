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
        
        Args:
            data (dict): Dictionary containing 'username' and 'password'.
        
        Returns:
            dict: A success message upon successful registration.
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
        
        Args:
            username (str): The username to search for.
        
        Returns:
            ObjectId: The user ID if found, otherwise None.
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
        
        Args:
            data (dict): Dictionary containing 'username' and 'password'.
        
        Returns:
            ObjectId: The user ID if credentials are correct, otherwise None.
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
        
        Args:
            user_id (str): The user ID to search for.
        
        Returns:
            dict: The user document if found, otherwise None.
        """
        return mongo.db.users.find_one({"_id": ObjectId(user_id)})

    @staticmethod
    def get_portfolio(user_id):
        """
        Fetch the user's portfolio by user ID.
        
        Args:
            user_id (str): The user ID to search for.
        
        Returns:
            list: The user's portfolio if the user is found, otherwise an empty list.
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
        
        Args:
            user_id (str): The user ID to search for.
        
        Returns:
            float: The user's balance if the user is found, otherwise 0.
        """
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)}, {"balance": 1})
        if user and 'balance' in user:
            return user['balance']
        return 0
