from flask import Blueprint, request, jsonify, current_app
from app.services.user_service import UserService
import jwt
import datetime
from functools import wraps
import logging

# Initialize the logger
logger = logging.getLogger(__name__)

# Create a Blueprint for authentication-related routes
bp = Blueprint('auth', __name__, url_prefix='/auth')

# Decorator to check if a valid token is provided
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Get the token from the Authorization header
        token = request.headers.get('Authorization')
        if not token:
            logger.warning("Token is missing")
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            # Split the token from the Bearer schema
            token = token.split()[1]
            # Decode the token using the secret key
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
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

# Route to verify user credentials and issue a token
@bp.route('/verify_credentials', methods=['POST'])
def verify_credentials():
    data = request.get_json()
    logger.info(f"Received request data: {data}")
    user_id = UserService.verify_credentials(data)
    if user_id:
        # Generate JWT token valid for 24 hours
        token = jwt.encode({
            'user_id': str(user_id),
            'exp': datetime.datetime.now() + datetime.timedelta(hours=24)
        }, current_app.config['SECRET_KEY'], algorithm="HS256")
        logger.info(f"Generated token for user {user_id}")
        return jsonify({"message": "Credentials verified", "token": token}), 200
    else:
        logger.warning("Invalid username or password")
        return jsonify({"error": "Invalid username or password"}), 401

# Route to register a new user
@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    logger.info(f"Registering new user with data: {data}")
    result = UserService.register_user(data)
    if result['message'] == "User registered successfully":
        logger.info(f"User {data['username']} registered successfully")
    else:
        logger.error(f"Error registering user {data['username']}")
    return jsonify(result)

# Route to get the user ID by username, token required
@bp.route('/get_user_id', methods=['GET'])
@token_required
def get_user_id(current_user):
    username = request.args.get('username')
    logger.info(f"Fetching user ID for username: {username}")
    user_id = UserService.get_user_id(username)
    if user_id:
        logger.info(f"Found user ID for username {username}: {user_id}")
        return jsonify({"_id": str(user_id)}), 200
    else:
        logger.warning(f"User not found for username: {username}")
        return jsonify({"error": "User not found"}), 404
