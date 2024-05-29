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

@bp.route('/verify_credentials', methods=['POST'])
def verify_credentials():
    """
    Verify user credentials.
    Expects JSON payload with 'username' and 'password'.
    Returns a success message and user ID if credentials are correct.
    """
    data = request.get_json()
    result = UserService.verify_credentials(data)
    if result:
        return jsonify({"message": "Credentials verified", "_id": str(result)}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401
