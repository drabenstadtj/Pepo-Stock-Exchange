from app import mongo
from bson import ObjectId

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
