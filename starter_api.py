from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from database import SessionLocal, User  # Import User model and database session

# Authentication changes:
#  Replaced placeholder database with real PostGre database by using SeessionLocal.
# Using this to make sure stored hashed passwords are stored persistently. 
# Also changed the UserCreate model to have name and role field to match database schema for access control. 
# Added secure password hashing. 
# Now checks for duplicate emails. 

app = FastAPI()


# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Request model for user registration
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str  # "student" or "tutor"

# Function to hash passwords
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

@app.post("/register", status_code=201)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists in the database
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # Hash the password before storing it
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

    return {"message": "User registered successfully", "user_id": new_user.user_id}

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Starter with Authentication!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

