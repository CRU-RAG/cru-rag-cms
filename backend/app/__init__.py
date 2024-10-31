"""Entry point for the application."""
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_restful import Api
from .resources.content_resources import ContentListResource, ContentResource
from .resources.auth_resources import UserRegisterResource, UserLoginResource
from .services.limiter import LIMITER as limiter
from .extensions import DB as db

# Application Factory
def create_app():
    """Create a Flask application."""
    app = Flask(__name__)
    CORS(app)
    JWTManager(app)
    Bcrypt(app)
    api = Api(app)
    api.add_resource(ContentListResource, '/contents')
    api.add_resource(ContentResource, '/contents/<string:id>')
    api.add_resource(UserRegisterResource, '/register')
    api.add_resource(UserLoginResource, '/login')
    app.config.from_object('config.Config')

    db.init_app(app)
    limiter.init_app(app)

    with app.app_context():
        # from . import routes
        db.create_all()

    return app
