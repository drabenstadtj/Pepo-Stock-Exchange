import schedule
import time
from app import create_app, mongo
from app.services.stock_service import StockService

app = create_app()

def job():
    with app.app_context():
        StockService.update_stock_prices()
    print("Stock prices updated.")

# Schedule the job every 30 seconds
schedule.every(30).seconds.do(job)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
