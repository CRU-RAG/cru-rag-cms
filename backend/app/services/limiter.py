"""Rate limiting service for Flask app."""
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

LIMITER = Limiter(key_func=get_remote_address)
