from fastapi import Request
from fastapi.responses import JSONResponse


class ERPException(Exception):
    """Base exception for all ERP-related errors."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code


class NotFoundException(ERPException):
    """Exception raised when a requested resource is not found."""
    def __init__(self, message: str):
        super().__init__(message, status_code=404)


class ValidationException(ERPException):
    """Exception raised for validation errors."""
    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class DuplicateException(ERPException):
    """Exception raised when trying to create a duplicate resource."""
    def __init__(self, message: str):
        super().__init__(message, status_code=409)


class UnauthorizedException(ERPException):
    """Exception raised for unauthorized access."""
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, status_code=401)


class ForbiddenException(ERPException):
    """Exception raised for forbidden access."""
    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, status_code=403)


async def erp_exception_handler(request: Request, exc: ERPException):
    """Global exception handler for ERPException and its subclasses."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": exc.message}
    )