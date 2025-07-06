#!/usr/bin/env python3
"""
Script to create the children table in the database.
Run this script to add the children table to your existing database.
"""

import sys
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_children_table():
    """Create the children table in the database"""
    
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
        
        # SQL to create the children table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS children (
            id VARCHAR PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            email VARCHAR(255) UNIQUE,
            phone VARCHAR(20),
            parent_id VARCHAR NOT NULL,
            date_of_birth VARCHAR(10),
            grade VARCHAR(50),
            school VARCHAR(255),
            emergency_contact VARCHAR(20),
            notes TEXT,
            is_active BOOLEAN NOT NULL DEFAULT TRUE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """
        
        # Create indexes
        create_indexes_sql = """
        CREATE INDEX IF NOT EXISTS idx_children_first_name ON children(first_name);
        CREATE INDEX IF NOT EXISTS idx_children_last_name ON children(last_name);
        CREATE INDEX IF NOT EXISTS idx_children_email ON children(email);
        CREATE INDEX IF NOT EXISTS idx_children_parent_id ON children(parent_id);
        CREATE INDEX IF NOT EXISTS idx_children_is_active ON children(is_active);
        """
        
        # Add foreign key constraint
        add_foreign_key_sql = """
        ALTER TABLE children 
        ADD CONSTRAINT fk_children_parent_id 
        FOREIGN KEY (parent_id) REFERENCES users(id) ON DELETE CASCADE;
        """
        
        print("🔧 Creating children table...")
        
        # Execute the table creation
        db.execute(text(create_table_sql))
        print("✅ Children table created successfully")
        
        # Execute the index creation
        db.execute(text(create_indexes_sql))
        print("✅ Indexes created successfully")
        
        # Try to add foreign key constraint (might fail if constraint already exists)
        try:
            db.execute(text(add_foreign_key_sql))
            print("✅ Foreign key constraint added successfully")
        except Exception as e:
            print(f"⚠️  Foreign key constraint might already exist: {str(e)}")
        
        # Commit the changes
        db.commit()
        print("✅ Database changes committed successfully")
        
        # Verify the table was created
        result = db.execute(text("SELECT COUNT(*) FROM children"))
        count = result.scalar()
        print(f"✅ Children table verified - current count: {count}")
        
        db.close()
        print("🎉 Children table setup completed successfully!")
        
    except Exception as e:
        print(f"❌ Error creating children table: {str(e)}")
        if 'db' in locals():
            db.rollback()
            db.close()
        sys.exit(1)

if __name__ == "__main__":
    create_children_table() 