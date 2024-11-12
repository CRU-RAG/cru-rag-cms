"""Module to create a user instance from data."""

import base64
from uuid import uuid4
from bcrypt import gensalt, hashpw

from app.models.user import AdminUser, EditorUser, RegularUser

USER_CLASSES = {"regular": RegularUser, "admin": AdminUser, "editor": EditorUser}


def create_user_instance(data):
    """Utility function to create a user instance from data."""
    password_bytes = data["password"].encode("utf-8")
    hashed_password = hashpw(password_bytes, gensalt())
    hashed_password_str = base64.b64encode(hashed_password).decode("utf-8")
    role = data.get("role", "regular").lower()
    user_class = USER_CLASSES.get(role, USER_CLASSES["regular"])
    new_user = user_class(
        username=data["username"],
        first_name=data["first_name"],
        middle_name=data.get("middle_name", ""),
        last_name=data["last_name"],
        email=data["email"],
        phone_number=data.get("phone_number", ""),
        password_hash=hashed_password_str,
    )
    return new_user
