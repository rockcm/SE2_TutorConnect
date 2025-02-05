from sqlalchemy import create_engine, Column, Integer, String, ARRAY, ForeignKey, DECIMAL, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

DATABASE_URL = "postgresql://user:password@localhost/tutor_matching"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    location = Column(String)
    preferred_subjects = Column(ARRAY(Integer))  # References Subject IDs
    preferred_availability = Column(ARRAY(String))
    created_at = Column(TIMESTAMP, server_default=func.now())

class Tutor(Base):
    __tablename__ = "tutors"
    
    tutor_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    location = Column(String)
    expertise = Column(ARRAY(Integer))  # References Subject IDs
    availability = Column(ARRAY(String))
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
Base.metadata.create_all(engine)