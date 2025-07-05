from pydantic import BaseModel

class PermissionCreateRequest(BaseModel):
    name: str
    description: str
    resource: str
    action: str 