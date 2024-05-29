import json
import pymongo

def load_stocks_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def initialize_stocks():
    # Load stock data from JSON file
    stocks_data = load_stocks_data('data/initial_data.json')

    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["gourdstocks"]
    stocks_collection = db["stocks"]

    # Insert stock data into the database
    for stock_data in stocks_data:
        stocks_collection.insert_one(stock_data)

    print("Stocks initialized successfully.")

if __name__ == "__main__":
    initialize_stocks()
