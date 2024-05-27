from flask import Blueprint, jsonify, request
from app.services.user_service import UserService

bp = Blueprint('portfolio', __name__, url_prefix='/portfolio')

@bp.route('/', methods=['GET'])
def get_portfolio():
    user_id = request.args.get('user_id')
    portfolio = UserService.get_portfolio(user_id)
    return jsonify(portfolio)
