from flask import Blueprint, request, jsonify
from app.services.transaction_service import TransactionService
import jwt
from functools import wraps
import os
from flask_cors import CORS

# Create a Blueprint for transaction-related routes
bp = Blueprint('transactions', __name__, url_prefix='/transactions')

#Apply CORS
CORS(bp, supports_credentials=True)

# Load environment variables
SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')

def token_required(f):
    """
    Decorator to ensure a valid JWT token is present in the request header.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            # Extract token from 'Bearer <token>' format
            token = token.split()[1]
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 403
        except Exception as e:
            print(f"Token verification error: {e}")
            return jsonify({'message': 'Token verification failed!'}), 403

        return f(user_id, *args, **kwargs)

    return decorated

@bp.route('/buy', methods=['POST'])
@token_required
def buy_stock(user_id):
    """
    Buy a stock.
    
    Expects a JSON payload with stock details.
    Returns the result of the stock purchase transaction.
    """
    try:
        data = request.get_json()
        data['user_id'] = user_id
        result = TransactionService.buy_stock(data)
        return jsonify(result), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        print(f"Error during buy transaction: {e}")
        return jsonify({"error": "Internal Server Error"}), 500, {'Content-Type': 'application/json'}

@bp.route('/sell', methods=['POST'])
@token_required
def sell_stock(user_id):
    """
    Sell a stock.
    
    Expects a JSON payload with stock details.
    Returns the result of the stock sale transaction.
    """
    try:
        data = request.get_json()
        data['user_id'] = user_id
        result = TransactionService.sell_stock(data)
        return jsonify(result), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        print(f"Error during sell transaction: {e}")
        return jsonify({"error": "Internal Server Error"}), 500, {'Content-Type': 'application/json'}

@bp.route('/', methods=['GET'])
@token_required
def get_transactions(user_id):
    """
    Fetch all transactions for the user.
    
    Returns a list of all transactions for the authenticated user.
    """
    try:
        transactions = TransactionService.get_transactions(user_id)
        return jsonify(transactions), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        print(f"Error fetching transactions: {e}")
        return jsonify({"error": "Internal Server Error"}), 500, {'Content-Type': 'application/json'}
