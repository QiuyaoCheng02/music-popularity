# app/database.py
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# ========================================================
# Database Configuration
# Update username, password, and dbname as needed
# Format: postgresql://username:password@localhost/dbname
# ========================================================

SQLALCHEMY_DATABASE_URL = "postgresql://postgres@localhost/music_db"

# Create engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



# Database initialization function
def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully.")
    except Exception as e:
        print(f"⚠️ Warning: Database connection failed. Is PostgreSQL running? Error: {e}")