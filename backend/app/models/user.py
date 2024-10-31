"""User model"""
from datetime import datetime
from ..extensions import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class User(db.Model):
    """Users model"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, username, password_hash):
        """Initialize user"""
        self.username = username
        self.password_hash = password_hash

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ("password_hash",)
