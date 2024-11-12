"""Definition of the resources for the authentication endpoints."""

import base64
from flask import request
from flask_jwt_extended import create_access_token
from bcrypt import checkpw

from app.utils.user_factory import create_user_instance
from ..models.user import RegularUserSchema, User
from ..extensions import DB as db
from ..models.user import UserSchema
from ..services.limiter import LIMITER as limiter
from .base_resource import BaseResource

USER_SCHEMA = UserSchema()


class UserRegisterResource(BaseResource):
    """Resource to register a new user"""

    @limiter.limit("5 per minute")
    def post(self):
        """Method to register a new user"""
        data = request.get_json()
        if User.query.filter_by(username=data["username"]).first():
            return self.make_response(
                message="Username unavailable",
                error="User with this username already exists",
                status=400,
            )
        new_user = create_user_instance(data)
        db.session.add(new_user)
        db.session.commit()
        user_schema = RegularUserSchema()
        return self.make_response(
            payload=user_schema.dump(new_user),
            message="User registered successfully",
            status=201,
        )


class UserLoginResource(BaseResource):
    """Resource to login a user"""

    @limiter.limit("10 per minute")
    def post(self):
        """Method to login a user"""
        data = request.get_json()
        user = User.query.filter_by(username=data["username"]).first()
        if user:
            password_bytes = data["password"].encode("utf-8")
            stored_hash = base64.b64decode(user.password_hash.encode("utf-8"))
            if checkpw(password_bytes, stored_hash):
                access_token = create_access_token(identity=user.id)
                return self.make_response(
                    payload={"access_token": access_token},
                    message="Logged In Successfully",
                )
        return self.make_response(
            message="Unable to Login", error="Invalid credentials", status=401
        )
