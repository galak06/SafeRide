# Database Models

This directory contains all SQLAlchemy ORM models organized by domain for better maintainability and separation of concerns.

## Structure

```
db/models/
├── __init__.py              # Main package file - imports all models
├── enums.py                 # Enum definitions used across models
├── associations.py          # Many-to-many relationship tables
├── user.py                  # User authentication and management
├── role.py                  # Role-based access control
├── permission.py            # Fine-grained permissions
├── driver_company.py        # Transportation companies
├── service_area.py          # Company service coverage areas
├── user_location.py         # User GPS location tracking
├── ride.py                  # Transportation rides
├── route_plan.py            # Optimized route planning
├── route_stop.py            # Individual route stops
├── audit_log.py             # System activity logging
└── parent_child_relationship.py  # Family relationship management
```

## Usage

### Importing Models

**Option 1: Import from main db_models (recommended for backward compatibility)**
```python
from db.db_models import User, Role, ParentChildRelationship
```

**Option 2: Import from specific model files**
```python
from db.models.user import User
from db.models.role import Role
from db.models.parent_child_relationship import ParentChildRelationship
```

**Option 3: Import from models package**
```python
from db.models import User, Role, ParentChildRelationship
```

### Importing Enums

```python
from db.models.enums import UserRoleEnum, RideStatusEnum, CompanyStatusEnum, RelationshipTypeEnum
```

## Model Categories

### Authentication & Authorization
- **User**: Core user entity with authentication details
- **Role**: Role-based access control roles
- **Permission**: Fine-grained permissions for resources
- **AuditLog**: System activity tracking

### Transportation
- **DriverCompany**: Transportation service companies
- **ServiceArea**: Geographic service coverage areas
- **Ride**: Individual transportation rides
- **RoutePlan**: Optimized route planning
- **RouteStop**: Individual stops within routes

### Location & Tracking
- **UserLocation**: Real-time user GPS tracking

### Relationships
- **ParentChildRelationship**: Family relationship management

## Benefits of Modular Structure

1. **Separation of Concerns**: Each model has its own file with focused responsibility
2. **Maintainability**: Easier to find and modify specific models
3. **Scalability**: New models can be added without cluttering a single file
4. **Team Collaboration**: Multiple developers can work on different models simultaneously
5. **Testing**: Individual models can be tested in isolation
6. **Documentation**: Each model file can have detailed docstrings and comments

## Design Patterns

- **Single Responsibility Principle**: Each model file handles one domain entity
- **Dependency Inversion**: Models depend on abstractions (Base class) not concrete implementations
- **Open/Closed Principle**: New models can be added without modifying existing ones
- **Interface Segregation**: Each model exposes only the relationships it needs

## Adding New Models

1. Create a new file in `db/models/` with descriptive name
2. Import necessary SQLAlchemy components and Base
3. Define the model class with proper table name and columns
4. Add relationships as needed
5. Import the model in `db/models/__init__.py`
6. Add to `__all__` list in `db/models/__init__.py`
7. Import in main `db/db_models.py` for backward compatibility

## Example: Adding a New Model

```python
# db/models/example_model.py
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class ExampleModel(Base):
    """Example model for demonstration"""
    __tablename__ = "example_models"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

Then update the imports in `__init__.py` and `db_models.py`. 