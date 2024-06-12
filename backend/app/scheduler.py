from apscheduler.schedulers.background import BackgroundScheduler
import time
from app.services.trends_service import TrendsService
from pymongo import MongoClient
import logging

logger = logging.getLogger(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['gourdstocks']
stock_collection = db['stocks']

# Initialize the scheduler
scheduler = BackgroundScheduler()
multiplier = 10  # Default multiplier

def get_stock_sectors():
    """
    Retrieve a list of unique stock sectors from the database.
    
    Returns:
        list: A list of unique stock sectors.
    """
    try:
        sectors = stock_collection.distinct('sector')
        logger.info("Retrieved stock sectors from the database")
        return sectors
    except Exception as e:
        logger.error(f"Error retrieving stock sectors: {e}")
        raise e

def schedule_trend_updates():
    """
    Schedule periodic updates for all stock sectors based on Google Trends data.
    """
    stock_sectors = get_stock_sectors()
    for i, sector in enumerate(stock_sectors):
        scheduler.add_job(
            func=TrendsService.update_stock_price,
            trigger='interval',
            minutes=60/len(stock_sectors),
            args=[sector, multiplier]
        )
        logger.info(f"Scheduled update job for sector {sector}")

if __name__ == '__main__':
    schedule_trend_updates()
    scheduler.start()
    logger.info("Scheduler started")

    # Keep the script running
    while True:
        time.sleep(60)
