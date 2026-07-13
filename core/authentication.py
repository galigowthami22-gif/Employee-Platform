"""
PHASE 7: AUTHENTICATION PLATFORM
JWT authentication with refresh tokens, MFA, password policies, and device management.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from jose import jwt
from jose.exceptions import JWTError
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
import secrets
from functools import wraps

from core.config import settings, get_settings


# Password hashing context
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=settings.BCRYPT_LOG_ROUNDS
)


class Token(BaseModel):
    """Token response model"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenPayload(BaseModel):
    """JWT token payload"""
    sub: str  # user_id
    company_id: str
    roles: list
    permissions: list
    iat: float
    exp: float
    type: str  # access or refresh


class MFASetup(BaseModel):
    """MFA setup response"""
    secret_key: str
    qr_code_url: str
    backup_codes: list


class DeviceInfo(BaseModel):
    """Device information"""
    device_id: str
    device_name: str
    device_type: str  # mobile, desktop, tablet
    os_version: str
    browser_version: str
    ip_address: str
    is_trusted: bool = False


class PasswordPolicy:
    """Password policy validator"""
    
    MIN_LENGTH = 12
    REQUIRE_UPPERCASE = True
    REQUIRE_LOWERCASE = True
    REQUIRE_DIGITS = True
    REQUIRE_SPECIAL = True
    SPECIAL_CHARS = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    COMMON_PASSWORDS = [
        "password", "123456", "12345678", "qwerty", "abc123",
        "monkey", "1234567", "letmein", "trustno1", "dragon"
    ]
    
    @classmethod
    def validate(cls, password: str) -> tuple[bool, Optional[str]]:
        """
        Validate password against policy
        Returns: (is_valid, error_message)
        """
        if len(password) < cls.MIN_LENGTH:
            return False, f"Password must be at least {cls.MIN_LENGTH} characters"
        
        if cls.REQUIRE_UPPERCASE and not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter"
        
        if cls.REQUIRE_LOWERCASE and not any(c.islower() for c in password):
            return False, "Password must contain at least one lowercase letter"
        
        if cls.REQUIRE_DIGITS and not any(c.isdigit() for c in password):
            return False, "Password must contain at least one digit"
        
        if cls.REQUIRE_SPECIAL and not any(c in cls.SPECIAL_CHARS for c in password):
            return False, f"Password must contain at least one special character: {cls.SPECIAL_CHARS}"
        
        if password.lower() in cls.COMMON_PASSWORDS:
            return False, "Password is too common, please choose a stronger password"
        
        return True, None


class PasswordHasher:
    """Password hashing and verification"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt"""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify plain password against hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def needs_rehash(hashed_password: str) -> bool:
        """Check if password hash needs updating"""
        return pwd_context.needs_update(hashed_password)


class JWTManager:
    """JWT token generation and validation"""
    
    @staticmethod
    def create_access_token(
        user_id: str,
        company_id: str,
        roles: list,
        permissions: list,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT access token"""
        if expires_delta is None:
            expires_delta = timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        
        expire = datetime.now(timezone.utc) + expires_delta
        
        payload = {
            "sub": user_id,
            "company_id": company_id,
            "roles": roles,
            "permissions": permissions,
            "type": "access",
            "iat": datetime.now(timezone.utc).timestamp(),
            "exp": expire.timestamp()
        }
        
        encoded_jwt = jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        return encoded_jwt
    
    @staticmethod
    def create_refresh_token(
        user_id: str,
        company_id: str,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT refresh token"""
        if expires_delta is None:
            expires_delta = timedelta(
                days=settings.REFRESH_TOKEN_EXPIRE_DAYS
            )
        
        expire = datetime.now(timezone.utc) + expires_delta
        
        payload = {
            "sub": user_id,
            "company_id": company_id,
            "type": "refresh",
            "iat": datetime.now(timezone.utc).timestamp(),
            "exp": expire.timestamp()
        }
        
        encoded_jwt = jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> Optional[TokenPayload]:
        """Verify JWT token and return payload"""
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            return TokenPayload(**payload)
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    @staticmethod
    def decode_token_without_verification(token: str) -> Optional[Dict[str, Any]]:
        """Decode token without verification (for claims inspection)"""
        try:
            payload = jwt.decode(
                token,
                options={"verify_signature": False}
            )
            return payload
        except Exception:
            return None


class MFAManager:
    """Multi-Factor Authentication manager"""
    
    BACKUP_CODES_COUNT = 10
    
    @staticmethod
    def generate_secret() -> str:
        """Generate TOTP secret key"""
        try:
            import pyotp
        except ImportError:
            raise RuntimeError("pyotp is required for MFA operations")
        return pyotp.random_base32()
    
    @staticmethod
    def generate_qr_code(
        secret: str,
        user_email: str,
        issuer: str = "Stackly ERP"
    ) -> str:
        """Generate QR code URL for TOTP setup"""
        try:
            import pyotp
        except ImportError:
            raise RuntimeError("pyotp is required for MFA operations")
        totp = pyotp.TOTP(secret)
        return totp.provisioning_uri(
            name=user_email,
            issuer_name=issuer
        )
    
    @staticmethod
    def verify_totp(secret: str, token: str, window: int = 1) -> bool:
        """Verify TOTP token"""
        try:
            import pyotp
        except ImportError:
            raise RuntimeError("pyotp is required for MFA operations")
        totp = pyotp.TOTP(secret)
        # Allow slight time drift (window)
        return totp.verify(token, valid_window=window)
    
    @staticmethod
    def generate_backup_codes() -> list:
        """Generate backup codes for account recovery"""
        codes = []
        for _ in range(MFAManager.BACKUP_CODES_COUNT):
            code = secrets.token_hex(4)  # 8 character hex codes
            codes.append(code)
        return codes
    
    @staticmethod
    def hash_backup_code(code: str) -> str:
        """Hash backup code for storage"""
        return PasswordHasher.hash_password(code)
    
    @staticmethod
    def verify_backup_code(plain_code: str, hashed_code: str) -> bool:
        """Verify backup code"""
        return PasswordHasher.verify_password(plain_code, hashed_code)


class SessionManager:
    """Session and device management"""
    
    @staticmethod
    def generate_session_id() -> str:
        """Generate unique session ID"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def generate_device_id() -> str:
        """Generate unique device ID"""
        return secrets.token_urlsafe(16)
    
    @staticmethod
    def create_device_fingerprint(device_info: DeviceInfo) -> str:
        """Create device fingerprint from device info"""
        fingerprint_data = f"{device_info.device_type}:{device_info.os_version}:{device_info.browser_version}"
        return secrets.token_hex(8)  # Placeholder - in production, use proper fingerprinting


class AuthenticationService:
    """Main authentication service"""
    
    def __init__(self):
        self.password_hasher = PasswordHasher()
        self.jwt_manager = JWTManager()
        self.mfa_manager = MFAManager()
        self.session_manager = SessionManager()
    
    def authenticate_user(
        self,
        password: str,
        hashed_password: str
    ) -> bool:
        """Authenticate user with password"""
        return self.password_hasher.verify_password(password, hashed_password)
    
    def generate_tokens(
        self,
        user_id: str,
        company_id: str,
        roles: list,
        permissions: list
    ) -> Token:
        """Generate access and refresh tokens"""
        access_token = self.jwt_manager.create_access_token(
            user_id=user_id,
            company_id=company_id,
            roles=roles,
            permissions=permissions
        )
        
        refresh_token = self.jwt_manager.create_refresh_token(
            user_id=user_id,
            company_id=company_id
        )
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    
    def refresh_access_token(
        self,
        refresh_token: str,
        user_id: str,
        company_id: str,
        roles: list,
        permissions: list
    ) -> Optional[str]:
        """Refresh access token using refresh token"""
        payload = self.jwt_manager.verify_token(refresh_token)
        
        if not payload or payload.type != "refresh":
            return None
        
        if payload.sub != user_id or payload.company_id != company_id:
            return None
        
        new_access_token = self.jwt_manager.create_access_token(
            user_id=user_id,
            company_id=company_id,
            roles=roles,
            permissions=permissions
        )
        
        return new_access_token
    
    def setup_mfa(
        self,
        user_email: str
    ) -> MFASetup:
        """Setup MFA for user"""
        secret = self.mfa_manager.generate_secret()
        qr_code_url = self.mfa_manager.generate_qr_code(secret, user_email)
        backup_codes = self.mfa_manager.generate_backup_codes()
        
        return MFASetup(
            secret_key=secret,
            qr_code_url=qr_code_url,
            backup_codes=backup_codes
        )
    
    def verify_mfa_token(
        self,
        secret: str,
        token: str
    ) -> bool:
        """Verify MFA token"""
        return self.mfa_manager.verify_totp(secret, token)


# Global authentication service instance
auth_service = AuthenticationService()
