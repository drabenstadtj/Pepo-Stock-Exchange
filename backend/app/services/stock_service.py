from app import mongo
from bson import ObjectId
from .trends_service import TrendsService
from datetime import datetime
import time
import random

class StockService:
    @staticmethod
    def get_all_stocks():
        """
        Fetch all stocks from the database.
        
        Converts ObjectId to string for JSON serialization.
        
        Returns:
            list: A list of all stocks in the database.
        """
        try:
            stocks_cursor = mongo.db.stocks.find()
            stocks = []
            for stock in stocks_cursor:
                stock['_id'] = str(stock['_id'])  # Convert ObjectId to string
                stocks.append(stock)
            return stocks
        except Exception as e:
            print("Error fetching stocks: ", str(e))
            raise e

    @staticmethod
    def get_stock_price(stock_symbol):
        """
        Fetch the current price of a stock by its symbol.
        
        Args:
            stock_symbol (str): The symbol of the stock.
        
        Returns:
            float: The current price of the stock if found, otherwise None.
        """
        try:
            stock = mongo.db.stocks.find_one({"symbol": stock_symbol})
            if stock:
                return stock['price']
            return None
        except Exception as e:
            print(f"Error fetching stock price for {stock_symbol}: {e}")
            raise e

    @staticmethod
    def update_stock_prices():
        """
        Update the prices of all stocks in the database.
        
        Simulates price changes based on random percentage changes.
        Updates the high, low, and change values of each stock.
        """
        try:
            stocks = mongo.db.stocks.find()
            for stock in stocks:
                sector = stock.get('sector')
                if sector:
                    old_price = stock['price']

                    # Generate a random percentage change between -10% and 10%
                    percentage_change = random.uniform(-10, 10)

                    # Calculate the new price based on the percentage change
                    new_price = old_price * (1 + percentage_change / 100.0)
                    new_high = max(stock.get('high', new_price), new_price)
                    new_low = min(stock.get('low', new_price), new_price)
                    # Calculate the price change
                    price_change = new_price - old_price

                    # Update the stock with the new price, high, low, and change
                    mongo.db.stocks.update_one(
                        {'_id': stock['_id']},
                        {'$set': {
                            'price': new_price,
                            'high': new_high,
                            'low': new_low,
                            'change': price_change,
                            'last_update': datetime.now()
                        }}
                    )
                    # Wait between updates to avoid hitting rate limits
                    time.sleep(5)
        except Exception as e:
            print("Error updating stock prices: ", str(e))
            raise e
        
    @staticmethod
    def calculate_new_price(stock_symbol, quantity, is_buying):
        stock = mongo.db.stocks.find_one({"symbol": stock_symbol})
        if not stock:
            raise ValueError("Stock not found")

        # Simple model: price change proportional to quantity bought/sold
        price_change_factor = 0.001  # Adjust this factor as needed
        price_change = price_change_factor * quantity

        if is_buying:
            new_price = stock['price'] + price_change
        else:
            new_price = stock['price'] - price_change

        return new_price
