from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
import jwt
import datetime
from functools import wraps
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')

bp = Blueprint('auth', __name__, url_prefix='/auth')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
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

@bp.route('/verify_credentials', methods=['POST'])
def verify_credentials():
    data = request.get_json()
    print(f"Received request data: {data}")  # Debug: Log received request data
    user_id = UserService.verify_credentials(data)
    if user_id:
        token = jwt.encode({
            'user_id': str(user_id),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm="HS256")
        print(f"Generated token: {token}")  # Debug: Log generated token
        return jsonify({"message": "Credentials verified", "token": token}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

@bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    Expects JSON payload with 'username' and 'password'.
    Returns a success message upon successful registration.
    """
    data = request.get_json()
    result = UserService.register_user(data)
    return jsonify(result)

@bp.route('/get_user_id', methods=['GET'])
@token_required
def get_user_id(current_user):
    """
    Fetch the user ID by username.
    Expects a query parameter 'username'.
    Returns the user ID if found, or an error message if not found.
    """
    username = request.args.get('username')
    user_id = UserService.get_user_id(username)
    if user_id:
        return jsonify({"_id": str(user_id)}), 200
    else:
        return jsonify({"error": "User not found"}), 404


