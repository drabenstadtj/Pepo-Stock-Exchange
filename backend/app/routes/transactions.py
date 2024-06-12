from flask import Blueprint, request, jsonify
from app.services.transaction_service import TransactionService
import jwt
from functools import wraps
import os
import logging
from flask_cors import CORS

# Initialize the logger
logger = logging.getLogger(__name__)

# Create a Blueprint for transaction-related routes
bp = Blueprint('transactions', __name__, url_prefix='/transactions')

# Apply CORS
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
            logger.warning("Token is missing")
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            # Extract token from 'Bearer <token>' format
            token = token.split()[1]
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return jsonify({'message': 'Token has expired!'}), 403
        except jwt.InvalidTokenError:
            logger.warning("Token is invalid")
            return jsonify({'message': 'Token is invalid!'}), 403
        except Exception as e:
            logger.error(f"Token verification error: {e}")
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
        logger.info(f"Processing buy transaction for user {user_id} with data {data}")
        result = TransactionService.buy_stock(data)
        logger.info(f"Buy transaction successful for user {user_id}")
        return jsonify(result), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        logger.error(f"Error during buy transaction for user {user_id}: {e}")
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
        logger.info(f"Processing sell transaction for user {user_id} with data {data}")
        result = TransactionService.sell_stock(data)
        logger.info(f"Sell transaction successful for user {user_id}")
        return jsonify(result), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        logger.error(f"Error during sell transaction for user {user_id}: {e}")
        return jsonify({"error": "Internal Server Error"}), 500, {'Content-Type': 'application/json'}

@bp.route('/', methods=['GET'])
@token_required
def get_transactions(user_id):
    """
    Fetch all transactions for the user.
    
    Returns a list of all transactions for the authenticated user.
    """
    try:
        logger.info(f"Fetching transactions for user {user_id}")
        transactions = TransactionService.get_transactions(user_id)
        logger.info(f"Successfully fetched transactions for user {user_id}")
        return jsonify(transactions), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        logger.error(f"Error fetching transactions for user {user_id}: {e}")
        return jsonify({"error": "Internal Server Error"}), 500, {'Content-Type': 'application/json'}
