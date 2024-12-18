"""Definitions of user resources."""

from datetime import datetime
from flask import request
from flask_jwt_extended import jwt_required

from app.utils.pagination import get_pagination_info
from app.utils.user_factory import create_user_instance
from .base_resource import BaseResource
from ..models.user import (
    User,
    UserSchema,
    RegularUserSchema,
    EditorUserSchema,
    AdminUserSchema,
)
from ..extensions import DB as db
from ..middlewares.is_admin import is_admin
from ..middlewares.is_admin_or_self import is_admin_or_self

USER_SCHEMA = UserSchema()
USERS_SCHEMA = UserSchema(many=True)

USER_SCHEMAS = {
    "regular": RegularUserSchema(),
    "admin": AdminUserSchema(),
    "editor": EditorUserSchema(),
}


class UserListResource(BaseResource):
    """Resource to handle listing users (admin only)."""

    @jwt_required()
    @is_admin
    def get(self):
        """Get a list of all users (admin only)."""
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 15, type=int)
        pagination_object = User.query.filter(User.deleted_at.is_(None)).paginate(
            page=page, per_page=per_page
        )
        users = pagination_object.items
        pagination_info = get_pagination_info(pagination_object)
        return self.make_response(
            payload=USERS_SCHEMA.dump(users),
            pagination=pagination_info,
            message="Users retrieved successfully",
        )

    @jwt_required()
    @is_admin
    def post(self):
        """Create a new user (admin only)."""
        data = request.get_json()
        if User.query.filter_by(username=data["username"]).first():
            return self.make_response(
                message="Unable to create user", error="User already exists", status=400
            )
        new_user = create_user_instance(data)
        db.session.add(new_user)
        db.session.commit()
        user_schema = USER_SCHEMAS.get(new_user.role, RegularUserSchema())
        return self.make_response(
            payload=user_schema.dump(new_user),
            message="User created successfully",
            status=201,
        )


class UserResource(BaseResource):
    """Resource to handle user operations (admin only)."""

    @jwt_required()
    @is_admin_or_self
    def get(self, user_id):
        """Get a user by ID (admin and the user only)."""
        user = User.query.filter(User.deleted_at.is_(None), User.id == user_id).first()
        if not user:
            return self.make_response(
                message="Unable to retrieve user", error="User not found", status=404
            )
        return self.make_response(
            payload=USER_SCHEMA.dump(user),
            message="User retrieved successfully",
        )

    @jwt_required()
    @is_admin_or_self
    def delete(self, user_id):
        """Delete a user by ID (admin only)."""
        user_to_delete = User.query.filter(
            User.deleted_at.is_(None), User.id == user_id
        ).first()
        if not user_to_delete:
            return self.make_response(
                message="Unable to delete user", error="User not found", status=404
            )
        if user_to_delete.role == "admin":
            return self.make_response(
                message="Unable to delete user",
                error="The user is an admin",
                status=400,
            )
        user_to_delete.deleted_at = datetime.now()
        db.session.commit()
        return self.make_response(
            message="User deleted successfully",
        )

    @jwt_required()
    @is_admin
    def put(self, user_id):
        """Promote a user to admin (admin only)."""
        user_to_modify = User.query.filter(
            User.deleted_at.is_(None), User.id == user_id
        ).first()
        if not user_to_modify:
            return self.make_response(
                message="Unable to update user role", error="User not found", status=404
            )
        if user_to_modify.role == "admin":
            return self.make_response(
                message="Unable to update user role",
                error="User is an admin",
                status=400,
            )
        data = request.get_json()
        if "role" in data and data["role"].lower() in ["admin", "editor", "regular"]:
            user_to_modify.updated_at = datetime.now()
            user_to_modify.role = data["role"].lower()
            db.session.commit()
            return self.make_response(
                payload=USER_SCHEMA.dump(user_to_modify),
                message="User role updated successfully",
            )
        return self.make_response(
            message="Unable to update user role", error="Invalid role", status=400
        )
