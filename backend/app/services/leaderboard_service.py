from app import mongo
from .stock_service import StockService

class LeaderboardService:
    @staticmethod
    def get_leaderboard():
        try:
            users_cursor = mongo.db.users.find()
            leaderboard = []
            for user in users_cursor:
                invested_assets = 0
                for stock in user['portfolio']:
                    live_price = StockService.get_stock_price(stock['stock_symbol'])
                    invested_assets += stock['quantity'] * live_price
                net_worth = user['balance'] + invested_assets
                leaderboard.append({
                    'username': user['username'],
                    'title': 'Gourd Lord',  # Example title, customize as needed
                    'liquidAssets': user['balance'],
                    'investedAssets': invested_assets,
                    'netWorth': net_worth
                })

            # Sort leaderboard by net worth in descending order
            leaderboard.sort(key=lambda x: x['netWorth'], reverse=True)
            return leaderboard
        except Exception as e:
            print("Error fetching leaderboard data: ", str(e))
            raise e
