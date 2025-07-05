from sqlalchemy import create_engine, event, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError, OperationalError
import logging
from typing import Generator
import time
from contextlib import contextmanager

from core.config import settings

# Configure logging
logger = logging.getLogger(__name__)

# Database engine with connection pooling
engine = create_engine(
    settings.database_url,
    poolclass=QueuePool,
    pool_size=10,  # Number of connections to maintain
    max_overflow=20,  # Additional connections that can be created
    pool_pre_ping=True,  # Validate connections before use
    pool_recycle=3600,  # Recycle connections after 1 hour
    echo=settings.debug,  # Log SQL queries in debug mode
    connect_args={
        "connect_timeout": 10,  # Connection timeout
        "application_name": "SafeRide API"  # Application name for monitoring
    }
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """
    Database dependency with connection pooling and error handling
    
    Yields:
        Session: Database session
        
    Raises:
        DatabaseError: If database connection fails
    """
    db = SessionLocal()
    try:
        # Test connection before yielding
        db.execute(text("SELECT 1"))
        yield db
    except (SQLAlchemyError, OperationalError) as e:
        logger.error(f"Database connection error: {str(e)}")
        db.rollback()
        raise DatabaseError(f"Database connection failed: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected database error: {str(e)}")
        db.rollback()
        raise DatabaseError(f"Database operation failed: {str(e)}")
    finally:
        db.close()

@contextmanager
def get_db_session():
    """
    Context manager for database sessions with automatic cleanup
    
    Yields:
        Session: Database session
        
    Raises:
        DatabaseError: If database operation fails
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Database session error: {str(e)}")
        raise DatabaseError(f"Database operation failed: {str(e)}")
    finally:
        db.close()

def check_database_health() -> dict:
    """
    Check database health and connection status
    
    Returns:
        dict: Health status information
    """
    try:
        start_time = time.time()
        db = SessionLocal()
        
        # Test basic connectivity
        result = db.execute(text("SELECT 1 as test")).fetchone()
        response_time = time.time() - start_time
        
        # Get connection pool status
        pool = engine.pool
        pool_status = {
            "pool_type": type(pool).__name__,
            "pool_size": getattr(pool, '_pool_size', 'unknown'),
            "max_overflow": getattr(pool, '_max_overflow', 'unknown')
        }
        
        db.close()
        
        return {
            "status": "healthy",
            "response_time_ms": round(response_time * 1000, 2),
            "pool_status": pool_status,
            "timestamp": time.time()
        }
        
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": time.time()
        }

def init_database():
    """
    Initialize database tables
    
    Raises:
        DatabaseError: If database initialization fails
    """
    try:
        # Import all models to ensure they are registered
        from models.entities import ServiceArea, DriverCompany, UserLocation, RoutePlan, ParentChildRelationship
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise DatabaseError(f"Database initialization failed: {str(e)}")

# Database event listeners for monitoring
@event.listens_for(engine, "connect")
def receive_connect(dbapi_connection, connection_record):
    """Log when a new database connection is established"""
    logger.debug("New database connection established")

@event.listens_for(engine, "checkout")
def receive_checkout(dbapi_connection, connection_record, connection_proxy):
    """Log when a connection is checked out from the pool"""
    logger.debug("Database connection checked out from pool")

@event.listens_for(engine, "checkin")
def receive_checkin(dbapi_connection, connection_record):
    """Log when a connection is checked back into the pool"""
    logger.debug("Database connection checked back into pool")

# Import DatabaseError for exception handling
from core.exceptions import DatabaseError 