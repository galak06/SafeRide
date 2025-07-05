from pydantic import BaseModel
from typing import Dict

class UserStats(BaseModel):
    total_users: int
    active_users: int
    new_users_today: int
    new_users_this_week: int
    new_users_this_month: int
    users_by_role: Dict[str, int] 