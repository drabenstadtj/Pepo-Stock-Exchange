from app import mongo
from bson import ObjectId

class StockService:
    @staticmethod
    def get_all_stocks():
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
        print(stock_symbol)
        stock = mongo.db.stocks.find_one({"symbol": stock_symbol})
        if stock:
            return stock['price']
        return None