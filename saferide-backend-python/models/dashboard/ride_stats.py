from pydantic import BaseModel

class RideStats(BaseModel):
    total_rides: int
    completed_rides: int
    cancelled_rides: int
    pending_rides: int
    rides_today: int
    rides_this_week: int
    rides_this_month: int
    average_ride_value: float 