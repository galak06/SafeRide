from pydantic import BaseModel, Field
from typing import Optional

class PaginationParams(BaseModel):
    page: int = Field(1, ge=1, description="Page number")
    size: int = Field(10, ge=1, le=100, description="Page size")
    sort_by: Optional[str] = Field(None, description="Sort field")
    sort_order: str = Field("desc", pattern="^(asc|desc)$", description="Sort order") 