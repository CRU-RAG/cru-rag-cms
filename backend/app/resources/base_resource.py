"""Base resource class to handle common operations."""
from flask_restful import Resource
from .api_response import Response

class BaseResource(Resource):
    """Base resource class to handle common operations."""

    def __init__(self):
        self.response = Response()

    def make_response(self, payload=None, message=None, error=None, status=200, pagination=None):
        """Helper method to create a response."""
        self.response.payload = payload
        self.response.message = message
        self.response.error = error
        self.response.status = status
        self.response.pagination = pagination
        return self.response.to_dict(), status