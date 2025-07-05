from pydantic import BaseModel, Field

class PermissionModel(BaseModel):
    id: str = Field(..., description="Permission ID")
    name: str = Field(..., description="Permission name")
    description: str = Field(..., description="Permission description")
    resource: str = Field(..., description="Resource this permission applies to")
    action: str = Field(..., description="Action allowed (read, write, delete, etc.)") 