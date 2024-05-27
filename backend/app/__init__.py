from flask import Flask
from .config import Config
from flask_pymongo import PyMongo

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize PyMongo
    mongo.init_app(app)

    # Register blueprints
    from .routes import register_routes
    register_routes(app)

    return app
