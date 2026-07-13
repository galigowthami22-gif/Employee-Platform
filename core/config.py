"""
PHASE 5-6: CONFIGURATION FRAMEWORK
Configuration management system for multiple environments, secrets, and feature flags.
"""

import os
import yaml
from typing import Any, Dict, Optional
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Environment:
    """Environment type enumeration"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class Settings(BaseSettings):
    """Main configuration settings with environment support"""
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = ENVIRONMENT == "development"
    
    # Application
    APP_NAME: str = "Stackly ERP"
    APP_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Server
    SERVER_HOST: str = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", "8000"))
    WORKERS: int = int(os.getenv("WORKERS", "4"))
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:password@localhost:3306/stackly_erp"
    )
    DATABASE_ECHO: bool = False
    DATABASE_POOL_SIZE: int = int(os.getenv("DATABASE_POOL_SIZE", "20"))
    DATABASE_MAX_OVERFLOW: int = int(os.getenv("DATABASE_MAX_OVERFLOW", "10"))
    
    # Cache
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "3600"))
    CACHE_ENABLED: bool = True
    
    # Elasticsearch
    ELASTICSEARCH_URL: str = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
    ELASTICSEARCH_ENABLED: bool = False
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Security
    BCRYPT_LOG_ROUNDS: int = 12
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8080"]
    ALLOWED_HOSTS: list = ["localhost", "127.0.0.1"]
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW_SECONDS: int = 60
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "json"
    LOG_FILE_PATH: str = "logs/stackly.log"
    
    # Email
    MAIL_SERVER: str = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT: int = int(os.getenv("MAIL_PORT", "587"))
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD", "")
    MAIL_FROM: str = os.getenv("MAIL_FROM", "noreply@stackly.com")
    MAIL_FROM_NAME: str = os.getenv("MAIL_FROM_NAME", "Stackly ERP")
    
    # SMS
    SMS_PROVIDER: str = os.getenv("SMS_PROVIDER", "twilio")
    TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_FROM_NUMBER: str = os.getenv("TWILIO_FROM_NUMBER", "")
    
    # Payment Gateway
    STRIPE_API_KEY: str = os.getenv("STRIPE_API_KEY", "")
    STRIPE_WEBHOOK_SECRET: str = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    
    # File Storage
    FILE_UPLOAD_DIR: str = os.getenv("FILE_UPLOAD_DIR", "uploads")
    MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS: list = ["pdf", "doc", "docx", "xls", "xlsx", "jpg", "png", "zip"]
    
    # Feature Flags
    FEATURES: Dict[str, bool] = {
        "mfa_enabled": True,
        "payroll_automation": True,
        "advanced_analytics": False,
        "multi_currency": False,
        "mobile_app_sync": False,
        "audit_trails": True,
        "workflow_automation": True,
        "bulk_operations": True,
    }
    
    # Multi-tenancy
    ENABLE_MULTI_TENANCY: bool = True
    TENANT_ISOLATION_MODE: str = "row_level"  # row_level or schema_level
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # API Documentation
    OPENAPI_URL: str = "/openapi.json"
    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


class ConfigLoader:
    """Load configuration from YAML files"""
    
    CONFIG_DIR = Path(__file__).parent.parent / "config"
    
    @classmethod
    def load_config(cls, env: str = None) -> Dict[str, Any]:
        """Load configuration for specified environment"""
        if env is None:
            env = os.getenv("ENVIRONMENT", "development")
        
        config = {}
        
        # Load default config if exists
        default_config_path = cls.CONFIG_DIR / "default.yaml"
        if default_config_path.exists():
            try:
                with open(default_config_path, "r") as f:
                    config = yaml.safe_load(f) or {}
            except Exception as e:
                print(f"Error loading default config: {e}")
        
        # Load environment-specific config if exists
        env_config_path = cls.CONFIG_DIR / f"{env}.yaml"
        if env_config_path.exists():
            try:
                with open(env_config_path, "r") as f:
                    env_config = yaml.safe_load(f)
                    if env_config:
                        config.update(env_config)
            except Exception as e:
                print(f"Error loading {env} config: {e}")
        
        return config
    
    @classmethod
    def load_feature_flags(cls) -> Dict[str, bool]:
        """Load feature flags from configuration"""
        config = cls.load_config()
        return config.get("features", {})
    
    @classmethod
    def get_feature_flag(cls, flag_name: str) -> bool:
        """Get specific feature flag value"""
        flags = cls.load_feature_flags()
        return flags.get(flag_name, False)


class FeatureManager:
    """Manage feature flags with runtime support"""
    
    def __init__(self):
        self.flags = ConfigLoader.load_feature_flags()
    
    def is_enabled(self, feature_name: str) -> bool:
        """Check if feature is enabled"""
        return self.flags.get(feature_name, False)
    
    def enable_feature(self, feature_name: str):
        """Enable a feature"""
        self.flags[feature_name] = True
    
    def disable_feature(self, feature_name: str):
        """Disable a feature"""
        self.flags[feature_name] = False
    
    def get_all_flags(self) -> Dict[str, bool]:
        """Get all feature flags"""
        return self.flags.copy()


# Global instances
settings = get_settings()
feature_manager = FeatureManager()
config_loader = ConfigLoader()