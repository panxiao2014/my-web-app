#!/usr/bin/env python3
"""
Database seeding script for testing purposes.
This script adds test users to the database to ensure tests have data to work with.
"""

import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Users
from .utils import read_postgres_password


def seed_database():
    """Seed the database with test users."""
    try:
        # Get database connection
        password = read_postgres_password()
        database_url = f"postgresql+psycopg2://postgres:{password}@localhost:5432/userdb"
        
        # Create engine and session
        engine = create_engine(database_url, pool_pre_ping=True)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        # Create tables if they don't exist
        Base.metadata.create_all(bind=engine)
        
        # Create session
        db = SessionLocal()
        
        try:
            # Check if users already exist
            existing_users = db.query(Users).count()
            if existing_users > 0:
                print(f"Database already has {existing_users} users. Skipping seeding.")
                return
            
            # Create test users
            test_users = [
                Users(name="Alice", gender="Female", age=25),
                Users(name="Bob", gender="Male", age=30),
            ]
            
            # Add users to database
            for user in test_users:
                db.add(user)
            
            # Commit changes
            db.commit()
            print(f"Successfully seeded database with {len(test_users)} test users:")
            for user in test_users:
                print(f"  - {user.name} ({user.gender}, age {user.age})")
                
        except Exception as e:
            db.rollback()
            print(f"Error seeding database: {e}")
            sys.exit(1)
        finally:
            db.close()
            
    except Exception as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    seed_database()
