from fastapi import Request
from fastapi.responses import JSONResponse

class ERPException(Exception):
    def _init_(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code

async def erp_exception_handler(request: Request, exc: ERPException):
    return JSONResponse(status_code=exc.status_code, content={"success": False, "message": exc.message})