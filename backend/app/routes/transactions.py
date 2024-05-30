from flask import Blueprint, request, jsonify
from flask_cors import CORS
from app.services.transaction_service import TransactionService

# Create a Blueprint for transaction-related routes
bp = Blueprint('transactions', __name__, url_prefix='/transactions')
CORS(bp, supports_credentials=True)  # Apply CORS to the blueprint

@bp.route('/buy', methods=['POST'])
def buy_stock():
    data = request.get_json()
    data['user_id'] = None #USER ID
    result = TransactionService.buy_stock(data)
    return jsonify(result)

@bp.route('/sell', methods=['POST'])
def sell_stock():
    data = request.get_json()
    data['user_id'] = None #USER ID
    result = TransactionService.sell_stock(data)
    return jsonify(result)

@bp.route('/', methods=['GET'])
def get_transactions():
    user_id = request.args.get('user_id')
    transactions = TransactionService.get_transactions(user_id)
    return jsonify(transactions)
