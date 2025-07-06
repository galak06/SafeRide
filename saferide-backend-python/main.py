from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import httpx
import os
import json
import asyncio
from datetime import datetime, timedelta
from dotenv import load_dotenv
import random
import time
import logging
from sqlalchemy.orm import Session

# Configure logging
logger = logging.getLogger(__name__)

# Import the auth router
from routes.auth import router as auth_router
# Import the users router
from routes.users import router as users_router
# Import the relationships router
from routes.relationships import router as relationships_router
# Import the children router
from routes.children import router as children_router
# Import the companies router
from routes.companies import router as companies_router

# Import services
from services.admin_service import AdminService
from services.child_service import ChildService

# Import custom exceptions and global handler
from core.exceptions import global_exception_handler, SafeRideException, AuthenticationError, NotFoundError, DatabaseError

# Import security middleware
from core.middleware import (
    SecurityMiddleware, RateLimitMiddleware, SecurityHeadersMiddleware,
    InputValidationMiddleware, brute_force_protection
)

# Import database dependency
from db import get_db
from db.repositories import UserRepository, CompanyRepository

# Import settings
from core.config import settings

# Load environment variables
load_dotenv()

app = FastAPI(
    title="SafeRide API",
    description="Backend API for SafeRide ride-sharing application with Waze integration",
    version="1.0.0"
)

# Register global exception handler
app.add_exception_handler(Exception, global_exception_handler)

# Register specific handlers for SafeRide exceptions
app.add_exception_handler(SafeRideException, global_exception_handler)
app.add_exception_handler(AuthenticationError, global_exception_handler)
app.add_exception_handler(NotFoundError, global_exception_handler)
app.add_exception_handler(DatabaseError, global_exception_handler)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

# Security middleware
@app.middleware("http")
async def security_middleware(request: Request, call_next):
    """Security middleware for input validation and brute force protection"""
    try:
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"
        
        # Check if IP is locked due to brute force attempts
        if brute_force_protection.is_ip_locked(client_ip):
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "error": {
                        "message": "Too many failed attempts. Please try again later.",
                        "code": "BRUTE_FORCE_LOCKOUT",
                        "retry_after": 300
                    }
                }
            )
        
        # Validate request
        await InputValidationMiddleware.validate_request(request)
        
        # Process request
        response = await call_next(request)
        
        # Add security headers
        response = SecurityHeadersMiddleware.add_security_headers(response)
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Security middleware error: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "message": "Internal server error",
                    "code": "INTERNAL_ERROR"
                }
            }
        )

# Include the auth router
app.include_router(auth_router)
# Include the users router
app.include_router(users_router)
# Include the relationships router
app.include_router(relationships_router)
# Include the children router
app.include_router(children_router)
# Include the companies router
app.include_router(companies_router)

# Security
security = HTTPBearer()

# Pydantic models for type safety (similar to TypeScript interfaces)
class Location(BaseModel):
    lat: float = Field(..., description="Latitude")
    lng: float = Field(..., description="Longitude")
    address: Optional[str] = Field(None, description="Human readable address")

class RouteRequest(BaseModel):
    origin: Location = Field(..., description="Starting location")
    destination: Location = Field(..., description="Destination location")
    mode: str = Field("driving", description="Transport mode: driving, walking, transit")

class RouteResponse(BaseModel):
    distance: float = Field(..., description="Distance in kilometers")
    duration: int = Field(..., description="Duration in seconds")
    traffic_delay: int = Field(0, description="Traffic delay in seconds")
    route_points: List[Location] = Field(..., description="Route waypoints")
    eta: datetime = Field(..., description="Estimated arrival time")

class TrafficAlert(BaseModel):
    id: str = Field(..., description="Alert ID")
    type: str = Field(..., description="Alert type: accident, construction, police, etc.")
    severity: str = Field(..., description="Severity: low, medium, high")
    location: Location = Field(..., description="Alert location")
    description: str = Field(..., description="Alert description")
    created_at: datetime = Field(..., description="Alert creation time")

class RideRequest(BaseModel):
    user_id: str = Field(..., description="User ID")
    origin: Location = Field(..., description="Pickup location")
    destination: Location = Field(..., description="Drop-off location")
    passenger_count: int = Field(1, ge=1, le=4, description="Number of passengers")

class RideResponse(BaseModel):
    ride_id: str = Field(..., description="Unique ride ID")
    status: str = Field(..., description="Ride status: pending, confirmed, active, completed")
    driver_info: Optional[Dict[str, Any]] = Field(None, description="Driver information")
    estimated_pickup: datetime = Field(..., description="Estimated pickup time")
    estimated_arrival: datetime = Field(..., description="Estimated arrival time")
    fare_estimate: float = Field(..., description="Estimated fare in USD")

class UserAuth(BaseModel):
    email: str = Field(..., description="User email")
    password: str = Field(..., description="User password")

class AuthResponse(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("bearer", description="Token type")
    user_id: str = Field(..., description="User ID")
    expires_in: int = Field(3600, description="Token expiration in seconds")

# Mock Waze Service (simulates Waze API)
class MockWazeService:
    def __init__(self):
        self.api_key = os.getenv("WAZE_API_KEY", "mock_key")
        self.base_url = "https://api.waze.com"
    
    async def get_route(self, origin: Location, destination: Location, mode: str = "driving") -> RouteResponse:
        """Mock Waze route calculation"""
        # Simulate API delay
        await asyncio.sleep(0.5)
        
        # Calculate mock distance and duration
        distance = self._calculate_distance(origin, destination)
        base_duration = int(distance * 120)  # 2 minutes per km
        traffic_delay = random.randint(0, int(base_duration * 0.3))  # 0-30% traffic delay
        
        # Generate mock route points
        route_points = self._generate_route_points(origin, destination)
        
        # Calculate ETA
        eta = datetime.now() + timedelta(seconds=base_duration + traffic_delay)
        
        return RouteResponse(
            distance=distance,
            duration=base_duration + traffic_delay,
            traffic_delay=traffic_delay,
            route_points=route_points,
            eta=eta
        )
    
    async def get_traffic_alerts(self, area: str) -> List[TrafficAlert]:
        """Mock Waze traffic alerts"""
        await asyncio.sleep(0.3)
        
        alert_types = ["accident", "construction", "police", "hazard", "weather"]
        severities = ["low", "medium", "high"]
        
        alerts = []
        for i in range(random.randint(2, 8)):
            alert = TrafficAlert(
                id=f"alert_{i}",
                type=random.choice(alert_types),
                severity=random.choice(severities),
                location=Location(
                    lat=40.7128 + random.uniform(-0.1, 0.1),
                    lng=-74.0060 + random.uniform(-0.1, 0.1),
                    address=f"Alert location {i}"
                ),
                description=f"Mock {random.choice(alert_types)} alert",
                created_at=datetime.now() - timedelta(minutes=random.randint(5, 60))
            )
            alerts.append(alert)
        
        return alerts
    
    def _calculate_distance(self, origin: Location, destination: Location) -> float:
        """Calculate distance between two points (Haversine formula)"""
        import math
        
        lat1, lon1 = math.radians(origin.lat), math.radians(origin.lng)
        lat2, lon2 = math.radians(destination.lat), math.radians(destination.lng)
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        return 6371 * c  # Earth radius in km
    
    def _generate_route_points(self, origin: Location, destination: Location) -> List[Location]:
        """Generate mock route waypoints"""
        points = [origin]
        
        # Generate 3-8 intermediate points
        num_points = random.randint(3, 8)
        for i in range(num_points):
            # Interpolate between origin and destination
            ratio = (i + 1) / (num_points + 1)
            lat = origin.lat + (destination.lat - origin.lat) * ratio
            lng = origin.lng + (destination.lng - origin.lng) * ratio
            
            # Add some randomness
            lat += random.uniform(-0.01, 0.01)
            lng += random.uniform(-0.01, 0.01)
            
            points.append(Location(lat=lat, lng=lng, address=None))
        
        points.append(destination)
        return points

# Mock Ride Service
class MockRideService:
    def __init__(self):
        self.rides: Dict[str, Dict] = {}
        self.drivers = [
            {"id": "driver_1", "name": "John Smith", "rating": 4.8, "car": "Toyota Camry"},
            {"id": "driver_2", "name": "Sarah Johnson", "rating": 4.9, "car": "Honda Civic"},
            {"id": "driver_3", "name": "Mike Davis", "rating": 4.7, "car": "Ford Focus"}
        ]
    
    async def create_ride(self, ride_request: RideRequest) -> RideResponse:
        """Create a new ride request"""
        ride_id = f"ride_{len(self.rides) + 1}"
        
        # Calculate mock estimates
        distance = self._calculate_distance(ride_request.origin, ride_request.destination)
        estimated_duration = int(distance * 120)  # 2 minutes per km
        fare_estimate = distance * 2.5  # $2.50 per km
        
        # Assign random driver
        driver = random.choice(self.drivers)
        
        ride_data = {
            "ride_id": ride_id,
            "status": "pending",
            "driver_info": driver,
            "estimated_pickup": datetime.now() + timedelta(minutes=random.randint(5, 15)),
            "estimated_arrival": datetime.now() + timedelta(minutes=estimated_duration),
            "fare_estimate": fare_estimate
        }
        
        self.rides[ride_id] = ride_data
        return RideResponse(**ride_data)
    
    async def confirm_ride(self, ride_id: str) -> RideResponse:
        """Confirm a ride request"""
        if ride_id not in self.rides:
            raise HTTPException(status_code=404, detail="Ride not found")
        
        self.rides[ride_id]["status"] = "confirmed"
        return RideResponse(**self.rides[ride_id])
    
    async def get_ride_status(self, ride_id: str) -> Dict[str, Any]:
        """Get ride status"""
        if ride_id not in self.rides:
            raise HTTPException(status_code=404, detail="Ride not found")
        
        return self.rides[ride_id]
    
    def _calculate_distance(self, origin: Location, destination: Location) -> float:
        """Calculate distance between two points"""
        import math
        
        lat1, lon1 = math.radians(origin.lat), math.radians(origin.lng)
        lat2, lon2 = math.radians(destination.lat), math.radians(destination.lng)
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        return 6371 * c  # Earth radius in km

# Mock services
waze_service = MockWazeService()
ride_service = MockRideService()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Get current user from JWT token"""
    # Note: This is a simplified implementation
    # In production, you would validate the JWT token and extract user info
    return "user_123"

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "SafeRide API is running!",
        "version": "1.0.0",
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/route", response_model=RouteResponse)
async def calculate_route(route_request: RouteRequest):
    """Calculate route between two points"""
    return await waze_service.get_route(route_request.origin, route_request.destination, route_request.mode)

@app.get("/api/traffic/{area}", response_model=List[TrafficAlert])
async def get_traffic_alerts(area: str):
    """Get traffic alerts for a specific area"""
    return await waze_service.get_traffic_alerts(area)

@app.post("/api/rides", response_model=RideResponse)
async def create_ride(ride_request: RideRequest, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    """Create a new ride request"""
    return await ride_service.create_ride(ride_request)

@app.post("/api/rides/{ride_id}/confirm", response_model=RideResponse)
async def confirm_ride(ride_id: str, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    """Confirm a ride request"""
    return await ride_service.confirm_ride(ride_id)

@app.get("/api/rides/{ride_id}")
async def get_ride_status(ride_id: str, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get ride status"""
    return await ride_service.get_ride_status(ride_id)

@app.get("/api/admin/dashboard/metrics")
async def get_dashboard_metrics(db: Session = Depends(get_db)):
    """Get dashboard metrics for admin portal"""
    try:
        # Get user statistics
        total_users = UserRepository.count_all(db)
        active_users = UserRepository.count_active(db)
        
        # Get driver statistics
        drivers = UserRepository.get_drivers(db)
        total_drivers = len(drivers)
        active_drivers = len([d for d in drivers if getattr(d, 'is_active', False)])
        
        # Get company statistics
        total_companies = CompanyRepository.count_all(db)
        active_companies = CompanyRepository.count_active(db)
        
        # Get children statistics
        child_service = ChildService(db)
        all_children = child_service.get_all_children()
        total_children = len(all_children)
        
        # Mock ride statistics (since we don't have a ride system yet)
        active_rides = 0  # This would come from a ride service
        
        return {
            "total_users": total_users,
            "active_users": active_users,
            "total_drivers": total_drivers,
            "active_drivers": active_drivers,
            "total_companies": total_companies,
            "active_companies": active_companies,
            "total_children": total_children,
            "active_rides": active_rides,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get dashboard metrics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get dashboard metrics: {str(e)}"
        )

@app.get("/api/health")
async def health_check():
    """Detailed health check endpoint with security status"""
    from db.database import check_database_health
    
    # Check database health
    db_health = check_database_health()
    
    # Get security status
    security_status = {
        "rate_limiting": "enabled",
        "brute_force_protection": "enabled",
        "input_validation": "enabled",
        "security_headers": "enabled",
        "ssl_enforced": settings.debug == False,  # SSL in production
        "secret_management": "configured" if len(settings.secret_key) >= 32 else "weak"
    }
    
    # Overall health status
    overall_status = "healthy"
    if db_health["status"] != "healthy":
        overall_status = "degraded"
    if security_status["secret_management"] == "weak":
        overall_status = "warning"
    
    return {
        "status": overall_status,
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "services": {
            "database": db_health,
            "authentication": "active",
            "waze_api": "available"
        },
        "security": security_status,
        "uptime": "running",  # In production, calculate actual uptime
        "environment": "development" if settings.debug else "production"
    }

# Import logger
import logging
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 