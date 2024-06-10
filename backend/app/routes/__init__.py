from flask import Blueprint

# Import your route modules
from .auth import bp as auth_bp
from .stocks import bp as stocks_bp
from .transactions import bp as transactions_bp
from .portfolio import bp as portfolio_bp
from .leaderboard import bp as leaderboard_bp

# Create a function to register all blueprints
def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(stocks_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(portfolio_bp)
    app.register_blueprint(leaderboard_bp)

