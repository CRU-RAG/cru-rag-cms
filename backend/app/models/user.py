"""User model"""
from datetime import datetime
from enum import Enum
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from ..extensions import DB as db

class UserRole(Enum):
    ADMIN = "ADMIN"
    EDITOR = "EDITOR"
    REGULAR = "REGULAR"

class User(db.Model):
    """Users model"""
    __tablename__ = 'users'

    id = db.Column(db.String(100), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    middle_name = db.Column(db.String(80), nullable=True)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    status = db.Column(db.Boolean, default=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    role = db.Column(
        db.Enum(UserRole, name='user_role', native_enum=False), 
        nullable=False, 
        default=UserRole.REGULAR
    )

    def __init__(self, username, password_hash, first_name, middle_name, last_name, email, phone_number):
        """Initialize user"""
        self.username = username
        self.password_hash = password_hash
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number

class UserSchema(SQLAlchemyAutoSchema):
    """User Schema"""
    class Meta:
        """Meta class for User Schema"""
        model = User
        load_instance = True
        exclude = ("password_hash",)
