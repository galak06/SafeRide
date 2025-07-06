#!/usr/bin/env python3
"""
Script to add sample children data to the database for testing.
"""

import sys
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import uuid

# Load environment variables
load_dotenv()

def add_sample_children():
    """Add sample children data to the database"""
    
    # Get database URL from environment
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ Error: DATABASE_URL environment variable not set")
        sys.exit(1)
    
    try:
        # Create database engine
        engine = create_engine(database_url)
        
        # Create a session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Sample children data
        sample_children = [
            {
                "id": str(uuid.uuid4()),
                "first_name": "Emma",
                "last_name": "Johnson",
                "email": "emma.johnson@example.com",
                "phone": "+1234567890",
                "parent_id": "admin-001",
                "date_of_birth": "2015-03-15",
                "grade": "3rd Grade",
                "school": "Elementary School",
                "emergency_contact": "+1234567891",
                "notes": "Allergic to peanuts",
                "is_active": True
            },
            {
                "id": str(uuid.uuid4()),
                "first_name": "Liam",
                "last_name": "Smith",
                "email": "liam.smith@example.com",
                "phone": "+1234567892",
                "parent_id": "admin-001",
                "date_of_birth": "2017-08-22",
                "grade": "1st Grade",
                "school": "Elementary School",
                "emergency_contact": "+1234567893",
                "notes": "Loves soccer",
                "is_active": True
            },
            {
                "id": str(uuid.uuid4()),
                "first_name": "Sophia",
                "last_name": "Williams",
                "email": "sophia.williams@example.com",
                "phone": "+1234567894",
                "parent_id": "admin-001",
                "date_of_birth": "2019-11-08",
                "grade": "Kindergarten",
                "school": "Elementary School",
                "emergency_contact": "+1234567895",
                "notes": "Very shy, needs extra attention",
                "is_active": True
            }
        ]
        
        print("🔧 Adding sample children data...")
        
        # Insert each child
        for child in sample_children:
            insert_sql = """
            INSERT INTO children (
                id, first_name, last_name, email, phone, parent_id, 
                date_of_birth, grade, school, emergency_contact, notes, is_active
            ) VALUES (
                :id, :first_name, :last_name, :email, :phone, :parent_id,
                :date_of_birth, :grade, :school, :emergency_contact, :notes, :is_active
            ) ON CONFLICT (id) DO NOTHING;
            """
            
            db.execute(text(insert_sql), child)
            print(f"✅ Added child: {child['first_name']} {child['last_name']}")
        
        # Commit the changes
        db.commit()
        print("✅ Sample children data committed successfully")
        
        # Verify the data was added
        result = db.execute(text("SELECT COUNT(*) FROM children"))
        count = result.scalar()
        print(f"✅ Total children in database: {count}")
        
        # Show the added children
        result = db.execute(text("SELECT id, first_name, last_name, parent_id FROM children"))
        children = result.fetchall()
        print("\n📋 Children in database:")
        for child in children:
            print(f"  - {child[1]} {child[2]} (ID: {child[0]}, Parent: {child[3]})")
        
        db.close()
        print("\n🎉 Sample children data added successfully!")
        
    except Exception as e:
        print(f"❌ Error adding sample children: {str(e)}")
        if 'db' in locals():
            db.rollback()
            db.close()
        sys.exit(1)

if __name__ == "__main__":
    add_sample_children() 