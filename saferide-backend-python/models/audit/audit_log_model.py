from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class AuditLogModel(BaseModel):
    id: str
    user_id: str
    action: str
    resource: str
    resource_id: Optional[str]
    details: Dict[str, Any]
    ip_address: str
    user_agent: str
    created_at: datetime = Field(default_factory=datetime.now) 