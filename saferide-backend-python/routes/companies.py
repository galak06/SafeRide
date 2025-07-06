from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from db.database import get_db
from services.company_service import CompanyService
from models.entities.company import CompanyCreate, CompanyUpdate
from auth.auth import get_current_user, require_admin
from core.exceptions import NotFoundError, DatabaseError, ValidationError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/companies", tags=["companies"])

@router.get("/", response_model=List[dict])
async def get_companies(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    search: Optional[str] = Query(None, description="Search term for company name, description, or email"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    """
    Get all companies with pagination and filtering.
    Requires admin role.
    """
    try:
        company_service = CompanyService(db)
        companies = company_service.get_all_companies(
            skip=skip, 
            limit=limit, 
            search=search, 
            is_active=is_active
        )
        return companies
    except DatabaseError as e:
        logger.error(f"Database error in get_companies: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in get_companies: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{company_id}", response_model=dict)
async def get_company(
    company_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    """
    Get company by ID with driver information.
    Requires admin role.
    """
    try:
        company_service = CompanyService(db)
        company = company_service.get_company_by_id(company_id)
        return company
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DatabaseError as e:
        logger.error(f"Database error in get_company: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in get_company: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/", response_model=dict)
async def create_company(
    company_data: CompanyCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    """
    Create a new company.
    Requires admin role.
    """
    try:
        company_service = CompanyService(db)
        company = company_service.create_company(company_data)
        return company
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DatabaseError as e:
        logger.error(f"Database error in create_company: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in create_company: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/{company_id}", response_model=dict)
async def update_company(
    company_id: str,
    company_data: CompanyUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    """
    Update company information.
    Requires admin role.
    """
    try:
        company_service = CompanyService(db)
        company = company_service.update_company(company_id, company_data)
        return company
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DatabaseError as e:
        logger.error(f"Database error in update_company: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in update_company: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{company_id}")
async def delete_company(
    company_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    """
    Delete a company.
    Requires admin role.
    """
    try:
        company_service = CompanyService(db)
        success = company_service.delete_company(company_id)
        return {"message": "Company deleted successfully"}
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DatabaseError as e:
        logger.error(f"Database error in delete_company: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in delete_company: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/{company_id}/drivers/{driver_id}")
async def assign_driver_to_company(
    company_id: str,
    driver_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    """
    Assign a driver to a company.
    Requires admin role.
    """
    try:
        company_service = CompanyService(db)
        company = company_service.assign_driver_to_company(company_id, driver_id)
        return {"message": "Driver assigned to company successfully", "company": company}
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DatabaseError as e:
        logger.error(f"Database error in assign_driver_to_company: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in assign_driver_to_company: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{company_id}/drivers/{driver_id}")
async def remove_driver_from_company(
    company_id: str,
    driver_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    """
    Remove a driver from a company.
    Requires admin role.
    """
    try:
        company_service = CompanyService(db)
        company = company_service.remove_driver_from_company(company_id, driver_id)
        return {"message": "Driver removed from company successfully", "company": company}
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DatabaseError as e:
        logger.error(f"Database error in remove_driver_from_company: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in remove_driver_from_company: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/drivers/available", response_model=List[dict])
async def get_available_drivers(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    """
    Get all available drivers (not assigned to any company).
    Requires admin role.
    """
    try:
        company_service = CompanyService(db)
        drivers = company_service.get_available_drivers(skip=skip, limit=limit)
        return drivers
    except DatabaseError as e:
        logger.error(f"Database error in get_available_drivers: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in get_available_drivers: {e}")
        raise HTTPException(status_code=500, detail="Internal server error") 