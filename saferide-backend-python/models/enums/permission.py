from enum import Enum

class Permission(str, Enum):
    # User Management
    VIEW_USERS = "view_users"
    CREATE_USERS = "create_users"
    EDIT_USERS = "edit_users"
    DELETE_USERS = "delete_users"
    BLOCK_USERS = "block_users"
    
    # Ride Management
    VIEW_RIDES = "view_rides"
    CREATE_RIDES = "create_rides"
    EDIT_RIDES = "edit_rides"
    CANCEL_RIDES = "cancel_rides"
    ASSIGN_DRIVERS = "assign_drivers"
    
    # Driver Management
    VIEW_DRIVERS = "view_drivers"
    APPROVE_DRIVERS = "approve_drivers"
    SUSPEND_DRIVERS = "suspend_drivers"
    RATE_DRIVERS = "rate_drivers"
    
    # Company Management
    MANAGE_COMPANIES = "manage_companies"
    VIEW_COMPANY_DRIVERS = "view_company_drivers"
    ASSIGN_DRIVERS_TO_COMPANY = "assign_drivers_to_company"
    MANAGE_SERVICE_AREAS = "manage_service_areas"
    
    # Route Planning
    PLAN_ROUTES = "plan_routes"
    VIEW_ROUTE_OPTIMIZATION = "view_route_optimization"
    MANAGE_USER_LOCATIONS = "manage_user_locations"
    
    # Analytics & Reports
    VIEW_ANALYTICS = "view_analytics"
    EXPORT_REPORTS = "export_reports"
    VIEW_REVENUE = "view_revenue"
    
    # System Settings
    MANAGE_SETTINGS = "manage_settings"
    VIEW_LOGS = "view_logs"
    MANAGE_ROLES = "manage_roles"
    
    # Real-time Monitoring
    VIEW_LIVE_RIDES = "view_live_rides"
    TRACK_DRIVERS = "track_drivers" 