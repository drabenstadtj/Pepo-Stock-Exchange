import os
from dotenv import load_dotenv

load_dotenv()  # This loads the environment variables from a .env file in the backend directory

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    SESSION_SECRET = os.getenv('SESSION_SECRET', 'default_session_secret')
    MONGO_URI = os.getenv('DATABASE_URI', 'mongodb://localhost:27017/')
    CORS_ORIGINS = os.getenv('http://localhost:3000, http://192.168.68.250:3000', '*')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config_by_name = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig
}
