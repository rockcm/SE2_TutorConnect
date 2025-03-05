from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from database import SessionLocal, User  # Import User model and DB session
from auth_utils import hash_password  # Import password hashing function
from typing import Literal  # Restrict role values

# Create an APIRouter instance (so it can be imported)
router = APIRouter()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# User registration model
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Literal["student", "tutor"]  # Restricts roles to valid values

@router.post("/register", status_code=201)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Registers a new user with hashed password and stores in database"""
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # Hash the password before storing
    hashed_password = hash_password(user.password)

    # Create a new user in the database
    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "user_id": new_user.user_id"}
    }