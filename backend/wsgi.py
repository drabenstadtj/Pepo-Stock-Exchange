import os
from app import create_app

config_name = os.getenv('FLASK_CONFIG', 'prod')  # Default to 'prod' if not set
port = int(os.getenv('BACKEND_PORT', 5000))  # Default to 5000 if not set

app = create_app(config_name=config_name)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host='0.0.0.0', port=port)
