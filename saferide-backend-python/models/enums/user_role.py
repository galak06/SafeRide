from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    SUPPORT = "support"
    DRIVER = "driver"
    RIDER = "rider"
    COMPANY_ADMIN = "company_admin"
    COMPANY_MANAGER = "company_manager" 