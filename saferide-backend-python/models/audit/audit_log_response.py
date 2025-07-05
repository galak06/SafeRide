from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from ..responses.user_response import UserResponse

class AuditLogResponse(BaseModel):
    id: str
    user: UserResponse
    action: str
    resource: str
    resource_id: Optional[str]
    details: Dict[str, Any]
    ip_address: str
    user_agent: str
    created_at: datetime 