from app import mongo
from bson import ObjectId
from .stock_service import StockService
from datetime import datetime

class TransactionService:
    @staticmethod
    def buy_stock(data):
        """
        Buy a stock.
        Expects data to contain 'user_id', 'stock_symbol', and 'quantity'.
        Fetches the current stock price, updates user's portfolio and balance, 
        and logs the transaction in the transactions collection.
        Returns a success message if the purchase is successful, or an error message otherwise.
        """
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
    def sell_stock(data):
        """
        Sell a stock.
        Expects data to contain 'user_id', 'stock_symbol', and 'quantity'.
        Fetches the current stock price, updates user's portfolio and balance,
        and logs the transaction in the transactions collection.
        Returns a success message if the sale is successful, or an error message otherwise.
        """
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
            portfolio = user.get('portfolio', [])
            for stock in portfolio:
                if stock['stock_symbol'] == stock_symbol:
                    if stock['quantity'] >= quantity:
                        stock['quantity'] -= quantity
                        if stock['quantity'] == 0:
                            portfolio.remove(stock)
                        break
            else:
                return {"message": "Insufficient stock quantity"}

            # Add total price to user's balance
            total_price = price * quantity
            new_balance = user['balance'] + total_price
            mongo.db.users.update_one(
                {"_id": user_id},
                {"$set": {"balance": new_balance, "portfolio": portfolio}}
            )

            # Log the transaction
            transaction = {
                "user_id": user_id,
                "stock_symbol": stock_symbol,
                "quantity": quantity,
                "price": price,
                "total_price": total_price,
                "type": "sell",
                "date": datetime.now()
            }
            mongo.db.transactions.insert_one(transaction)

            return {"message": "Stock sold successfully"}
        return {"message": "User not found"}

    @staticmethod
    def get_transactions(user_id=None):
        """
        Fetch transactions.
        Optionally expects 'user_id' to filter transactions for a specific user.
        Converts ObjectId and datetime to string for JSON serialization.
        Returns a list of transactions.
        """
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