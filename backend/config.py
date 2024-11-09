"""Configuration file for the Flask application."""

import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


# pylint: disable=too-few-public-methods
class Config:
    """Set Flask configuration vars from .env file."""

    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
