from app import mongo
from bson import ObjectId
from .trends_service import TrendsService
from datetime import datetime
import time
class StockService:
    @staticmethod
    def get_all_stocks():
        """
        Fetch all stocks from the database.
        Converts ObjectId to string for JSON serialization.
        Returns a list of stocks.
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
        Returns the price if the stock is found, otherwise returns None.
        """
        print(stock_symbol)
        stock = mongo.db.stocks.find_one({"symbol": stock_symbol})
        if stock:
            return stock['price']
        return None


    @staticmethod
    def update_stock_prices():
        try:
            stocks = mongo.db.stocks.find()
            for stock in stocks:
                sector = stock.get('sector')
                if sector:
                    interest = TrendsService.get_trends_interest(sector)
                    # Adjust the price based on the interest (simple example)
                    new_price = stock['price'] * (1 + interest / 100.0)
                    new_high = max(stock.get('high', new_price), new_price)
                    new_low = min(stock.get('low', new_price), new_price)
                    
                    mongo.db.stocks.update_one(
                        {'_id': stock['_id']},
                        {'$set': {
                            'price': new_price,
                            'high': new_high,
                            'low': new_low,
                            'last_update': datetime.now()
                        }}
                    )
                    # Wait between requests to avoid hitting rate limits
                    time.sleep(60)
        except Exception as e:
            print("Error updating stock prices: ", str(e))
            raise e