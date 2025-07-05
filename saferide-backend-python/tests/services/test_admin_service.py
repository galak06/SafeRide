import pytest
from unittest.mock import patch, MagicMock
from services.admin_service import AdminService
from models.base import UserModel, RoleModel
from models.entities import CompanyModel, ServiceAreaModel
from datetime import datetime, timedelta

class TestAdminService:
    """Test Admin service functionality"""
    
    @pytest.fixture
    def db(self):
        return MagicMock(name="db_session")

    @pytest.fixture
    def admin_service(self, db):
        return AdminService(db)

    @pytest.fixture
    def mock_user(self):
        return UserModel(
            id="test-user-123",
            email="test@example.com",
            password_hash="hashed",  # Use password_hash to match UserModel
            first_name="Test",
            last_name="User",
            phone="+1234567890",
            role_id="role-1",
            company_id=None,
            is_active=True,
            is_verified=True,
            profile_picture=None,
            last_login=None,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

    @pytest.fixture
    def mock_role(self):
        return RoleModel(
            id="role-1",
            name="admin",
            description="Admin role",
            permissions=["view_users"],
            is_active=True
        )

    @pytest.fixture
    def mock_company(self):
        return CompanyModel(
            id="company-1",
            name="Test Company",
            description="A test company",
            address="123 Test St",
            phone="1234567890",
            email="company@example.com",
            service_areas=[],
            drivers=[],
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

    @pytest.fixture
    def mock_service_area(self):
        return ServiceAreaModel(
            id="area-1",
            name="Test Area",
            description="A test area",
            coordinates=[{"lat": 0.0, "lng": 0.0}],
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

    class TestGetDashboardData:
        @pytest.mark.asyncio
        async def test_get_dashboard_data_success(self, admin_service, db, mock_user, mock_company, mock_service_area):
            with patch('db.repositories.UserRepository.count_all', return_value=10), \
                 patch('db.repositories.UserRepository.count_active', return_value=8), \
                 patch('db.repositories.CompanyRepository.count_all', return_value=2), \
                 patch('db.repositories.ServiceAreaRepository.count_all', return_value=1), \
                 patch('db.repositories.UserRepository.get_recent', return_value=[mock_user]), \
                 patch('db.repositories.CompanyRepository.get_recent', return_value=[mock_company]):
                dashboard_data = admin_service.get_dashboard_stats()
                assert isinstance(dashboard_data, dict)
                assert dashboard_data["total_users"] == 10
                assert dashboard_data["active_users"] == 8
                assert dashboard_data["total_companies"] == 2
                assert dashboard_data["total_service_areas"] == 1
                assert dashboard_data["recent_users"] == 1
                assert dashboard_data["recent_companies"] == 1
                assert dashboard_data["user_activity_rate"] == 80

        @pytest.mark.asyncio
        async def test_get_dashboard_data_error_handling(self, admin_service):
            with patch('db.repositories.UserRepository.count_all', side_effect=Exception("DB Error")):
                with pytest.raises(Exception):
                    admin_service.get_dashboard_stats()

    # Additional tests for user/company/service area management would follow the same pattern:
    # Patch the relevant repository method, return mock data, and assert on the returned model/fields. 