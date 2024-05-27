from flask import Blueprint, request, jsonify
from app.services.transaction_service import TransactionService

bp = Blueprint('transactions', __name__, url_prefix='/transactions')

@bp.route('/buy', methods=['POST'])
def buy_stock():
    data = request.get_json()
    result = TransactionService.buy_stock(data)
    return jsonify(result)

@bp.route('/', methods=['GET'])
def get_transactions():
    user_id = request.args.get('user_id')
    transactions = TransactionService.get_transactions(user_id)
    return jsonify(transactions)
