from pydantic import BaseModel, EmailStr
from typing import Optional

class RegisterSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    role_name: str

class LoginSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class RefreshSchema(BaseModel):
    refresh_token: str

class ForgotPasswordSchema(BaseModel):
    email: EmailStr

class ResetPasswordSchema(BaseModel):
    reset_token: str
    new_password: str