from typing import Dict, Any, List, Optional
import logging
from datetime import datetime, timedelta
import uuid
from sqlalchemy.orm import Session

from db.db_models import RideStatusEnum
from models.requests import RideRequest
from models.responses import RideResponse
from core.exceptions import NotFoundError, DatabaseError, ValidationError

logger = logging.getLogger(__name__)

class RideService:
    """Service for managing ride operations with mock data persistence"""
    
    def __init__(self, db: Session):
        self.db = db
        # Mock ride storage for development
        self._rides = {}
    
    async def create_ride(self, ride_request: RideRequest) -> RideResponse:
        """
        Create a new ride
        
        Args:
            ride_request: Ride request data
            
        Returns:
            RideResponse with created ride information
            
        Raises:
            ValidationError: If ride data is invalid
            DatabaseError: If database operation fails
        """
        try:
            # Validate ride request
            if not ride_request.origin or not ride_request.destination:
                raise ValidationError("Origin and destination are required")
            
            if ride_request.passenger_count < 1 or ride_request.passenger_count > 4:
                raise ValidationError("Passenger count must be between 1 and 4")
            
            # Create mock ride
            ride_id = str(uuid.uuid4())
            self._rides[ride_id] = {
                "id": ride_id,
                "passenger_id": ride_request.user_id,
                "origin_lat": ride_request.origin.lat,
                "origin_lng": ride_request.origin.lng,
                "destination_lat": ride_request.destination.lat,
                "destination_lng": ride_request.destination.lng,
                "origin_address": ride_request.origin.address or "",
                "destination_address": ride_request.destination.address or "",
                "passenger_count": ride_request.passenger_count,
                "status": RideStatusEnum.PENDING,
                "created_at": datetime.utcnow()
            }
            
            logger.info(f"Ride created: {ride_id}")
            
            # Convert to response model
            return RideResponse(
                ride_id=ride_id,
                status=RideStatusEnum.PENDING.value,
                driver_info=None,  # Will be populated when driver is assigned
                estimated_pickup=datetime.now() + timedelta(minutes=5),  # Mock for now
                estimated_arrival=datetime.now() + timedelta(minutes=20),  # Mock for now
                fare_estimate=10.0  # Mock for now
            )
            
        except (ValidationError, DatabaseError):
            raise
        except Exception as e:
            logger.error(f"Error creating ride: {e}")
            raise DatabaseError(f"Failed to create ride: {str(e)}")
    
    async def get_ride(self, ride_id: str) -> RideResponse:
        """
        Get ride by ID
        
        Args:
            ride_id: Unique ride identifier
            
        Returns:
            RideResponse with ride information
            
        Raises:
            NotFoundError: If ride not found
            DatabaseError: If database operation fails
        """
        try:
            ride = self._rides.get(ride_id)
            if not ride:
                raise NotFoundError(f"Ride {ride_id} not found")
            
            return RideResponse(
                ride_id=ride["id"],
                status=ride["status"].value,
                driver_info=None,  # Will be populated when driver is assigned
                estimated_pickup=datetime.now() + timedelta(minutes=5),
                estimated_arrival=datetime.now() + timedelta(minutes=20),
                fare_estimate=10.0  # Mock for now
            )
            
        except (NotFoundError, DatabaseError):
            raise
        except Exception as e:
            logger.error(f"Error getting ride {ride_id}: {e}")
            raise DatabaseError(f"Failed to get ride: {str(e)}")
    
    async def update_ride_status(self, ride_id: str, status: str) -> RideResponse:
        """
        Update ride status
        
        Args:
            ride_id: Unique ride identifier
            status: New status (pending, accepted, in_progress, completed, cancelled)
            
        Returns:
            RideResponse with updated ride information
            
        Raises:
            NotFoundError: If ride not found
            ValidationError: If status is invalid
            DatabaseError: If database operation fails
        """
        try:
            # Validate status
            try:
                status_enum = RideStatusEnum(status)
            except ValueError:
                raise ValidationError(f"Invalid status: {status}")
            
            # Update ride status
            ride = self._rides.get(ride_id)
            if not ride:
                raise NotFoundError(f"Ride {ride_id} not found")
            
            ride["status"] = status_enum
            logger.info(f"Ride {ride_id} status updated to {status}")
            
            return RideResponse(
                ride_id=ride["id"],
                status=ride["status"].value,
                driver_info=None,  # Will be populated when driver is assigned
                estimated_pickup=datetime.now() + timedelta(minutes=5),
                estimated_arrival=datetime.now() + timedelta(minutes=20),
                fare_estimate=10.0  # Mock for now
            )
            
        except (NotFoundError, ValidationError, DatabaseError):
            raise
        except Exception as e:
            logger.error(f"Error updating ride status: {e}")
            raise DatabaseError(f"Failed to update ride status: {str(e)}")
    
    async def assign_driver(self, ride_id: str, driver_id: str) -> RideResponse:
        """
        Assign a driver to a ride
        
        Args:
            ride_id: Unique ride identifier
            driver_id: Driver identifier
            
        Returns:
            RideResponse with updated ride information
            
        Raises:
            NotFoundError: If ride not found
            DatabaseError: If database operation fails
        """
        try:
            # For now, just update status to accepted
            # In a real implementation, you'd also update the driver_id field
            ride = self._rides.get(ride_id)
            if not ride:
                raise NotFoundError(f"Ride {ride_id} not found")
            
            ride["status"] = RideStatusEnum.ACTIVE
            logger.info(f"Driver {driver_id} assigned to ride {ride_id}")
            
            return RideResponse(
                ride_id=ride["id"],
                status=ride["status"].value,
                driver_info={"id": driver_id, "name": "Driver Name"},  # Mock for now
                estimated_pickup=datetime.now() + timedelta(minutes=5),
                estimated_arrival=datetime.now() + timedelta(minutes=20),
                fare_estimate=10.0  # Mock for now
            )
            
        except (NotFoundError, DatabaseError):
            raise
        except Exception as e:
            logger.error(f"Error assigning driver: {e}")
            raise DatabaseError(f"Failed to assign driver: {str(e)}")
    
    async def get_user_rides(self, user_id: str, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get rides for a specific user
        
        Args:
            user_id: User identifier
            status: Optional status filter
            
        Returns:
            List of ride dictionaries
            
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            user_rides = []
            for ride in self._rides.values():
                if ride["passenger_id"] == user_id:
                    if status is None or ride["status"].value == status:
                        user_rides.append({
                            "id": ride["id"],
                            "status": ride["status"].value,
                            "origin_address": ride["origin_address"],
                            "destination_address": ride["destination_address"],
                            "passenger_count": ride["passenger_count"],
                            "created_at": ride["created_at"].isoformat(),
                            "estimated_pickup": (datetime.now() + timedelta(minutes=5)).isoformat(),
                            "estimated_arrival": (datetime.now() + timedelta(minutes=20)).isoformat(),
                            "fare_estimate": 10.0
                        })
            
            return user_rides
            
        except Exception as e:
            logger.error(f"Error getting user rides: {e}")
            raise DatabaseError(f"Failed to get user rides: {str(e)}")
    
    async def cancel_ride(self, ride_id: str, reason: str = "") -> RideResponse:
        """
        Cancel a ride
        
        Args:
            ride_id: Unique ride identifier
            reason: Optional cancellation reason
            
        Returns:
            RideResponse with updated ride information
            
        Raises:
            NotFoundError: If ride not found
            DatabaseError: If database operation fails
        """
        try:
            ride = self._rides.get(ride_id)
            if not ride:
                raise NotFoundError(f"Ride {ride_id} not found")
            
            ride["status"] = RideStatusEnum.CANCELLED
            logger.info(f"Ride {ride_id} cancelled. Reason: {reason}")
            
            return RideResponse(
                ride_id=ride["id"],
                status=ride["status"].value,
                driver_info=None,
                estimated_pickup=datetime.now(),
                estimated_arrival=datetime.now(),
                fare_estimate=0.0
            )
            
        except (NotFoundError, DatabaseError):
            raise
        except Exception as e:
            logger.error(f"Error cancelling ride: {e}")
            raise DatabaseError(f"Failed to cancel ride: {str(e)}") 