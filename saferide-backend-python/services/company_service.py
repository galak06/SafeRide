from typing import List, Dict, Any, Optional
import logging
from datetime import datetime
from sqlalchemy.orm import Session

from db.repositories import CompanyRepository, UserRepository
from models.entities.company import CompanyCreate, CompanyUpdate, CompanyModel, OperationAreaType
from core.exceptions import NotFoundError, DatabaseError, ValidationError

logger = logging.getLogger(__name__)

class CompanyService:
    """Service for handling company operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_companies(self, skip: int = 0, limit: int = 100, 
                         search: Optional[str] = None, is_active: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Get all companies with pagination and filtering
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            search: Search term for company name, description, or email
            is_active: Filter by active status
            
        Returns:
            List of company dictionaries
            
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            companies = CompanyRepository.get_all(self.db, skip=skip, limit=limit, 
                                                search=search, is_active=is_active)
            
            company_dicts = []
            for company in companies:
                driver_count = len(CompanyRepository.get_drivers(self.db, str(company.id)))
                company_dicts.append({
                    "id": str(company.id),
                    "name": company.name,
                    "description": company.description,
                    "contact_email": company.contact_email,
                    "contact_phone": company.contact_phone,
                    "address": company.address,
                    "operation_area_type": company.operation_area_type,
                    "center_lat": company.center_lat,
                    "center_lng": company.center_lng,
                    "radius_km": company.radius_km,
                    "polygon_coordinates": company.polygon_coordinates,
                    "is_active": company.is_active,
                    "created_at": company.created_at.isoformat() if company.created_at else None,
                    "updated_at": company.updated_at.isoformat() if company.updated_at else None,
                    "driver_count": driver_count
                })
            
            return company_dicts
            
        except Exception as e:
            logger.error(f"Error getting companies: {e}")
            raise DatabaseError(f"Failed to get companies: {str(e)}")
    
    def get_company_by_id(self, company_id: str) -> Dict[str, Any]:
        """
        Get company by ID
        
        Args:
            company_id: Company identifier
            
        Returns:
            Company dictionary with complete information
            
        Raises:
            NotFoundError: If company not found
            DatabaseError: If database operation fails
        """
        try:
            company = CompanyRepository.get_by_id(self.db, company_id)
            if not company:
                raise NotFoundError(f"Company {company_id} not found")
            
            drivers = CompanyRepository.get_drivers(self.db, company_id)
            driver_list = []
            for driver in drivers:
                driver_list.append({
                    "id": driver.id,
                    "first_name": driver.first_name,
                    "last_name": driver.last_name,
                    "email": driver.email,
                    "phone": driver.phone,
                    "is_active": driver.is_active
                })
            
            return {
                "id": str(company.id),
                "name": company.name,
                "description": company.description,
                "contact_email": company.contact_email,
                "contact_phone": company.contact_phone,
                "address": company.address,
                "operation_area_type": company.operation_area_type,
                "center_lat": company.center_lat,
                "center_lng": company.center_lng,
                "radius_km": company.radius_km,
                "polygon_coordinates": company.polygon_coordinates,
                "is_active": company.is_active,
                "created_at": company.created_at.isoformat() if company.created_at else None,
                "updated_at": company.updated_at.isoformat() if company.updated_at else None,
                "drivers": driver_list,
                "driver_count": len(driver_list)
            }
            
        except (NotFoundError, DatabaseError):
            raise
        except Exception as e:
            logger.error(f"Error getting company {company_id}: {e}")
            raise DatabaseError(f"Failed to get company: {str(e)}")
    
    def create_company(self, company_data: CompanyCreate) -> Dict[str, Any]:
        """
        Create a new company
        
        Args:
            company_data: Company creation data
            
        Returns:
            Created company dictionary
            
        Raises:
            ValidationError: If company data is invalid
            DatabaseError: If database operation fails
        """
        try:
            # Validate operation area data
            if company_data.operation_area_type == OperationAreaType.CIRCLE:
                if not company_data.center_lat or not company_data.center_lng or not company_data.radius_km:
                    raise ValidationError("Circle operation area requires center coordinates and radius")
            elif company_data.operation_area_type == OperationAreaType.POLYGON:
                if not company_data.polygon_coordinates or len(company_data.polygon_coordinates) < 3:
                    raise ValidationError("Polygon operation area requires at least 3 coordinates")
            
            # Check if company name already exists
            existing_company = CompanyRepository.get_by_name(self.db, company_data.name)
            if existing_company:
                raise ValidationError(f"Company with name '{company_data.name}' already exists")
            
            # Prepare company data for repository
            company_dict = company_data.dict()
            
            # Create company
            company = CompanyRepository.create(self.db, company_dict)
            
            logger.info(f"Company created: {company.id}")
            
            return self.get_company_by_id(str(company.id))
            
        except (ValidationError, DatabaseError):
            raise
        except Exception as e:
            logger.error(f"Error creating company: {e}")
            raise DatabaseError(f"Failed to create company: {str(e)}")
    
    def update_company(self, company_id: str, company_data: CompanyUpdate) -> Dict[str, Any]:
        """
        Update company information
        
        Args:
            company_id: Company identifier
            company_data: Updated company data
            
        Returns:
            Updated company dictionary
            
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
            
            # Validate operation area data if being updated
            if company_data.operation_area_type:
                if company_data.operation_area_type == OperationAreaType.CIRCLE:
                    if not company_data.center_lat or not company_data.center_lng or not company_data.radius_km:
                        raise ValidationError("Circle operation area requires center coordinates and radius")
                elif company_data.operation_area_type == OperationAreaType.POLYGON:
                    if not company_data.polygon_coordinates or len(company_data.polygon_coordinates) < 3:
                        raise ValidationError("Polygon operation area requires at least 3 coordinates")
            
            # Check name uniqueness if being updated
            if company_data.name and company_data.name != existing_company.name:
                name_exists = CompanyRepository.get_by_name(self.db, company_data.name)
                if name_exists:
                    raise ValidationError(f"Company with name '{company_data.name}' already exists")
            
            # Prepare update data
            update_data = company_data.dict(exclude_unset=True)
            
            # Update company
            company = CompanyRepository.update(self.db, company_id, update_data)
            if not company:
                raise NotFoundError(f"Company {company_id} not found")
            
            logger.info(f"Company {company_id} updated")
            
            return self.get_company_by_id(company_id)
            
        except (NotFoundError, ValidationError, DatabaseError):
            raise
        except Exception as e:
            logger.error(f"Error updating company: {e}")
            raise DatabaseError(f"Failed to update company: {str(e)}")
    
    def delete_company(self, company_id: str) -> bool:
        """
        Delete a company
        
        Args:
            company_id: Company identifier
            
        Returns:
            True if company was deleted
            
        Raises:
            NotFoundError: If company not found
            DatabaseError: If database operation fails
        """
        try:
            # Check if company exists
            company = CompanyRepository.get_by_id(self.db, company_id)
            if not company:
                raise NotFoundError(f"Company {company_id} not found")
            
            # Check if company has drivers
            drivers = CompanyRepository.get_drivers(self.db, company_id)
            if drivers:
                raise ValidationError(f"Cannot delete company with {len(drivers)} assigned drivers")
            
            # Delete company
            success = CompanyRepository.delete(self.db, company_id)
            if not success:
                raise NotFoundError(f"Company {company_id} not found")
            
            logger.info(f"Company {company_id} deleted")
            return True
            
        except (NotFoundError, ValidationError, DatabaseError):
            raise
        except Exception as e:
            logger.error(f"Error deleting company: {e}")
            raise DatabaseError(f"Failed to delete company: {str(e)}")
    
    def assign_driver_to_company(self, company_id: str, driver_id: str) -> Dict[str, Any]:
        """
        Assign a driver to a company
        
        Args:
            company_id: Company identifier
            driver_id: Driver (user) identifier
            
        Returns:
            Updated company dictionary
            
        Raises:
            NotFoundError: If company or driver not found
            ValidationError: If driver is not a driver role
            DatabaseError: If database operation fails
        """
        try:
            # Validate company exists
            company = CompanyRepository.get_by_id(self.db, company_id)
            if not company:
                raise NotFoundError(f"Company {company_id} not found")
            
            # Validate driver exists and has driver role
            driver = UserRepository.get_by_id(self.db, driver_id)
            if not driver:
                raise NotFoundError(f"Driver {driver_id} not found")
            
            # Check if user has driver role
            driver_roles = [role.name for role in driver.roles]
            if "driver" not in driver_roles:
                raise ValidationError(f"User {driver_id} does not have driver role")
            
            # Assign driver to company
            updated_driver = UserRepository.assign_to_company(self.db, driver_id, company_id)
            if not updated_driver:
                raise NotFoundError(f"Driver {driver_id} not found")
            
            logger.info(f"Driver {driver_id} assigned to company {company_id}")
            
            return self.get_company_by_id(company_id)
            
        except (NotFoundError, ValidationError, DatabaseError):
            raise
        except Exception as e:
            logger.error(f"Error assigning driver to company: {e}")
            raise DatabaseError(f"Failed to assign driver to company: {str(e)}")
    
    def remove_driver_from_company(self, company_id: str, driver_id: str) -> Dict[str, Any]:
        """
        Remove a driver from a company
        
        Args:
            company_id: Company identifier
            driver_id: Driver (user) identifier
            
        Returns:
            Updated company dictionary
            
        Raises:
            NotFoundError: If company or driver not found
            DatabaseError: If database operation fails
        """
        try:
            # Validate company exists
            company = CompanyRepository.get_by_id(self.db, company_id)
            if not company:
                raise NotFoundError(f"Company {company_id} not found")
            
            # Validate driver exists
            driver = UserRepository.get_by_id(self.db, driver_id)
            if not driver:
                raise NotFoundError(f"Driver {driver_id} not found")
            
            # Remove driver from company
            updated_driver = UserRepository.remove_from_company(self.db, driver_id)
            if not updated_driver:
                raise NotFoundError(f"Driver {driver_id} not found")
            
            logger.info(f"Driver {driver_id} removed from company {company_id}")
            
            return self.get_company_by_id(company_id)
            
        except (NotFoundError, DatabaseError):
            raise
        except Exception as e:
            logger.error(f"Error removing driver from company: {e}")
            raise DatabaseError(f"Failed to remove driver from company: {str(e)}")
    
    def get_available_drivers(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get all available drivers (not assigned to any company)
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of available driver dictionaries
            
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            drivers = UserRepository.get_drivers(self.db, skip=skip, limit=limit)
            
            available_drivers = []
            for driver in drivers:
                if not driver.company_id:  # Only include unassigned drivers
                    available_drivers.append({
                        "id": driver.id,
                        "first_name": driver.first_name,
                        "last_name": driver.last_name,
                        "email": driver.email,
                        "phone": driver.phone,
                        "is_active": driver.is_active
                    })
            
            return available_drivers
            
        except Exception as e:
            logger.error(f"Error getting available drivers: {e}")
            raise DatabaseError(f"Failed to get available drivers: {str(e)}") 