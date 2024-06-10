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
    # if request.method == 'OPTIONS':
    #     response = make_response()
    #     response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")  # Adjust this if you need specific origins
    #     response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    #     response.headers.add("Access-Control-Allow-Methods", "GET,OPTIONS")
    #     response.headers.add("Access-Control-Allow-Credentials", "true")
    #     return response, 204
    
    # try:
    #     # Retrieve the leaderboard from the service
    #     leaderboard = LeaderboardService.get_leaderboard()
    #     # Create the response
    #     response = jsonify(leaderboard)
    #     response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")  # Adjust this if you need specific origins
    #     response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    #     response.headers.add("Access-Control-Allow-Methods", "GET,OPTIONS")
    #     response.headers.add("Access-Control-Allow-Credentials", "true")
    #     return response, 200
    # except Exception as e:
    #     # Create the error response
    #     response = jsonify({'error': str(e)})
    #     response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")  # Adjust this if you need specific origins
    #     response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    #     response.headers.add("Access-Control-Allow-Methods", "GET,OPTIONS")
    #     response.headers.add("Access-Control-Allow-Credentials", "true")
    #     return response, 500
    try:
        # Retrieve the leaderboard from the service
        leaderboard = LeaderboardService.get_leaderboard()
        return jsonify(leaderboard)
    except Exception as e:
        
        return jsonify({'error': str(e)})