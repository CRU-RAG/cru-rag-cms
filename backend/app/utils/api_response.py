"""API response classes."""
from abc import ABC, abstractmethod
from typing import Any, Dict

class ApiResponse(ABC):
    """Abstract base class for API responses."""

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert the response to a dictionary."""
        pass

class SuccessResponse(ApiResponse):
    """API response for successful operations."""

    def __init__(self, data: Any = None, message: str = "Success"):
        """Initialize the success response."""
        self.status = "success"
        self.message = message
        self.data = data

    def to_dict(self) -> Dict[str, Any]:
        """Convert the response to a dictionary."""
        response = {
            "status": self.status,
            "message": self.message,
        }
        if self.data is not None:
            response["data"] = self.data
        return response

class ErrorResponse(ApiResponse):
    """API response for error situations."""

    def __init__(self, message: str = "An error occurred", errors: Any = None):
        self.status = "error"
        self.message = message
        self.errors = errors

    def to_dict(self) -> Dict[str, Any]:
        response = {
            "status": self.status,
            "message": self.message
        }
        if self.errors is not None:
            response["errors"] = self.errors
        return response
