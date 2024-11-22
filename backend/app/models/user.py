"""User model"""

from datetime import datetime
from uuid import uuid4
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from ..extensions import DB as db


# pylint: disable=too-many-instance-attributes
# pylint: disable=too-few-public-methods
class User(db.Model):
    """Users model"""

    __tablename__ = "users"

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
    role = db.Column(db.String(50), nullable=False)

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        username,
        password_hash,
        first_name,
        middle_name,
        last_name,
        email,
        phone_number,
        role,
    ):
        """Initialize user"""
        self.id = str(uuid4())
        self.username = username
        self.password_hash = password_hash
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.role = role


class RegularUser(User):
    """Regular User model"""

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        username,
        password_hash,
        first_name,
        middle_name,
        last_name,
        email,
        phone_number,
    ):
        super().__init__(
            username,
            password_hash,
            first_name,
            middle_name,
            last_name,
            email,
            phone_number,
            "regular",
        )


class EditorUser(User):
    """Editor User model"""

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        username,
        password_hash,
        first_name,
        middle_name,
        last_name,
        email,
        phone_number,
    ):
        super().__init__(
            username,
            password_hash,
            first_name,
            middle_name,
            last_name,
            email,
            phone_number,
            "editor",
        )


class AdminUser(User):
    """Admin User model"""

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        username,
        password_hash,
        first_name,
        middle_name,
        last_name,
        email,
        phone_number,
    ):
        super().__init__(
            username,
            password_hash,
            first_name,
            middle_name,
            last_name,
            email,
            phone_number,
            "admin",
        )


class UserSchema(SQLAlchemyAutoSchema):
    """Base User Schema"""

    class Meta:
        """Meta class for User Schema"""

        model = User
        load_instance = True
        exclude = ("password_hash",)


class RegularUserSchema(UserSchema):
    """Regular User Schema"""

    class Meta(UserSchema.Meta):
        """Meta class for Regular User Schema"""

        model = RegularUser


class EditorUserSchema(UserSchema):
    """Editor User Schema"""

    class Meta(UserSchema.Meta):
        """Meta class for Editor User Schema"""

        model = EditorUser


class AdminUserSchema(UserSchema):
    """Admin User Schema"""

    class Meta(UserSchema.Meta):
        """Meta class for Admin User Schema"""

        model = AdminUser
