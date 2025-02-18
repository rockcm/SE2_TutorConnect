from fastapi import FastAI
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, User

app = FastAPI()

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
    email: str
    password: str
    role: str

# Example User model (adjust based on your actual model)
class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)
