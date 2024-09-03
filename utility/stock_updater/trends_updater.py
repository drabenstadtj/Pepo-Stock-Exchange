import time
import random
from pytrends.request import TrendReq
from pytrends.exceptions import TooManyRequestsError
from pymongo import MongoClient
import os
from datetime import datetime

# Function to fetch trends data in batches with error handling
def fetch_trends_data(stock_sectors, batch_size=5, delay=10):
    trends_data = {}
    for i in range(0, len(stock_sectors), batch_size):
        batch = stock_sectors[i:i+batch_size]
        pytrends = TrendReq(hl='en-US', tz=360)
        
        while True:
            try:
                pytrends.build_payload(batch, cat=0, timeframe='now 1-H', geo='', gprop='')
                data = pytrends.interest_over_time()
                if not data.empty:
                    for sector in batch:
                        trends_data[sector] = data[sector].iloc[-1]  # Get the latest interest data point
                time.sleep(delay)  # Delay between batches to avoid rate limiting
                break
            except TooManyRequestsError:
                print("Received 429 Too Many Requests error. Waiting for 5 minutes before retrying...")
                time.sleep(5 * 60)  # Wait for 5 minutes
    return trends_data

# MongoDB connection
client = MongoClient(os.getenv("DATABASE_URI", "mongodb://localhost:27017/"))
db = client.get_database("gourdstocks")
stocks_collection = db.stocks

# Function to calculate new stock price based on trends data
def calculate_new_price(current_price, interest_data):
    # Implement your price calculation logic here
    # For simplicity, let's assume price increases by 1% for each interest point
    if interest_data != 0:
        interest_factor = interest_data / 100
        new_price = current_price * (1 + interest_factor)
    else:
        new_price = current_price * (1 - .02)
    return new_price

# Function to update stock prices in the database
def update_stock_prices():
    stock_sectors = stocks_collection.distinct("sector")
    trends_data = fetch_trends_data(stock_sectors)

    for stock in stocks_collection.find():
        sector = stock['sector']
        if sector in trends_data:
            old_price = stock['price']
            new_price = calculate_new_price(old_price, trends_data[sector])
            if not new_price == old_price:
                change = new_price - old_price
            else:
                change = stock['change']
            stocks_collection.update_one(
                {"_id": stock['_id']},
                {"$set": 
                    {
                        "price": new_price, 
                        "change": change, 
                        "last_update": datetime.utcnow(),
                        'low': min(stock['low'], new_price),
                        'high': max(stock['high'], new_price)
                    }
                }
            )
            print(f"Updated {stock['name']} price to {new_price} (Change: {change})")

# Schedule the job to run every 5 minutes using schedule
import schedule

update_stock_prices()

schedule.every(5).minutes.do(update_stock_prices)

print("Scheduler started. Updating stock prices every 5 minutes...")

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
