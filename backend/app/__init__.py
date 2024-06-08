from flask import Flask
from .config import config_by_name
from flask_pymongo import PyMongo
from flask_cors import CORS
import logging

mongo = PyMongo()

def create_app(config_name='prod'):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Initialize PyMongo
    mongo.init_app(app)

    # Enable CORS for the app
    CORS(app, origins=app.config['CORS_ORIGINS'])

    # Register blueprints
    from .routes import register_routes
    register_routes(app)

    # Configure logging
    if config_name == 'prod':
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.DEBUG)

    return app
