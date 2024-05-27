from flask import Blueprint, request, jsonify
from app.services.transaction_service import TransactionService

# Create a Blueprint for transaction-related routes
bp = Blueprint('transactions', __name__, url_prefix='/transactions')

@bp.route('/buy', methods=['POST'])
def buy_stock():
    """
    Buy a stock.
    Expects JSON payload with 'user_id', 'stock_symbol', and 'quantity'.
    Fetches the current stock price and processes the purchase.
    Returns a success message if the purchase is successful, or an error message otherwise.
    """
    data = request.get_json()
    result = TransactionService.buy_stock(data)
    return jsonify(result)

@bp.route('/sell', methods=['POST'])
def sell_stock():
    """
    Sell a stock.
    Expects JSON payload with 'user_id', 'stock_symbol', and 'quantity'.
    Fetches the current stock price and processes the sale.
    Returns a success message if the sale is successful, or an error message otherwise.
    """
    data = request.get_json()
    result = TransactionService.sell_stock(data)
    return jsonify(result)

@bp.route('/', methods=['GET'])
def get_transactions():
    """
    Fetch transactions.
    Optionally expects a query parameter 'user_id' to fetch transactions for a specific user.
    Returns a list of transactions.
    """
    user_id = request.args.get('user_id')
    transactions = TransactionService.get_transactions(user_id)
    return jsonify(transactions)
