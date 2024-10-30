"""Module to define the KnowledgeBase model"""
from flask_bcrypt import bcrypt
from . import db

class KnowledgeBase(db.Model):
    """KnowledgeBase Model"""
    id = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(5000), nullable=False)

    def to_dict(self):
        """Method to return a dictionary of the model"""
        short_content = self.content[:50] + '...' if len(self.content) > 50 else self.content
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'short_content': short_content
        }

    def __repr__(self):
        """Method to return a string representation of the model"""
        return f"Item('{self.name}', '{self.description}')"

class User(db.Model):
    """Users model"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, username, password):
        """Initialize user"""
        self.username = username
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        """Check user password"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
