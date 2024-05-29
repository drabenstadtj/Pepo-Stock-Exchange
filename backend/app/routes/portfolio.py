from flask import Blueprint, jsonify, request
from app.services.user_service import UserService

# Create a Blueprint for portfolio-related routes
bp = Blueprint('portfolio', __name__, url_prefix='/portfolio')

@bp.route('/stocks', methods=['GET'])
def get_portfolio():
    """
    Fetch the user's portfolio.
    Expects a query parameter 'user_id'.
    Returns the user's portfolio if the user is found.
    """
    user_id = request.args.get('user_id')
    portfolio = UserService.get_portfolio(user_id)
    return jsonify(portfolio)

@bp.route('/balance', methods=['GET'])
def get_balance():
    """
    Fetch the user's portfolio.
    Expects a query parameter 'user_id'.
    Returns the user's portfolio if the user is found.
    """
    user_id = request.args.get('user_id')
    portfolio = UserService.get_balance(user_id)
    return jsonify(portfolio)
