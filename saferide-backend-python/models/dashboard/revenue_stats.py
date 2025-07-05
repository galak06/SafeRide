from pydantic import BaseModel
from typing import Dict

class RevenueStats(BaseModel):
    total_revenue: float
    revenue_today: float
    revenue_this_week: float
    revenue_this_month: float
    average_revenue_per_ride: float
    revenue_by_month: Dict[str, float] 