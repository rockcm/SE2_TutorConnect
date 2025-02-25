from sqlalchemy import create_engine, Column, Integer, String, ARRAY, ForeignKey, DECIMAL, TIMESTAMP, func
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import JSON
from sqlalchemy import DateTime


# Authentication changes: 
# Ensures that user credentials are stored and managed securely within the database. 
# The User model didn't have a way to store passwords, so added hashed password column to store user passwords. 
# Also added a role column so we can tell students and tutors apart. 
# Changed the name and email fields in Tutor model to be a FK to User table. This ensures all tutors are users.

DATABASE_URL = "sqlite:///tutor_matching.db"


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()



class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)  
    location = Column(String)

    # Changed ARRAY to JSON for SQLite
    preferred_subjects = Column(JSON, nullable=True)  # Store as JSON
    preferred_availability = Column(JSON, nullable=True)

    role = Column(String, nullable=False)  # Either 'student' or 'tutor'
    created_at = Column(TIMESTAMP, server_default=func.now())

class Tutor(Base):
    __tablename__ = "tutors"
    
    tutor_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, unique=True)

    # Changed ARRAY to JSON for SQLite
    expertise = Column(JSON, nullable=True)  
    availability = Column(JSON, nullable=True)

    experience_years = Column(Integer)
    rating = Column(DECIMAL(3, 2))
    created_at = Column(DateTime, default=func.now())


class Subject(Base):
    __tablename__ = "subjects"
    
    subject_id = Column(Integer, primary_key=True, index=True)
    subject_name = Column(String, unique=True, nullable=False)

class Match(Base):
    __tablename__ = "matches"
    
    match_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    tutor_id = Column(Integer, ForeignKey("tutors.tutor_id"), nullable=False)
    match_score = Column(DECIMAL(5, 2))
    created_at = Column(DateTime, default=func.now())
# Create tables
Base.metadata.create_all(engine)
