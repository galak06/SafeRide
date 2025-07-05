from pydantic_settings import BaseSettings
from typing import List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Application
    app_name: str = "SafeRide API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Security - CRITICAL: These must be set via environment variables
    secret_key: str  # Required - Set SECRET_KEY environment variable
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Database - CRITICAL: These must be set via environment variables
    database_url: str  # Required - Set DATABASE_URL environment variable
    
    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]
    
    # Rate Limiting
    rate_limit_per_minute: int = 100
    rate_limit_per_hour: int = 1000
    
    # External APIs
    waze_api_key: Optional[str] = None
    google_maps_api_key: Optional[str] = None
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Frontend URL (for CORS or other integrations)
    frontend_url: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance - lazy initialization
_settings = None

def get_settings() -> Settings:
    """Get settings instance with lazy initialization"""
    global _settings
    if _settings is None:
        _settings = Settings()
        validate_settings(_settings)
    return _settings

def validate_settings(settings_instance: Settings):
    """Validate critical settings and provide helpful error messages"""
    missing_vars = []
    
    # Check for required environment variables
    if not settings_instance.secret_key or settings_instance.secret_key == "":
        missing_vars.append("SECRET_KEY")
    
    if not settings_instance.database_url or settings_instance.database_url == "":
        missing_vars.append("DATABASE_URL")
    
    if missing_vars:
        error_msg = f"""
🚨 CRITICAL SECURITY ERROR: Missing required environment variables!

The following environment variables must be set:
{', '.join(missing_vars)}

Please set these variables in your .env file or environment:

Example .env file:
SECRET_KEY=your-super-secret-key-at-least-32-characters-long
DATABASE_URL=postgresql://username:password@localhost:5432/database_name

For production, use a secure secret management service like:
- AWS Secrets Manager
- HashiCorp Vault
- Azure Key Vault
- Google Secret Manager

NEVER commit secrets to version control!
        """
        raise ValueError(error_msg)
    
    # Validate secret key strength
    if len(settings_instance.secret_key) < 32:
        print("⚠️  WARNING: SECRET_KEY should be at least 32 characters long for production security.")
    
    # Validate database URL format
    if not settings_instance.database_url.startswith(('postgresql://', 'postgres://')):
        print("⚠️  WARNING: DATABASE_URL should start with 'postgresql://' or 'postgres://'")

# Initialize settings
settings = get_settings() 