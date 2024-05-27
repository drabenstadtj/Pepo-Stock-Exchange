from flask import Blueprint, request, jsonify
from app.services.user_service import UserService

# Create a Blueprint for authentication-related routes
bp = Blueprint('auth', __name__, url_prefix='/auth')

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
def get_user_id():
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
