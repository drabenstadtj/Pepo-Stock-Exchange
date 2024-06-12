from app import mongo
from pytrends.request import TrendReq
from datetime import datetime
import time
import logging

logger = logging.getLogger(__name__)

class TrendsService:
    pytrends = TrendReq(hl='en-US', tz=360)

    @staticmethod
    def get_trends_data(keyword):
        """
        Fetch interest data for a specific keyword using Google Trends.
        
        Args:
            keyword (str): The keyword to fetch trends data for.
        
        Returns:
            float: The latest interest value for the keyword, or 0 if no data is found.
        """
        try:
            TrendsService.pytrends.build_payload([keyword], cat=0, timeframe='now 1-H', geo='', gprop='')
            data = TrendsService.pytrends.interest_over_time()
            if not data.empty:
                logger.info(f"Fetched trends data for {keyword}")
                return data[keyword].iloc[-1]  # Get the latest interest value
            return 0
        except Exception as e:
            logger.error(f"Error fetching trends data for {keyword}: {e}")
            raise e

    @staticmethod
    def update_stock_price(sector, multiplier):
        """
        Update the price of a stock sector based on Google Trends data.
        
        Args:
            sector (str): The stock sector to update.
            multiplier (float): The factor by which to adjust the stock price based on interest.
        """
        try:
            interest = TrendsService.get_trends_data(sector)
            stock = mongo.db.stocks.find_one({"sector": sector})
            if not stock:
                raise ValueError(f"Stock sector '{sector}' not found")

            old_price = stock['price']
            new_price = interest * multiplier

            new_high = max(stock.get('high', new_price), new_price)
            new_low = min(stock.get('low', new_price), new_price)
            price_change = new_price - old_price

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
            logger.info(f"Updated stock price for sector {sector}: {new_price}")
        except ValueError as ve:
            logger.error(f"ValueError: {ve}")
            raise ve
        except Exception as e:
            logger.error(f"Error updating stock price for sector {sector}: {e}")
            raise e

    @staticmethod
    def schedule_trend_updates(stock_sectors, multiplier):
        """
        Schedule periodic updates for all stock sectors based on Google Trends data.
        
        Args:
            stock_sectors (list): A list of stock sectors to update.
            multiplier (float): The factor by which to adjust the stock prices based on interest.
        """
        try:
            for sector in stock_sectors:
                TrendsService.update_stock_price(sector, multiplier)
                logger.info(f"Scheduled update for sector {sector}")
                # Wait between updates to avoid hitting rate limits
                time.sleep(60 / len(stock_sectors))
        except Exception as e:
            logger.error(f"Error scheduling trend updates: {e}")
            raise e
