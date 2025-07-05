from pydantic import BaseModel
from typing import Dict

class CompanyStats(BaseModel):
    total_companies: int
    active_companies: int
    total_drivers: int
    active_drivers: int
    total_service_areas: int
    active_service_areas: int
    companies_by_region: Dict[str, int] 