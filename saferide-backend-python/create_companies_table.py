#!/usr/bin/env python3
"""
Database migration script to create companies table and update users table.
This script creates the companies table with support for both circle and polygon operation areas,
and adds the company_id foreign key to the users table.
"""

import os
import sys
import uuid
from datetime import datetime
from sqlalchemy import create_engine, text, MetaData, Table, Column, String, Text, Boolean, DateTime, Float, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import ProgrammingError
import json

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.config import settings

def create_companies_table():
    """Create the companies table"""
    
    # Create database engine
    engine = create_engine(settings.database_url)
    
    try:
        with engine.begin() as conn:
            # Check if companies table already exists
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'companies'
                );
            """))
            
            if result.scalar():
                print("Companies table already exists. Skipping creation.")
                return
            
            # Create companies table
            conn.execute(text("""
                CREATE TABLE companies (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    name VARCHAR(255) NOT NULL UNIQUE,
                    description TEXT,
                    contact_email VARCHAR(255) NOT NULL,
                    contact_phone VARCHAR(50),
                    address TEXT,
                    operation_area_type VARCHAR(20) NOT NULL DEFAULT 'circle',
                    center_lat DOUBLE PRECISION,
                    center_lng DOUBLE PRECISION,
                    radius_km DOUBLE PRECISION,
                    polygon_coordinates JSONB,
                    is_active BOOLEAN NOT NULL DEFAULT TRUE,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
            """))
            
            # Create indexes for better performance
            conn.execute(text("""
                CREATE INDEX idx_companies_name ON companies(name);
                CREATE INDEX idx_companies_contact_email ON companies(contact_email);
                CREATE INDEX idx_companies_is_active ON companies(is_active);
                CREATE INDEX idx_companies_operation_area_type ON companies(operation_area_type);
            """))
            
            # Create trigger to update updated_at timestamp
            conn.execute(text("""
                CREATE OR REPLACE FUNCTION update_updated_at_column()
                RETURNS TRIGGER AS $$
                BEGIN
                    NEW.updated_at = CURRENT_TIMESTAMP;
                    RETURN NEW;
                END;
                $$ language 'plpgsql';
            """))
            
            conn.execute(text("""
                CREATE TRIGGER update_companies_updated_at 
                    BEFORE UPDATE ON companies 
                    FOR EACH ROW 
                    EXECUTE FUNCTION update_updated_at_column();
            """))
            
            print("✅ Companies table created successfully!")
            
    except Exception as e:
        print(f"❌ Error creating companies table: {e}")
        raise

def add_company_id_to_users():
    """Add company_id column to users table"""
    
    # Create database engine
    engine = create_engine(settings.database_url)
    
    try:
        with engine.begin() as conn:
            # Check if company_id column already exists
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.columns 
                    WHERE table_schema = 'public' 
                    AND table_name = 'users' 
                    AND column_name = 'company_id'
                );
            """))
            
            if result.scalar():
                print("company_id column already exists in users table. Skipping addition.")
                return
            
            # Add company_id column to users table
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN company_id UUID REFERENCES companies(id);
            """))
            
            # Create index for better performance
            conn.execute(text("""
                CREATE INDEX idx_users_company_id ON users(company_id);
            """))
            
            print("✅ company_id column added to users table successfully!")
            
    except Exception as e:
        print(f"❌ Error adding company_id to users table: {e}")
        raise

def insert_sample_companies():
    """Insert sample companies for testing"""
    
    # Create database engine
    engine = create_engine(settings.database_url)
    
    try:
        with engine.begin() as conn:
            # Check if sample companies already exist
            result = conn.execute(text("SELECT COUNT(*) FROM companies WHERE name LIKE 'Sample%';"))
            count = result.scalar() or 0
            
            if count > 0:
                print("Sample companies already exist. Skipping insertion.")
                return
            
            # Insert sample companies
            sample_companies = [
                {
                    "id": str(uuid.uuid4()),
                    "name": "Sample Taxi Company",
                    "description": "A sample taxi company for testing",
                    "contact_email": "contact@sampletaxi.com",
                    "contact_phone": "+1-555-0123",
                    "address": "123 Main St, New York, NY 10001",
                    "operation_area_type": "circle",
                    "center_lat": 40.7128,
                    "center_lng": -74.0060,
                    "radius_km": 25.0,
                    "is_active": True
                },
                {
                    "id": str(uuid.uuid4()),
                    "name": "Sample Ride Share",
                    "description": "A sample ride-sharing company",
                    "contact_email": "info@sampleshare.com",
                    "contact_phone": "+1-555-0456",
                    "address": "456 Broadway, New York, NY 10013",
                    "operation_area_type": "polygon",
                    "polygon_coordinates": [
                        {"lat": 40.7128, "lng": -74.0060},
                        {"lat": 40.7589, "lng": -73.9851},
                        {"lat": 40.7505, "lng": -73.9934},
                        {"lat": 40.7128, "lng": -74.0060}
                    ],
                    "is_active": True
                }
            ]
            
            for company in sample_companies:
                if company["operation_area_type"] == "circle":
                    conn.execute(text("""
                        INSERT INTO companies (
                            id, name, description, contact_email, contact_phone, address,
                            operation_area_type, center_lat, center_lng, radius_km, is_active
                        ) VALUES (
                            :id, :name, :description, :contact_email, :contact_phone, :address,
                            :operation_area_type, :center_lat, :center_lng, :radius_km, :is_active
                        );
                    """), company)
                else:  # polygon
                    company = company.copy()
                    company["polygon_coordinates"] = json.dumps(company["polygon_coordinates"])
                    conn.execute(text("""
                        INSERT INTO companies (
                            id, name, description, contact_email, contact_phone, address,
                            operation_area_type, polygon_coordinates, is_active
                        ) VALUES (
                            :id, :name, :description, :contact_email, :contact_phone, :address,
                            :operation_area_type, :polygon_coordinates, :is_active
                        );
                    """), company)
            
            print("✅ Sample companies inserted successfully!")
            
    except Exception as e:
        print(f"❌ Error inserting sample companies: {e}")
        raise

def main():
    """Main migration function"""
    print("🚀 Starting companies table migration...")
    
    try:
        # Create companies table
        create_companies_table()
        
        # Add company_id to users table
        add_company_id_to_users()
        
        # Insert sample data
        insert_sample_companies()
        
        print("🎉 Companies migration completed successfully!")
        
    except Exception as e:
        print(f"💥 Migration failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 