from app import mongo
from bson import ObjectId
from .stock_service import StockService
from datetime import datetime

class TransactionService:
    @staticmethod
    def buy_stock(data):
        user_id = data['user_id']
        stock_symbol = data['stock_symbol']
        quantity = data['quantity']

        # Convert user_id to ObjectId
        user_id = ObjectId(user_id)

        # Fetch the current price of the stock
        price = StockService.get_stock_price(stock_symbol)
        if price is None:
            return {"message": "Stock not found"}

        # Update user's portfolio and balance
        user = mongo.db.users.find_one({"_id": user_id})
        if user:
            # Deduct total price from user's balance
            total_price = price * quantity
            if user['balance'] >= total_price:
                new_balance = user['balance'] - total_price
                mongo.db.users.update_one(
                    {"_id": user_id},
                    {"$set": {"balance": new_balance},
                     "$push": {"portfolio": {"stock_symbol": stock_symbol, "quantity": quantity, "price": price}}}
                )

                # Log the transaction
                transaction = {
                    "user_id": user_id,
                    "stock_symbol": stock_symbol,
                    "quantity": quantity,
                    "price": price,
                    "total_price": total_price,
                    "type": "buy",
                    "date": datetime.now()
                }
                mongo.db.transactions.insert_one(transaction)

                return {"message": "Stock purchased successfully"}
            else:
                return {"message": "Insufficient balance"}
        return {"message": "User not found"}

    @staticmethod
    def get_transactions(user_id=None):
        try:
            query = {}
            if user_id:
                query['user_id'] = ObjectId(user_id)
            transactions = mongo.db.transactions.find(query)
            transaction_list = []
            for transaction in transactions:
                transaction['_id'] = str(transaction['_id'])
                transaction['user_id'] = str(transaction['user_id'])
                transaction['date'] = transaction['date'].isoformat()
                transaction_list.append(transaction)
            return transaction_list
        except Exception as e:
            print("Error in get_transactions:", str(e))
            traceback.print_exc()
            return {"message": "Internal Server Error"}
