from pydantic import BaseModel
from .user_response import UserResponse

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 3600
    user: UserResponse 