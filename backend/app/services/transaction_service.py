import logging
from app import mongo
from bson import ObjectId
from .stock_service import StockService
from datetime import datetime

logger = logging.getLogger(__name__)

class TransactionService:
    @staticmethod
    def buy_stock(data):
        """
        Buy a stock.
        
        Expects data to contain 'user_id', 'stock_symbol', and 'quantity'.
        Fetches the current stock price, updates user's portfolio and balance,
        and logs the transaction in the transactions collection.
        
        Args:
            data (dict): Dictionary containing 'user_id', 'stock_symbol', and 'quantity'.
        
        Returns:
            dict: A success message if the purchase is successful, or an error message otherwise.
        """
        user_id = data['user_id']
        stock_symbol = data['stock_symbol'].upper()
        quantity = data['quantity']

        # Convert user_id to ObjectId
        user_id = ObjectId(user_id)

        try:
            logger.info(f"Initiating buy transaction for user {user_id}, stock {stock_symbol}, quantity {quantity}")

            # Fetch the current price of the stock
            price = StockService.get_stock_price(stock_symbol)
            if price is None:
                logger.warning(f"Stock {stock_symbol} not found")
                return {"message": "Stock not found"}

            # Update user's portfolio and balance
            user = mongo.db.users.find_one({"_id": user_id})
            if user:
                # Deduct total price from user's balance
                total_price = price * quantity
                if user['balance'] >= total_price:
                    new_balance = user['balance'] - total_price

                    # Check if the stock is already in the portfolio
                    portfolio = user.get('portfolio', [])
                    stock_exists = False
                    for stock in portfolio:
                        if stock['stock_symbol'] == stock_symbol:
                            stock['quantity'] += quantity
                            stock_exists = True
                            break

                    if not stock_exists:
                        portfolio.append({"stock_symbol": stock_symbol, "quantity": quantity})

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
                        "type": "buy",
                        "date": datetime.now()
                    }
                    mongo.db.transactions.insert_one(transaction)

                    # Adjust stock price
                    StockService.update_stock_price(stock_symbol, quantity, is_buying=True)

                    logger.info(f"Buy transaction completed for user {user_id}, stock {stock_symbol}, quantity {quantity}")
                    return {"message": "Stock purchased successfully"}
                else:
                    logger.warning(f"User {user_id} has insufficient balance for buying {quantity} of {stock_symbol}")
                    return {"message": "Insufficient balance"}
            else:
                logger.warning(f"User {user_id} not found")
                return {"message": "User not found"}
        except Exception as e:
            logger.error(f"Error during buy transaction for user {user_id}, stock {stock_symbol}: {e}")
            return {"message": "Internal Server Error"}

    @staticmethod
    def sell_stock(data):
        """
        Sell a stock.
        
        Expects data to contain 'user_id', 'stock_symbol', and 'quantity'.
        Fetches the current stock price, updates user's portfolio and balance,
        and logs the transaction in the transactions collection.
        
        Args:
            data (dict): Dictionary containing 'user_id', 'stock_symbol', and 'quantity'.
        
        Returns:
            dict: A success message if the sale is successful, or an error message otherwise.
        """
        user_id = data['user_id']
        stock_symbol = data['stock_symbol'].upper()
        quantity = data['quantity']

        # Convert user_id to ObjectId
        user_id = ObjectId(user_id)

        try:
            logger.info(f"Initiating sell transaction for user {user_id}, stock {stock_symbol}, quantity {quantity}")

            # Fetch the current price of the stock
            price = StockService.get_stock_price(stock_symbol)
            if price is None:
                logger.warning(f"Stock {stock_symbol} not found")
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
                    logger.warning(f"User {user_id} has insufficient quantity of {stock_symbol} to sell")
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

                # Adjust stock price
                StockService.update_stock_price(stock_symbol, quantity, is_buying=False)

                logger.info(f"Sell transaction completed for user {user_id}, stock {stock_symbol}, quantity {quantity}")
                return {"message": "Stock sold successfully"}
            else:
                logger.warning(f"User {user_id} not found")
                return {"message": "User not found"}
        except Exception as e:
            logger.error(f"Error during sell transaction for user {user_id}, stock {stock_symbol}: {e}")
            return {"message": "Internal Server Error"}

    @staticmethod
    def get_transactions(user_id=None):
        """
        Fetch transactions.
        
        Optionally expects 'user_id' to filter transactions for a specific user.
        Converts ObjectId and datetime to string for JSON serialization.
        
        Args:
            user_id (str, optional): The ID of the user to filter transactions for.
        
        Returns:
            list: A list of transactions.
        """
        try:
            logger.info(f"Fetching transactions for user {user_id}" if user_id else "Fetching all transactions")
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
            logger.info(f"Fetched {len(transaction_list)} transactions")
            return transaction_list
        except Exception as e:
            logger.error(f"Error in get_transactions: {e}")
            return {"message": "Internal Server Error"}
