# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # reads your .env file into environment variables

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-fallback-key-change-in-prod')
    DATABASE = os.path.join('/tmp', 'bthub.db')
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

# This dict lets you switch configs by name (useful later for hosting)
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}