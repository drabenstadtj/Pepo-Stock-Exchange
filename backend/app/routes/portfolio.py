from flask import Blueprint, jsonify, request
from app.services.user_service import UserService
import jwt
from functools import wraps
import os
import logging

# Initialize the logger
logger = logging.getLogger(__name__)

# Create a Blueprint for portfolio-related routes
bp = Blueprint('portfolio', __name__, url_prefix='/portfolio')

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

@bp.route('/stocks', methods=['GET'])
@token_required
def get_portfolio(user_id):
    """
    Fetch the user's portfolio.
    
    Expects a valid JWT token.
    Returns the user's portfolio if the user is found.
    """
    try:
        logger.info(f"Fetching portfolio for user ID: {user_id}")
        portfolio = UserService.get_portfolio(user_id)
        logger.info(f"Successfully fetched portfolio for user ID: {user_id}")
        return jsonify(portfolio), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        logger.error(f"Error fetching portfolio for user ID {user_id}: {e}")
        return jsonify({'error': str(e)}), 500, {'Content-Type': 'application/json'}

@bp.route('/balance', methods=['GET'])
@token_required
def get_balance(user_id):
    """
    Fetch the user's balance.
    
    Expects a valid JWT token.
    Returns the user's balance if the user is found.
    """
    try:
        logger.info(f"Fetching balance for user ID: {user_id}")
        balance = UserService.get_balance(user_id)
        logger.info(f"Successfully fetched balance for user ID: {user_id}")
        return jsonify(balance), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        logger.error(f"Error fetching balance for user ID {user_id}: {e}")
        return jsonify({'error': str(e)}), 500, {'Content-Type': 'application/json'}

@bp.route('/assets_value', methods=['GET'])
@token_required
def get_assets_value(user_id):
    """
    Fetch the user's balance.
    
    Expects a valid JWT token.
    Returns the user's balance if the user is found.
    """
    try:
        logger.info(f"Fetching assets value for user ID: {user_id}")
        assets_value = UserService.get_assets_value(user_id)
        logger.info(f"Successfully fetched assets value for user ID: {user_id}")
        return jsonify(assets_value), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        logger.error(f"Error fetching assets value for user ID {user_id}: {e}")
        return jsonify({'error': str(e)}), 500, {'Content-Type': 'application/json'}
