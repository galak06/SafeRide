from pydantic import BaseModel
from typing import List

class RoleCreateRequest(BaseModel):
    name: str
    description: str
    permissions: List[str] 