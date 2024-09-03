from flask import Blueprint, jsonify
from app.services.stock_service import StockService
import traceback
import logging
from flask_cors import CORS

# Initialize the logger
logger = logging.getLogger(__name__)

# Create a Blueprint for stock-related routes
bp = Blueprint('stocks', __name__, url_prefix='/stocks')

# Apply CORS
CORS(bp, supports_credentials=True)

@bp.route('/', methods=['GET'])
def get_stocks():
    """
    Fetch all stocks.
    
    Returns a list of all stocks in the database.
    In case of an error, returns a 500 Internal Server Error.
    """
    try:
        logger.info("Fetching all stocks from the database")
        stocks = StockService.get_all_stocks()
        logger.info("Successfully fetched all stocks")
        return jsonify(stocks), 200
    except Exception as e:
        logger.error(f"Error fetching stocks: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal Server Error"}), 500

@bp.route('/<symbol>', methods=['GET'])
def get_stock_price(symbol):
    """
    Get the current price of a stock.
    
    Expects the stock symbol as a URL parameter.
    Returns the current stock price if found, otherwise returns a 404 Not Found.
    """
    try:
        logger.info(f"Fetching stock price for symbol: {symbol.upper()}")
        price = StockService.get_stock_price(symbol.upper())
        if price is not None:
            logger.info(f"Successfully fetched stock price for symbol: {symbol.upper()}")
            return jsonify({"symbol": symbol.upper(), "price": price}), 200, {'Content-Type': 'application/json'}
        else:
            logger.warning(f"Stock not found for symbol: {symbol.upper()}")
            return jsonify({"error": "Stock not found"}), 404, {'Content-Type': 'application/json'}
    except Exception as e:
        logger.error(f"Error fetching stock price for symbol {symbol.upper()}: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal Server Error"}), 500, {'Content-Type': 'application/json'}
