from fastapi import APIRouter, Depends, HTTPException, Request, Form
from sqlalchemy.orm import Session
from schemas.auth_schema import RegisterSchema, LoginSchema, RefreshSchema, ForgotPasswordSchema, ResetPasswordSchema
from models.user_model import User
from models.role_model import Role
from models.refresh_token_model import RefreshToken
from models.password_reset_model import PasswordReset
from core.database import get_db
from jose import jwt
from core.config import settings
from utils.security import hash_password, verify_password
from utils.jwt import create_access_token, create_refresh_token
from dependencies.dependency import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
def register_user(payload: RegisterSchema, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        return {"Info": "Email already exists"}

    role = db.query(Role).filter(Role.name == payload.role_name).first()
    if not role:
        raise HTTPException(status_code=400, detail="Role not found")

    user = User(
        username=payload.username,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role_id=role.id
    )

    db.add(user)
    db.commit()

    return {"Info": "User registered"}

@router.post("/login")
async def login(request: Request,
                username: str | None = Form(None),
                email_form: str | None = Form(None),
                password_form: str | None = Form(None),
                db: Session = Depends(get_db)):
    # Support both JSON and form data for tests and clients; form fields are
    # declared so OpenAPI shows `username`/`email` and `password`.
    data = {}
    try:
        data = await request.json()
    except Exception:
        form = await request.form()
        data = dict(form)

    # prefer JSON body values, then form values
    email_or_username = data.get("email") or data.get("username") or email_form or username
    password = data.get("password") or password_form

    if not email_or_username or not password:
        raise HTTPException(status_code=400, detail="username/email and password required")

    # allow login by email or username
    user = db.query(User).filter((User.email == email_or_username) | (User.username == email_or_username)).first()

    if not user:
        return {"Info": "Invalid credentials"}

    if not verify_password(password, user.hashed_password):
        return {"Info": "Invalid credentials"}
    
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    token_db = RefreshToken(user_id=user.id, token=refresh_token)

    db.add(token_db)
    db.commit()

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return {"id": current_user.id, "username": current_user.username, "email": current_user.email}

@router.post("/refresh")
def refresh_access_token(payload: RefreshSchema):
    try:
        decoded = jwt.decode(payload.refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = decoded["sub"]
        access_token = create_access_token({"sub": user_id})
        return {"access_token": access_token}
    except:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
@router.post("/forgot-password")
def forgot_password(payload: ForgotPasswordSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        return {"Info": "User not found"}

    reset_token = create_access_token({"sub": str(user.id)})
    token_record = PasswordReset(email=user.email, reset_token=reset_token)
    db.add(token_record)
    db.commit()
    return {"Info": "Reset token generated", "reset_token": reset_token}

@router.post("/reset-password")
def reset_password(payload: ResetPasswordSchema, db: Session = Depends(get_db)):
    token_record = db.query(PasswordReset).filter(PasswordReset.reset_token == payload.reset_token).first()

    if not token_record:
        raise HTTPException(status_code=400, detail="Invalid token")

    decoded = jwt.decode(payload.reset_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    user_id = decoded.get("sub")
    user = db.query(User).filter(User.id == int(user_id)).first()
    user.hashed_password = hash_password(payload.new_password)
    db.commit()
    return {"Info": "Password updated"}