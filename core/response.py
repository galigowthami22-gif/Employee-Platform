"""
Response Wrappers
Standard response models and functions for consistent API responses.
"""

from pydantic import BaseModel
from typing import Generic, Optional, Any, TypeVar

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """Standard API response wrapper."""
    success: bool
    message: str
    data: Optional[T] = None
    status_code: int = 200

    model_config = {
        "from_attributes": True
    }


def success_response(message: str, data=None, status_code: int = 200):
    """Create a successful response."""
    return {
        "success": True,
        "message": message,
        "data": data,
        "status_code": status_code
    }


def error_response(message: str, status_code: int = 400):
    """Create an error response."""
    return {
        "success": False,
        "message": message,
        "status_code": status_code
    }