from pydantic import BaseModel, Field
from .user_response import UserResponse

class LoginResponse(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field("bearer", description="Token type")
    expires_in: int = Field(3600, description="Access token expiration in seconds")
    refresh_expires_in: int = Field(604800, description="Refresh token expiration in seconds (7 days)")
    user: UserResponse = Field(..., description="User information")

class TokenRefreshResponse(BaseModel):
    access_token: str = Field(..., description="New JWT access token")
    token_type: str = Field("bearer", description="Token type")
    expires_in: int = Field(3600, description="Access token expiration in seconds") 