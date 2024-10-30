from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter

db = SQLAlchemy()

# Application Factory
def create_app():
    app = Flask(__name__)
    CORS(app)
    jwt = JWTManager(app)
    bcrypt = Bcrypt(app)
    app.config.from_object('config.Config')

    db.init_app(app)

    with app.app_context():
        from . import routes
        db.create_all()

    return app
