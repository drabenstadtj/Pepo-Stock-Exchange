from app import mongo
from bson import ObjectId

class UserService:
    @staticmethod
    def register_user(data):
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
        user = mongo.db.users.find_one({"username": username}, {"_id": 1})
        if user:
            return user['_id']
        return None

    @staticmethod
    def get_portfolio(user_id):
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)}, {"portfolio": 1})
        if user and 'portfolio' in user:
            return user['portfolio']
        return []
