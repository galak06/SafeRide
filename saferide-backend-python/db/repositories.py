from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timedelta
from .database import get_db
from .db_models import (
    User, Role, Permission, DriverCompany, ServiceArea, UserLocation, 
    Ride, RoutePlan, RouteStop, AuditLog, UserRoleEnum, RideStatusEnum, 
    CompanyStatusEnum
)
from models.requests import (
    UserCreateRequest, UserUpdateRequest, CompanyCreateRequest, 
    CompanyUpdateRequest, ServiceAreaCreateRequest, UserLocationCreateRequest
)

class UserRepository:
    """Repository for user operations"""
    
    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_by_id(db: Session, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100, 
                search: Optional[str] = None, role_id: Optional[str] = None,
                is_active: Optional[bool] = None) -> List[User]:
        """Get all users with filtering"""
        query = db.query(User)
        
        if search:
            search_filter = or_(
                User.first_name.ilike(f"%{search}%"),
                User.last_name.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        if role_id:
            query = query.join(User.roles).filter(Role.id == role_id)
        
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def create(db: Session, user_data: UserCreateRequest, hashed_password: str) -> User:
        """Create new user"""
        user = User(
            id=str(uuid.uuid4()),
            email=user_data.email,
            hashed_password=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            phone=user_data.phone
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def update(db: Session, user_id: str, user_data: UserUpdateRequest) -> Optional[User]:
        """Update user"""
        user = UserRepository.get_by_id(db, user_id)
        if not user:
            return None
        
        update_data = user_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def delete(db: Session, user_id: str) -> bool:
        """Delete user"""
        user = UserRepository.get_by_id(db, user_id)
        if not user:
            return False
        
        db.delete(user)
        db.commit()
        return True
    
    @staticmethod
    def update_last_login(db: Session, user_id: str) -> None:
        """Update user's last login time"""
        user = UserRepository.get_by_id(db, user_id)
        if user:
            setattr(user, 'last_login', datetime.utcnow())
            db.commit()
    
    @staticmethod
    def update_status(db: Session, user_id: str, is_active: bool) -> Optional[User]:
        """Update user active status"""
        user = UserRepository.get_by_id(db, user_id)
        if not user:
            return None
        
        setattr(user, 'is_active', is_active)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def update_role(db: Session, user_id: str, role_id: str) -> Optional[User]:
        """Update user role"""
        user = UserRepository.get_by_id(db, user_id)
        if not user:
            return None
        
        # Get the new role
        role = RoleRepository.get_by_id(db, role_id)
        if not role:
            return None
        
        # Clear existing roles and assign new one
        user.roles = [role]
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def count_all(db: Session) -> int:
        """Count total number of users"""
        return db.query(User).count()
    
    @staticmethod
    def count_active(db: Session) -> int:
        """Count number of active users"""
        return db.query(User).filter(User.is_active == True).count()
    
    @staticmethod
    def get_recent(db: Session, limit: int = 5) -> List[User]:
        """Get recent users"""
        return db.query(User).order_by(desc(User.created_at)).limit(limit).all()

class RoleRepository:
    """Repository for role operations"""
    
    @staticmethod
    def get_by_id(db: Session, role_id: str) -> Optional[Role]:
        """Get role by ID"""
        return db.query(Role).filter(Role.id == role_id).first()
    
    @staticmethod
    def get_by_name(db: Session, name: str) -> Optional[Role]:
        """Get role by name"""
        return db.query(Role).filter(Role.name == name).first()
    
    @staticmethod
    def get_all(db: Session) -> List[Role]:
        """Get all roles"""
        return db.query(Role).all()
    
    @staticmethod
    def create(db: Session, name: str, description: Optional[str] = None) -> Role:
        """Create new role"""
        role = Role(
            id=str(uuid.uuid4()),
            name=name,
            description=description
        )
        db.add(role)
        db.commit()
        db.refresh(role)
        return role

class PermissionRepository:
    """Repository for permission operations"""
    
    @staticmethod
    def get_by_id(db: Session, permission_id: str) -> Optional[Permission]:
        """Get permission by ID"""
        return db.query(Permission).filter(Permission.id == permission_id).first()
    
    @staticmethod
    def get_all(db: Session) -> List[Permission]:
        """Get all permissions"""
        return db.query(Permission).all()
    
    @staticmethod
    def create(db: Session, permission_id: str, name: str, description: str, 
               resource: str, action: str) -> Permission:
        """Create new permission"""
        permission = Permission(
            id=permission_id,
            name=name,
            description=description,
            resource=resource,
            action=action
        )
        db.add(permission)
        db.commit()
        db.refresh(permission)
        return permission

class CompanyRepository:
    """Repository for company operations"""
    
    @staticmethod
    def get_by_id(db: Session, company_id: str) -> Optional[DriverCompany]:
        """Get company by ID"""
        return db.query(DriverCompany).filter(DriverCompany.id == company_id).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100,
                search: Optional[str] = None, is_active: Optional[bool] = None) -> List[DriverCompany]:
        """Get all companies with filtering"""
        query = db.query(DriverCompany)
        
        if search:
            search_filter = or_(
                DriverCompany.name.ilike(f"%{search}%"),
                DriverCompany.email.ilike(f"%{search}%"),
                DriverCompany.city.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        if is_active is not None:
            status_filter = CompanyStatusEnum.ACTIVE if is_active else CompanyStatusEnum.INACTIVE
            query = query.filter(DriverCompany.status == status_filter)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def create(db: Session, company_data: CompanyCreateRequest) -> DriverCompany:
        """Create new company"""
        company = DriverCompany(
            id=str(uuid.uuid4()),
            name=company_data.name,
            email=company_data.email,
            phone=company_data.phone,
            address=company_data.address,
            city=company_data.city,
            state=company_data.state,
            zip_code=company_data.zip_code,
            country=company_data.country
        )
        db.add(company)
        db.commit()
        db.refresh(company)
        return company
    
    @staticmethod
    def update(db: Session, company_id: str, company_data: CompanyUpdateRequest) -> Optional[DriverCompany]:
        """Update company"""
        company = CompanyRepository.get_by_id(db, company_id)
        if not company:
            return None
        
        update_data = company_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(company, field, value)
        
        db.commit()
        db.refresh(company)
        return company
    
    @staticmethod
    def count_all(db: Session) -> int:
        """Count total number of companies"""
        return db.query(DriverCompany).count()
    
    @staticmethod
    def get_recent(db: Session, limit: int = 5) -> List[DriverCompany]:
        """Get recent companies"""
        return db.query(DriverCompany).order_by(desc(DriverCompany.created_at)).limit(limit).all()

class ServiceAreaRepository:
    """Repository for service area operations"""
    
    @staticmethod
    def get_by_company(db: Session, company_id: str) -> List[ServiceArea]:
        """Get service areas by company"""
        return db.query(ServiceArea).filter(ServiceArea.company_id == company_id).all()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[ServiceArea]:
        """Get all service areas with pagination"""
        return db.query(ServiceArea).offset(skip).limit(limit).all()
    
    @staticmethod
    def create(db: Session, area_data: ServiceAreaCreateRequest) -> ServiceArea:
        """Create new service area"""
        area = ServiceArea(
            id=str(uuid.uuid4()),
            company_id=area_data.company_id,
            name=area_data.name,
            description=area_data.description,
            center_lat=area_data.center_lat,
            center_lng=area_data.center_lng,
            radius_km=area_data.radius_km
        )
        db.add(area)
        db.commit()
        db.refresh(area)
        return area
    
    @staticmethod
    def count_all(db: Session) -> int:
        """Count total number of service areas"""
        return db.query(ServiceArea).count()

class UserLocationRepository:
    """Repository for user location operations"""
    
    @staticmethod
    def get_by_user(db: Session, user_id: str, skip: int = 0, limit: int = 100) -> List[UserLocation]:
        """Get user locations by user ID"""
        return db.query(UserLocation).filter(
            UserLocation.user_id == user_id
        ).order_by(desc(UserLocation.timestamp)).offset(skip).limit(limit).all()
    
    @staticmethod
    def create(db: Session, location_data: UserLocationCreateRequest) -> UserLocation:
        """Create new user location"""
        location = UserLocation(
            id=str(uuid.uuid4()),
            user_id=location_data.user_id,
            lat=location_data.lat,
            lng=location_data.lng,
            address=location_data.address,
            accuracy=location_data.accuracy
        )
        db.add(location)
        db.commit()
        db.refresh(location)
        return location

class RideRepository:
    """Repository for ride operations"""
    
    @staticmethod
    def get_by_id(db: Session, ride_id: str) -> Optional[Ride]:
        """Get ride by ID"""
        return db.query(Ride).filter(Ride.id == ride_id).first()
    
    @staticmethod
    def get_by_user(db: Session, user_id: str, skip: int = 0, limit: int = 100) -> List[Ride]:
        """Get rides by user (as passenger or driver)"""
        return db.query(Ride).filter(
            or_(Ride.passenger_id == user_id, Ride.driver_id == user_id)
        ).order_by(desc(Ride.created_at)).offset(skip).limit(limit).all()
    
    @staticmethod
    def create(db: Session, passenger_id: str, origin_lat: float, origin_lng: float,
               destination_lat: float, destination_lng: float, origin_address: str,
               destination_address: str, passenger_count: int = 1) -> Ride:
        """Create new ride"""
        ride = Ride(
            id=str(uuid.uuid4()),
            passenger_id=passenger_id,
            origin_lat=origin_lat,
            origin_lng=origin_lng,
            origin_address=origin_address,
            destination_lat=destination_lat,
            destination_lng=destination_lng,
            destination_address=destination_address,
            passenger_count=passenger_count
        )
        db.add(ride)
        db.commit()
        db.refresh(ride)
        return ride
    
    @staticmethod
    def update_status(db: Session, ride_id: str, status: RideStatusEnum) -> Optional[Ride]:
        """Update ride status"""
        ride = RideRepository.get_by_id(db, ride_id)
        if not ride:
            return None
        
        setattr(ride, 'status', status)
        if status == RideStatusEnum.ACTIVE:
            setattr(ride, 'pickup_time', datetime.utcnow())
        elif status == RideStatusEnum.COMPLETED:
            setattr(ride, 'completion_time', datetime.utcnow())
        
        db.commit()
        db.refresh(ride)
        return ride

class AuditLogRepository:
    """Repository for audit log operations"""
    
    @staticmethod
    def create(db: Session, user_id: str, action: str, resource: str,
               resource_id: Optional[str] = None, details: Optional[str] = None,
               ip_address: str = "127.0.0.1", user_agent: str = "Unknown") -> AuditLog:
        """Create new audit log entry"""
        log = AuditLog(
            id=str(uuid.uuid4()),
            user_id=user_id,
            action=action,
            resource=resource,
            resource_id=resource_id,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100,
                user_id: Optional[str] = None, action: Optional[str] = None,
                resource: Optional[str] = None) -> List[AuditLog]:
        """Get audit logs with filtering"""
        query = db.query(AuditLog)
        
        if user_id:
            query = query.filter(AuditLog.user_id == user_id)
        if action:
            query = query.filter(AuditLog.action == action)
        if resource:
            query = query.filter(AuditLog.resource == resource)
        
        return query.order_by(desc(AuditLog.timestamp)).offset(skip).limit(limit).all() 