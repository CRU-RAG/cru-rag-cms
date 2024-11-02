"""Definition of the resources for the authentication endpoints."""
import base64
from uuid import uuid4
from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token
from bcrypt import hashpw, gensalt, checkpw
from ..models.user import User, db
from ..models.user import UserSchema
from ..services.limiter import LIMITER as limiter

USER_SCHEMA = UserSchema()

class UserRegisterResource(Resource):
    """Resource to register a new user"""
    @limiter.limit("5 per minute")
    def post(self):
        """Method to register a new user"""
        data = request.get_json()
        if User.query.filter_by(username=data['username']).first():
            return {'message': 'User already exists'}, 400
        id = str(uuid4())
        password_bytes = data['password'].encode('utf-8')
        hashed_password = hashpw(password_bytes, gensalt())
        hashed_password_str = base64.b64encode(hashed_password).decode('utf-8')
        new_user = User(
            username=data['username'],
            first_name=data['first_name'],
            middle_name=data.get('middle_name', ''),
            last_name=data['last_name'],
            email=data['email'],
            phone_number=data.get('phone_number', ''),
            password_hash=hashed_password_str
        )
        new_user.id = id
        db.session.add(new_user)
        db.session.commit()
        return USER_SCHEMA.dump(new_user), 201

class UserLoginResource(Resource):
    """Resource to login a user"""
    @limiter.limit("10 per minute")
    def post(self):
        """Method to login a user"""
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if user:
            password_bytes = data['password'].encode('utf-8')
            stored_hash = base64.b64decode(user.password_hash.encode('utf-8'))
            if checkpw(password_bytes, stored_hash):
                access_token = create_access_token(identity=user.id)
                return {'access_token': access_token, 'message': 'Logged In Successfully'}, 200
        return {'message': 'Invalid credentials'}, 401
