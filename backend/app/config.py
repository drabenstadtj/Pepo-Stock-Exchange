import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/gourdstocks')
