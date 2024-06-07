from pytrends.request import TrendReq
import pymongo
from datetime import datetime
import time

# Setup MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['gourdstocks']
trends_collection = db['trends']
stocks_collection = db['stocks']

# Setup Pytrends
pytrends = TrendReq(hl='en-US', tz=360)

def fetch_live_interest_data(sector):
    try:
        pytrends.build_payload([sector], cat=0, timeframe='now 1-H')
        interest_over_time_df = pytrends.interest_over_time()
        if not interest_over_time_df.empty:
            live_interest = interest_over_time_df[sector].iloc[-1]
            return live_interest
    except Exception as e:
        print(f"Error fetching data for {sector}: {e}")
    return None

def store_live_interest_data():
    # Get all unique sectors from the stocks collection
    sectors = stocks_collection.distinct('sector')
    
    for sector in sectors:
        live_interest = fetch_live_interest_data(sector)
        if live_interest is not None:
            trends_collection.update_one(
                {'sector': sector},
                {'$set': {'live_interest': live_interest, 'timestamp': datetime.utcnow()}},
                upsert=True
            )
            print(f'Retrieved live data for {sector}')
        else:
            print(f'No live data for {sector}')
        time.sleep(60)  # Wait for 1 minute between requests to avoid rate limits

# Fetch and store live interest data
store_live_interest_data()
