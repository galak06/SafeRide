from pydantic import BaseModel

class DashboardMetrics(BaseModel):
    total_users: int
    total_rides: int
    total_revenue: float
    active_drivers: int
    pending_rides: int
    completed_rides_today: int
    revenue_today: float
    total_companies: int
    active_service_areas: int 