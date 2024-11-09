"""API response classes."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from datetime import datetime


# pylint: disable=too-few-public-methods
class ApiResponse(ABC):
    """Abstract base class for API responses."""

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert the response to a dictionary."""


# pylint: disable=too-few-public-methods
class Response(ApiResponse):
    """API response class."""

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        payload: Any = None,
        message: str = None,
        error: Optional[str] = None,
        status: int = 200,
        pagination: Optional[Dict[str, Any]] = None,
        response_generated_at: Optional[str] = None,
    ):
        """Initialize the response"""
        self.payload = payload
        self.message = message
        self.error = error
        self.status = status
        self.pagination = pagination
        self.response_generated_at = response_generated_at or datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert the response to a dictionary."""
        response = {
            "status": self.status,
            "message": self.message,
            "error": self.error,
            "payload": self.payload,
            "pagination": self.pagination,
            "response_generated_at": self.response_generated_at,
        }
        return {k: v for k, v in response.items() if v is not None}
