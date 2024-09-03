import os
from app import create_app

config_name = os.getenv('FLASK_CONFIG', 'dev') or 'dev'

app = create_app(config_name=config_name)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv('BACKEND_PORT', 5000)))
