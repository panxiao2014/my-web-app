#!/usr/bin/env python3
"""
Database seeding script for testing purposes.
This script adds test users to the database to ensure tests have data to work with.
"""

import os
import sys
from pathlib import Path
from sqlalchemy import create_engine, inspect, text
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
        
        # Ensure the users table exists (supports custom __tablename__ changes)
        inspector = inspect(engine)
        users_table_name = Users.__tablename__
        if not inspector.has_table(users_table_name):
            # Create the table using raw SQL with IF NOT EXISTS and anonymous constraints
            create_sql = f"""
            CREATE TABLE IF NOT EXISTS {users_table_name} (
                id SERIAL PRIMARY KEY,
                name VARCHAR(40) NOT NULL UNIQUE,
                gender VARCHAR(6) NOT NULL CHECK (gender IN ('Male','Female')),
                age INTEGER NOT NULL CHECK (age >= 0 AND age <= 100)
            )
            """
            with engine.begin() as conn:
                conn.execute(text(create_sql))
        
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

            # Verify the seeded users can be retrieved
            retrieved = db.query(Users).filter(Users.name.in_([u.name for u in test_users])).all()
            retrieved_names = {u.name for u in retrieved}
            expected_names = {u.name for u in test_users}
            if retrieved_names != expected_names:
                print("Error: Seed verification failed. Expected users not found in database.")
                print(f"Expected: {sorted(expected_names)}, Retrieved: {sorted(retrieved_names)}")
                sys.exit(1)
            
            print(f"Successfully seeded database with {len(test_users)} test users:")
            for user in retrieved:
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
