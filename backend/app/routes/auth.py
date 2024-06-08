from flask import Blueprint, request, jsonify, current_app
from app.services.user_service import UserService
import jwt
import datetime
from functools import wraps
import logging

# Create a Blueprint for authentication-related routes
bp = Blueprint('auth', __name__, url_prefix='/auth')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            token = token.split()[1]
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 403
        except Exception as e:
            logging.error(f"Token verification error: {e}")
            return jsonify({'message': 'Token verification failed!'}), 403

        return f(user_id, *args, **kwargs)

    return decorated

@bp.route('/verify_credentials', methods=['POST'])
def verify_credentials():
    data = request.get_json()
    logging.info(f"Received request data: {data}")
    user_id = UserService.verify_credentials(data)
    if user_id:
        token = jwt.encode({
            'user_id': str(user_id),
            'exp': datetime.datetime.now() + datetime.timedelta(hours=24)
        }, current_app.config['SECRET_KEY'], algorithm="HS256")
        logging.info(f"Generated token: {token}")
        return jsonify({"message": "Credentials verified", "token": token}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    result = UserService.register_user(data)
    return jsonify(result)

@bp.route('/get_user_id', methods=['GET'])
@token_required
def get_user_id(current_user):
    username = request.args.get('username')
    user_id = UserService.get_user_id(username)
    if user_id:
        return jsonify({"_id": str(user_id)}), 200
    else:
        return jsonify({"error": "User not found"}), 404
