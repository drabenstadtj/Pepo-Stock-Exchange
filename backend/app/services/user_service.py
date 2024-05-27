from app import mongo
from bson import ObjectId

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
            "password": data['password'],  # In a real application, hash the password
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
    def get_portfolio(user_id):
        """
        Fetch the user's portfolio by user ID.
        Expects the 'user_id' as input.
        Converts user_id to ObjectId.
        Returns the user's portfolio if the user is found, otherwise returns an empty list.
        """
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)}, {"portfolio": 1})
        if user and 'portfolio' in user:
            return user['portfolio']
        return []
