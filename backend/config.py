"""Configuration file for the Flask application."""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Set Flask configuration vars from .env file."""
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
