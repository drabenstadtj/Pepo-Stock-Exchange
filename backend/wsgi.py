import os
import logging
from logging.config import dictConfig
from app import create_app

# Configure logging
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

config_name = os.getenv('CONFIG', 'development')  # Default to 'dev' if not set
port = int(os.getenv('BACKEND_PORT', 5000))  # Default to 5000 if not set

app = create_app(config_name=config_name)

if __name__ == "__main__":
    from waitress import serve

    app.logger.info('Starting Pepo Stock Exchange application...')
    serve(app, host='0.0.0.0', port=port)
