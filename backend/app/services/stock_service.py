import logging
from app import mongo
from bson import ObjectId
from .trends_service import TrendsService
from datetime import datetime
import time
import random

logger = logging.getLogger(__name__)

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
            logger.info("Fetching all stocks from the database")
            stocks_cursor = mongo.db.stocks.find()
            stocks = []
            for stock in stocks_cursor:
                stock['_id'] = str(stock['_id'])  # Convert ObjectId to string
                stocks.append(stock)
            logger.info(f"Fetched {len(stocks)} stocks from the database")
            return stocks
        except Exception as e:
            logger.error(f"Error fetching stocks: {e}")
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
            logger.info(f"Fetching stock price for {stock_symbol}")
            stock = mongo.db.stocks.find_one({"symbol": stock_symbol})
            if stock:
                logger.info(f"Current price for {stock_symbol} is {stock['price']}")
                return stock['price']
            logger.warning(f"Stock {stock_symbol} not found")
            return None
        except Exception as e:
            logger.error(f"Error fetching stock price for {stock_symbol}: {e}")
            raise e

    @staticmethod
    def update_stock_prices():
        """
        Update the prices of all stocks in the database.
        
        Simulates price changes based on random percentage changes.
        Updates the high, low, and change values of each stock.
        """
        try:
            logger.info("Updating stock prices for all stocks")
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
                    logger.info(f"Updated stock {stock['symbol']} with new price {new_price}")
                    # Wait between updates to avoid hitting rate limits
                    time.sleep(5)
        except Exception as e:
            logger.error(f"Error updating stock prices: {e}")
            raise e
        
    @staticmethod
    def update_stock_price(stock_symbol, quantity, is_buying):
        """
        Update the price of a stock based on buying or selling quantity.
        
        Args:
            stock_symbol (str): The symbol of the stock.
            quantity (int): The quantity of stock being bought or sold.
            is_buying (bool): True if buying, False if selling.
        
        Returns:
            float: The new price of the stock if successful, otherwise an error message.
        """
        try:
            logger.info(f"Updating stock price for {stock_symbol}")
            stock = mongo.db.stocks.find_one({"symbol": stock_symbol})
            if not stock:
                raise ValueError(f"Stock '{stock_symbol}' not found")

            # Simple model: price change proportional to quantity bought/sold
            price_change_factor = 0.1  # Adjust this factor as needed
            price_change = price_change_factor * quantity

            if is_buying:
                new_price = stock['price'] + price_change
            else:
                new_price = stock['price'] - price_change

            old_price = stock['price']

            # Calculate the new price based on the percentage change
            new_high = max(stock.get('high', new_price), new_price)
            new_low = min(stock.get('low', new_price), new_price)
            # Calculate the price change
            price_change = new_price - old_price

            # Update the stock with the new price, high, low, and change
            result = mongo.db.stocks.update_one(
                {'_id': stock['_id']},
                {'$set': {
                    'price': new_price,
                    'high': new_high,
                    'low': new_low,
                    'change': price_change,
                    'last_update': datetime.now()
                }}
            )

            if result.matched_count == 0:
                raise RuntimeError(f"Failed to update stock '{stock_symbol}' in the database")

            logger.info(f"Updated stock {stock_symbol} with new price {new_price}")
            return new_price

        except ValueError as ve:
            logger.error(f"ValueError: {ve}")
            return {"error": str(ve)}
        except RuntimeError as re:
            logger.error(f"RuntimeError: {re}")
            return {"error": str(re)}
        except Exception as e:
            logger.error(f"Exception: {e}")
            return {"error": "An unexpected error occurred"}
