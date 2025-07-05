from typing import List, Dict, Any, Optional
import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from db.repositories import UserRepository, RoleRepository, CompanyRepository, ServiceAreaRepository
from models.base import UserModel, RoleModel
from models.entities import CompanyModel, ServiceAreaModel
from models.requests import CompanyCreateRequest, CompanyUpdateRequest, ServiceAreaCreateRequest
from core.exceptions import NotFoundError, DatabaseError, ValidationError, AuthenticationError

logger = logging.getLogger(__name__)

class AdminService:
    """Service for handling admin operations with database persistence"""
    
    def __init__(self, db: Session):
        self.db = db
    
    # User Management
    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get all users with pagination
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of user dictionaries
            
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            users = UserRepository.get_all(self.db, skip=skip, limit=limit)
            
            user_dicts = []
            for user in users:
                role = RoleRepository.get_by_id(self.db, user.role_id)
                user_dicts.append({
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "phone": user.phone,
                    "role": role.name if role else "Unknown",
                    "is_active": getattr(user, 'is_active', False),
                    "is_verified": getattr(user, 'is_verified', False),
                    "profile_picture": user.profile_picture,
                    "created_at": getattr(user, 'created_at', None) if getattr(user, 'created_at', None) is not None else None,
                    "updated_at": getattr(user, 'updated_at', None) if getattr(user, 'updated_at', None) is not None else None,
                    "last_login": getattr(user, 'last_login', None) if getattr(user, 'last_login', None) is not None else None
                })
            return user_dicts
            
        except Exception as e:
            logger.error(f"Error getting users: {e}")
            raise DatabaseError(f"Failed to get users: {str(e)}")
    
    def get_user_by_id(self, user_id: str) -> Dict[str, Any]:
        """
        Get user by ID
        
        Args:
            user_id: User identifier
            
        Returns:
            User dictionary with complete information
            
        Raises:
            NotFoundError: If user not found
            DatabaseError: If database operation fails
        """
        try:
            user = UserRepository.get_by_id(self.db, user_id)
            if not user:
                raise NotFoundError(f"User {user_id} not found")
            
            role = RoleRepository.get_by_id(self.db, user.role_id)
            company = None
            if user.company_id:
                company = CompanyRepository.get_by_id(self.db, user.company_id)
            
            return {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone": user.phone,
                "role": role.name if role else "Unknown",
                "company": company.name if company else None,
                "is_active": user.is_active,
                "is_verified": user.is_verified,
                "profile_picture": user.profile_picture,
                "created_at": user.created_at.isoformat() if user.created_at is not None else None,
                "updated_at": user.updated_at.isoformat() if user.updated_at is not None else None,
                "last_login": user.last_login.isoformat() if user.last_login is not None else None
            }
            
        except (NotFoundError, DatabaseError):
            raise
        except Exception as e:
            logger.error(f"Error getting user {user_id}: {e}")
            raise DatabaseError(f"Failed to get user: {str(e)}")
    
    def update_user_status(self, user_id: str, is_active: bool) -> Dict[str, Any]:
        """
        Update user active status
        
        Args:
            user_id: User identifier
            is_active: New active status
            
        Returns:
            Updated user dictionary
            
        Raises:
            NotFoundError: If user not found
            DatabaseError: If database operation fails
        """
        try:
            user = UserRepository.update_status(self.db, user_id, is_active)
            if not user:
                raise NotFoundError(f"User {user_id} not found")
            
            logger.info(f"User {user_id} status updated to {'active' if is_active else 'inactive'}")
            
            return self.get_user_by_id(user_id)
            
        except (NotFoundError, DatabaseError):
            raise
        except Exception as e:
            logger.error(f"Error updating user status: {e}")
            raise DatabaseError(f"Failed to update user status: {str(e)}")
    
    def update_user_role(self, user_id: str, role_id: str) -> Dict[str, Any]:
        """
        Update user role
        
        Args:
            user_id: User identifier
            role_id: New role identifier
            
        Returns:
            Updated user dictionary
            
        Raises:
            NotFoundError: If user or role not found
            ValidationError: If role is invalid
            DatabaseError: If database operation fails
        """
        try:
            # Validate role exists
            role = RoleRepository.get_by_id(self.db, role_id)
            if not role:
                raise ValidationError(f"Role {role_id} not found")
            
            user = UserRepository.update_role(self.db, user_id, role_id)
            if not user:
                raise NotFoundError(f"User {user_id} not found")
            
            logger.info(f"User {user_id} role updated to {role_id}")
            
            return self.get_user_by_id(user_id)
            
        except (NotFoundError, ValidationError, DatabaseError):
            raise
        except Exception as e:
            logger.error(f"Error updating user role: {e}")
            raise DatabaseError(f"Failed to update user role: {str(e)}")
    
    # Company Management
    def get_all_companies(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get all companies with pagination
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of company dictionaries
            
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            companies = CompanyRepository.get_all(self.db, skip=skip, limit=limit)
            
            company_dicts = []
            for company in companies:
                company_dicts.append({
                    "id": company.id,
                    "name": company.name,
                    "description": company.description,
                    "contact_email": company.contact_email,
                    "contact_phone": company.contact_phone,
                    "address": company.address,
                    "is_active": company.is_active,
                    "created_at": company.created_at.isoformat() if company.created_at is not None else None,
                    "updated_at": company.updated_at.isoformat() if company.updated_at is not None else None
                })
            
            return company_dicts
            
        except Exception as e:
            logger.error(f"Error getting companies: {e}")
            raise DatabaseError(f"Failed to get companies: {str(e)}")
    
    def create_company(self, company_data: CompanyCreateRequest) -> CompanyModel:
        """
        Create a new company
        
        Args:
            company_data: Company information
            
        Returns:
            Created company model
            
        Raises:
            ValidationError: If company data is invalid
            DatabaseError: If database operation fails
        """
        try:
            # Validate required fields
            if not company_data.name:
                raise ValidationError("Company name is required")
            
            if not company_data.email:
                raise ValidationError("Contact email is required")
            
            # Create company
            company = CompanyRepository.create(
                db=self.db,
                company_data=company_data
            )
            
            logger.info(f"Company created: {company.id}")
            
            return company
            
        except (ValidationError, DatabaseError):
            raise
        except Exception as e:
            logger.error(f"Error creating company: {e}")
            raise DatabaseError(f"Failed to create company: {str(e)}")
    
    def update_company(self, company_id: str, company_data: CompanyUpdateRequest) -> CompanyModel:
        """
        Update company information
        
        Args:
            company_id: Company identifier
            company_data: Updated company information
            
        Returns:
            Updated company model
            
        Raises:
            NotFoundError: If company not found
            ValidationError: If company data is invalid
            DatabaseError: If database operation fails
        """
        try:
            # Validate company exists
            existing_company = CompanyRepository.get_by_id(self.db, company_id)
            if not existing_company:
                raise NotFoundError(f"Company {company_id} not found")
            
            # Update company
            company = CompanyRepository.update(
                db=self.db,
                company_id=company_id,
                company_data=company_data
            )
            
            logger.info(f"Company {company_id} updated")
            
            return company
            
        except (NotFoundError, ValidationError, DatabaseError):
            raise
        except Exception as e:
            logger.error(f"Error updating company: {e}")
            raise DatabaseError(f"Failed to update company: {str(e)}")
    
    # Service Area Management
    def get_all_service_areas(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get all service areas with pagination
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of service area dictionaries
            
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            service_areas = ServiceAreaRepository.get_all(self.db, skip=skip, limit=limit)
            
            area_dicts = []
            for area in service_areas:
                area_dicts.append({
                    "id": area.id,
                    "name": area.name,
                    "description": area.description,
                    "center_lat": area.center_lat,
                    "center_lng": area.center_lng,
                    "radius_km": area.radius_km,
                    "is_active": area.is_active,
                    "created_at": area.created_at.isoformat() if area.created_at is not None else None,
                    "updated_at": area.updated_at.isoformat() if area.updated_at is not None else None
                })
            
            return area_dicts
            
        except Exception as e:
            logger.error(f"Error getting service areas: {e}")
            raise DatabaseError(f"Failed to get service areas: {str(e)}")
    
    def create_service_area(self, area_data: ServiceAreaCreateRequest) -> ServiceAreaModel:
        """
        Create a new service area
        
        Args:
            area_data: Service area information
            
        Returns:
            Created service area model
            
        Raises:
            ValidationError: If area data is invalid
            DatabaseError: If database operation fails
        """
        try:
            # Validate required fields
            if not area_data.name:
                raise ValidationError("Service area name is required")
            
            if not area_data.center_lat or not area_data.center_lng:
                raise ValidationError("Center coordinates are required")
            
            if not area_data.radius_km or area_data.radius_km <= 0:
                raise ValidationError("Valid radius is required")
            
            # Create service area
            area = ServiceAreaRepository.create(
                db=self.db,
                area_data=area_data
            )
            
            logger.info(f"Service area created: {area.id}")
            
            return area
            
        except (ValidationError, DatabaseError):
            raise
        except Exception as e:
            logger.error(f"Error creating service area: {e}")
            raise DatabaseError(f"Failed to create service area: {str(e)}")
    
    # Analytics and Reporting
    def get_dashboard_stats(self) -> Dict[str, Any]:
        """
        Get dashboard statistics
        
        Returns:
            Dictionary with dashboard statistics
            
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            # Get basic counts
            total_users = UserRepository.count_all(self.db)
            active_users = UserRepository.count_active(self.db)
            total_companies = CompanyRepository.count_all(self.db)
            total_service_areas = ServiceAreaRepository.count_all(self.db)
            
            # Get recent activity
            recent_users = UserRepository.get_recent(self.db, limit=7)
            recent_companies = CompanyRepository.get_recent(self.db, limit=7)
            
            return {
                "total_users": total_users,
                "active_users": active_users,
                "total_companies": total_companies,
                "total_service_areas": total_service_areas,
                "recent_users": len(recent_users),
                "recent_companies": len(recent_companies),
                "user_activity_rate": (active_users / total_users * 100) if total_users > 0 else 0
            }
            
        except Exception as e:
            logger.error(f"Error getting dashboard stats: {e}")
            raise DatabaseError(f"Failed to get dashboard stats: {str(e)}") 