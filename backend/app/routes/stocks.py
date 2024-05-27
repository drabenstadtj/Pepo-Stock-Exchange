from flask import Blueprint, jsonify
from app.services.stock_service import StockService
import traceback

# Create a Blueprint for stock-related routes
bp = Blueprint('stocks', __name__, url_prefix='/stocks')

@bp.route('/', methods=['GET'])
def get_stocks():
    """
    Fetch all stocks.
    Returns a list of all stocks in the database.
    In case of an error, returns a 500 Internal Server Error.
    """
    try:
        stocks = StockService.get_all_stocks()
        return jsonify(stocks), 200
    except Exception as e:
        print("Error: ", str(e))
        traceback.print_exc()
        return jsonify({"error": "Internal Server Error"}), 500
