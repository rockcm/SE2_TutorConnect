from sqlachemy import create_engine, Column, Integer, String, ARRAY, ForeignKey, DECIMAL, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Authentication changes: 
# Ensures that user credentials are stored and managed securely within the database. 
# The User model didn't have a way to store passwords, so added hashed password column to store user passwords. 
# Also added a role column so we can tell students and tutors apart. 
# Changed the name and email fields in Tutor model to be a FK to User table. This ensures all tutors are users.

DATABASE_URL = "postgresql://user:password@localhost/tutor_matching"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    # AUTH: Added hashed_password field for authentication
    hashed_password = Column(String, nullable=False)  

    location = Column(String)
    
    # Restored PostgreSQL ARRAY type
    preferred_subjects = Column(ARRAY(Integer), nullable=True)  # References Subject IDs
    preferred_availability = Column(ARRAY(String), nullable=True)

    # AUTH: Added role field to differentiate between students and tutors
    role = Column(String, nullable=False)  # Either 'student' or 'tutor'

    created_at = Column(TIMESTAMP, server_default=func.now())

class Tutor(Base):
    __tablename__ = "tutors"
    
    tutor_id = Column(Integer, primary_key=True, index=True)

    # Replaced duplicate email and name fields with a foreign key reference to the User table
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, unique=True)  

    # Restored PostgreSQL ARRAY type
    expertise = Column(ARRAY(Integer), nullable=True)  # References Subject IDs
    availability = Column(ARRAY(String), nullable=True)
    
    experience_years = Column(Integer)
    rating = Column(DECIMAL(3, 2))
    created_at = Column(TIMESTAMP, server_default=func.now())

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
    created_at = Column(TIMESTAMP, server_default=func.now())

# Create tables
Base.metadata.create_all(engine)l
