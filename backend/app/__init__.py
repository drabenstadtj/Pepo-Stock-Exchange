from flask import Flask
from .config import Config
from flask_pymongo import PyMongo
from flask_cors import CORS

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize PyMongo
    mongo.init_app(app)

    # Enable CORS for the app
    CORS(app)

    # Register blueprints
    from .routes import register_routes
    register_routes(app)

    return app
