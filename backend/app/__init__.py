"""Entry point for the application."""

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_restful import Api

from app.resources.comment_resources import CommentListResource, CommentResource
from .resources.content_resources import ContentListResource, ContentResource
from .resources.auth_resources import UserRegisterResource, UserLoginResource
from .resources.user_resources import UserListResource, UserResource
from .services.limiter import LIMITER as limiter
from .extensions import DB as db
from .resources.api_response import Response


# Application Factory
def create_app():
    """Create a Flask application."""
    app = Flask(__name__)
    CORS(app)
    JWTManager(app)
    Bcrypt(app)
    api = Api(app)
    api.add_resource(ContentListResource, "/contents")
    api.add_resource(ContentResource, "/contents/<string:content_id>")
    api.add_resource(CommentListResource, "/comments")
    api.add_resource(CommentResource, "/comments/<string:comment_id>")
    api.add_resource(UserListResource, "/users")
    api.add_resource(UserResource, "/users/<string:user_id>")
    api.add_resource(UserRegisterResource, "/register")
    api.add_resource(UserLoginResource, "/login")
    app.config.from_object("config.Config")

    db.init_app(app)
    limiter.init_app(app)

    # @app.errorhandler(Exception)
    # def handle_exception(e):
    #     """Handle uncaught exceptions"""
    #     db.session.rollback()
    #     response = Response(
    #         message="Something went wrong. Please try again later.",
    #         error=str(e),
    #         status=500,
    #     )
    #     return response.to_dict(), 500

    with app.app_context():
        db.create_all()

    return app
