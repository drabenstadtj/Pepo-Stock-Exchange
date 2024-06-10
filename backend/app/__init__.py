from flask import Flask, request
from .config import config_by_name
from flask_pymongo import PyMongo
import logging
from flask_cors import CORS

mongo = PyMongo()

def create_app(config_name='prod'):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Setup CORS using the configuration
    cors_origins = app.config['CORS_ORIGINS'].split(',')
    CORS(app, resources={r"/*": {"origins": cors_origins}}, supports_credentials=True)

    # Initialize PyMongo
    mongo.init_app(app)

    # Register blueprints
    from .routes import register_routes
    register_routes(app)

    # Configure logging
    if config_name == 'prod':
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.DEBUG)

    logger = logging.getLogger(__name__)

    @app.before_request
    def log_request():
        logger.debug(f"Request: {request.method} {request.url}")
        logger.debug(f"Request Headers: {dict(request.headers)}")
        if request.method in ['POST', 'PUT', 'PATCH'] and request.json:
            logger.debug(f"Request JSON Body: {request.json}")
        elif request.form:
            logger.debug(f"Request Form Body: {request.form}")

    @app.after_request
    def log_response(response):
        logger.debug(f"Response: {response.status_code}")
        logger.debug(f"Response Headers: {dict(response.headers)}")
        logger.debug(f"Response Body: {response.get_data(as_text=True)}")
        return response

    return app
