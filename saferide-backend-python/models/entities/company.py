from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class OperationAreaType(str, Enum):
    CIRCLE = "circle"
    POLYGON = "polygon"

class Coordinate(BaseModel):
    lat: float = Field(..., ge=-90, le=90, description="Latitude")
    lng: float = Field(..., ge=-180, le=180, description="Longitude")

class CircleOperationArea(BaseModel):
    center: Coordinate = Field(..., description="Center point of the operation area")
    radius_km: float = Field(..., gt=0, description="Radius in kilometers")

class PolygonOperationArea(BaseModel):
    coordinates: List[Coordinate] = Field(..., description="List of coordinates forming the polygon")
    
    @field_validator('coordinates')
    @classmethod
    def validate_coordinates(cls, v):
        if len(v) < 3:
            raise ValueError('Polygon must have at least 3 coordinates')
        return v

class CompanyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Company name")
    description: Optional[str] = Field(None, description="Company description")
    contact_email: EmailStr = Field(..., description="Contact email")
    contact_phone: Optional[str] = Field(None, description="Contact phone number")
    address: Optional[str] = Field(None, description="Company address")
    is_active: bool = Field(True, description="Whether the company is active")

class CompanyCreate(CompanyBase):
    operation_area_type: OperationAreaType = Field(..., description="Type of operation area")
    # Circle area fields
    center_lat: Optional[float] = Field(None, ge=-90, le=90, description="Center latitude for circle")
    center_lng: Optional[float] = Field(None, ge=-180, le=180, description="Center longitude for circle")
    radius_km: Optional[float] = Field(None, gt=0, description="Radius in kilometers for circle")
    # Polygon area fields
    polygon_coordinates: Optional[List[Dict[str, float]]] = Field(None, description="Polygon coordinates as list of {lat, lng} objects")

class CompanyUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Company name")
    description: Optional[str] = Field(None, description="Company description")
    contact_email: Optional[EmailStr] = Field(None, description="Contact email")
    contact_phone: Optional[str] = Field(None, description="Contact phone number")
    address: Optional[str] = Field(None, description="Company address")
    is_active: Optional[bool] = Field(None, description="Whether the company is active")
    operation_area_type: Optional[OperationAreaType] = Field(None, description="Type of operation area")
    center_lat: Optional[float] = Field(None, ge=-90, le=90, description="Center latitude for circle")
    center_lng: Optional[float] = Field(None, ge=-180, le=180, description="Center longitude for circle")
    radius_km: Optional[float] = Field(None, gt=0, description="Radius in kilometers for circle")
    polygon_coordinates: Optional[List[Dict[str, float]]] = Field(None, description="Polygon coordinates as list of {lat, lng} objects")

class CompanyModel(CompanyBase):
    id: str = Field(..., description="Company ID")
    operation_area_type: OperationAreaType = Field(..., description="Type of operation area")
    center_lat: Optional[float] = Field(None, description="Center latitude for circle")
    center_lng: Optional[float] = Field(None, description="Center longitude for circle")
    radius_km: Optional[float] = Field(None, description="Radius in kilometers for circle")
    polygon_coordinates: Optional[List[Dict[str, float]]] = Field(None, description="Polygon coordinates")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    driver_count: int = Field(0, description="Number of drivers in the company")

    class Config:
        from_attributes = True 