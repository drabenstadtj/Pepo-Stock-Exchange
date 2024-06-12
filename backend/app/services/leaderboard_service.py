import logging
from app import mongo
from .stock_service import StockService

logger = logging.getLogger(__name__)

class LeaderboardService:
    @staticmethod
    def get_leaderboard():
        """
        Fetch the leaderboard data.

        Retrieves user data from the database, calculates the net worth for each user,
        and sorts the users by their net worth in descending order.

        Returns:
            list: A list of dictionaries containing the leaderboard data.
        """
        try:
            logger.info("Fetching leaderboard data")

            # Fetch all users from the database
            users_cursor = mongo.db.users.find()
            leaderboard = []
            
            for user in users_cursor:
                invested_assets = 0
                # Calculate invested assets by summing the value of each stock in the portfolio
                for stock in user['portfolio']:
                    live_price = StockService.get_stock_price(stock['stock_symbol'])
                    invested_assets += stock['quantity'] * live_price
                
                # Calculate net worth as the sum of liquid assets and invested assets
                net_worth = user['balance'] + invested_assets
                
                # Append user data to the leaderboard
                leaderboard.append({
                    'username': user['username'],
                    'title': 'Gourd Lord',  # Example title, customize as needed
                    'liquidAssets': user['balance'],
                    'investedAssets': invested_assets,
                    'netWorth': net_worth
                })

            # Sort the leaderboard by net worth in descending order
            leaderboard.sort(key=lambda x: x['netWorth'], reverse=True)
            
            logger.info("Leaderboard data fetched successfully")
            return leaderboard
        except Exception as e:
            # Log the error and raise it for further handling
            logger.error(f"Error fetching leaderboard data: {e}")
            raise e
