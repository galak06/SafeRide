from pydantic import BaseModel, Field
from typing import List, Dict, Any
from .route_plan import RoutePlan

class RouteOptimizationResponse(BaseModel):
    route_plan: RoutePlan
    optimization_metrics: Dict[str, Any] = Field(..., description="Optimization metrics")
    alternative_routes: List[RoutePlan] = Field(..., description="Alternative route options") 