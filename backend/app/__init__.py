from flask import Flask, request
from flask_pymongo import PyMongo
from flask_cors import CORS
import logging
from .config import config_by_name

mongo = PyMongo()

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Initialize extensions
    mongo.init_app(app)
    CORS(app)

    # Register blueprints
    from .routes import register_routes
    register_routes(app)

    # Configure logging
<<<<<<< HEAD
    logging.basicConfig(level=logging.DEBUG if config_name != 'prod' else logging.INFO)
=======
    if config_name == 'production':
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.DEBUG)

>>>>>>> bc5033d2621a4bc9d0d429c9ab1308ffa78884d4
    logger = logging.getLogger(__name__)

    @app.before_request
    def log_request():
        logger.debug(f"Request: {request.method} {request.url} {request.host}")
        logger.debug(f"Request Headers: {dict(request.headers)}")
        if request.method in ['POST', 'PUT', 'PATCH'] and request.json:
            logger.debug(f"Request JSON Body: {request.json}")
        elif request.form:
            logger.debug(f"Request Form Body: {request.form}")

    @app.after_request
    def log_response(response):
        logger.debug(f"Response: {response.status_code}")
        logger.debug(f"Response Headers: {dict(response.headers)}")
        return response

    return app
