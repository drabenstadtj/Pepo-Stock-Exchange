from flask import Blueprint, jsonify
from app.services.leaderboard_service import LeaderboardService

# Create a Blueprint for leaderboard-related routes
bp = Blueprint('leaderboard', __name__, url_prefix='/leaderboard')

@bp.route('', methods=['GET'])
def get_leaderboard():
    """
    Fetch the current leaderboard.
    
    Returns a JSON object with the leaderboard data.
    """
    try:
        # Retrieve the leaderboard from the service
        leaderboard = LeaderboardService.get_leaderboard()
        # Return the leaderboard data as JSON with a 200 status code
        
        return jsonify(leaderboard), 200
    except Exception as e:
        # Return an error message and a 500 status code if an exception occurs
        return jsonify({'error': str(e)}), 500
