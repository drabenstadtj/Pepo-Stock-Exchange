from flask import Blueprint, jsonify
from app.services.leaderboard_service import LeaderboardService

bp = Blueprint('leaderboard', __name__, url_prefix='/leaderboard')

@bp.route('', methods=['GET'])
def get_leaderboard():
    try:
        leaderboard = LeaderboardService.get_leaderboard()
        return jsonify(leaderboard), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return jsonify({'error': str(e)}), 500, {'Content-Type': 'application/json'}
