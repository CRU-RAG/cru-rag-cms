import base64
from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from bcrypt import hashpw, gensalt, checkpw
from ..models.user import User, db
from ..models.user import UserSchema
from ..services.limiter import limiter

user_schema = UserSchema()

class UserRegisterResource(Resource):
    @limiter.limit("5 per minute")
    def post(self):
        data = request.get_json()
        if User.query.filter_by(username=data['username']).first():
            return {'message': 'User already exists'}, 400
        password_bytes = data['password'].encode('utf-8')
        hashed_password = hashpw(password_bytes, gensalt())
        hashed_password_str = base64.b64encode(hashed_password).decode('utf-8')
        new_user = User(username=data['username'], password_hash=hashed_password_str)
        db.session.add(new_user)
        db.session.commit()
        return user_schema.dump(new_user), 201

class UserLoginResource(Resource):
    @limiter.limit("10 per minute")
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if user:
            password_bytes = data['password'].encode('utf-8')
            stored_hash = base64.b64decode(user.password_hash.encode('utf-8'))
            if checkpw(password_bytes, stored_hash):
                access_token = create_access_token(identity=user.id)
                return {'access_token': access_token, 'msg': 'Registered Successfully'}, 200
        return {'message': 'Invalid credentials'}, 401
