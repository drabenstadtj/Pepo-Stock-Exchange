from flask import Blueprint, jsonify, request, make_response
from app.services.leaderboard_service import LeaderboardService
from flask_cors import CORS

# Create a Blueprint for leaderboard-related routes
bp = Blueprint('leaderboard', __name__, url_prefix='/leaderboard')

#Apply CORS
CORS(bp, supports_credentials=True)

@bp.route('', methods=['GET', 'OPTIONS'])
def get_leaderboard():
    """
    Fetch the current leaderboard.
    
    Returns a JSON object with the leaderboard data.
    """
    try:
        # Retrieve the leaderboard from the service
        leaderboard = LeaderboardService.get_leaderboard()
        return jsonify(leaderboard)
    except Exception as e:
        
        return jsonify({'error': str(e)})