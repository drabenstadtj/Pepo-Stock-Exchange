from flask import Blueprint, request, jsonify, session
from app.services.transaction_service import TransactionService

# Create a Blueprint for transaction-related routes
bp = Blueprint('transactions', __name__, url_prefix='/transactions')

@bp.route('/buy', methods=['POST'])
def buy_stock():
    if 'user_id' not in session:
        return jsonify({"error": "User not logged in"}), 401

    data = request.get_json()
    data['user_id'] = session['user_id']
    result = TransactionService.buy_stock(data)
    return jsonify(result)

@bp.route('/sell', methods=['POST'])
def sell_stock():
    if 'user_id' not in session:
        return jsonify({"error": "User not logged in"}), 401

    data = request.get_json()
    print(data)
    data['user_id'] = session['user_id']
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
