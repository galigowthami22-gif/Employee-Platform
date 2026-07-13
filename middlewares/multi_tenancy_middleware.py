"""
Multi-Tenancy Middleware for Request Context and Tenant Isolation
"""

from typing import Optional, Callable
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
import contextvars

# Context variable for tenant ID
tenant_context: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar(
    "tenant_id", default=None
)

# Context variable for user ID
user_context: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar(
    "user_id", default=None
)

# Context variable for company ID
company_context: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar(
    "company_id", default=None
)


class MultiTenancyMiddleware(BaseHTTPMiddleware):
    """
    Middleware to handle multi-tenancy isolation.
    Extracts tenant ID from JWT and enforces row-level security.
    """
    
    async def dispatch(self, request: Request, call_next: Callable):
        """Process request and set tenant context"""
        
        # Skip for non-protected endpoints
        skip_paths = ["/api/v1/auth/login", "/api/v1/auth/register", "/docs", "/redoc"]
        if any(request.url.path.startswith(path) for path in skip_paths):
            return await call_next(request)
        
        # Extract tenant from authorization header
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            from core.authentication import JWTManager
            
            token = auth_header.split(" ")[1]
            payload = JWTManager.decode_token_without_verification(token)
            
            if payload:
                tenant_id = payload.get("company_id")
                user_id = payload.get("sub")
                
                if tenant_id:
                    tenant_context.set(tenant_id)
                    company_context.set(tenant_id)
                
                if user_id:
                    user_context.set(user_id)
        
        # Add tenant ID to request state
        request.state.tenant_id = tenant_context.get()
        request.state.user_id = user_context.get()
        request.state.company_id = company_context.get()
        
        response = await call_next(request)
        return response


def get_tenant_id() -> Optional[str]:
    """Get current tenant ID from context"""
    return tenant_context.get()


def get_user_id() -> Optional[str]:
    """Get current user ID from context"""
    return user_context.get()


def get_company_id() -> Optional[str]:
    """Get current company ID from context"""
    return company_context.get()


def ensure_tenant_context() -> str:
    """Ensure tenant context is set, raise error if not"""
    tenant_id = get_tenant_id()
    if not tenant_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tenant context not found"
        )
    return tenant_id
