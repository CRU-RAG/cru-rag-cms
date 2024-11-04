"""API response classes."""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class ApiResponse(ABC):
    """Abstract base class for API responses."""

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert the response to a dictionary."""
        pass

class Response(ApiResponse):
    """API response class."""

    def __init__(
        self,
        data: Any = None,
        message: str = None,
        error: Optional[str] = None,
        status: int = 200,
    ):
        """Initialize the response"""
        self.message = message
        self.error = error
        self.data = data
        self.status = status
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the response to a dictionary."""
        response = {
            "status": self.status,
            "message": self.message,
            "error": self.error,
            "data": self.data,
        }
        return {k: v for k, v in response.items() if v is not None}
