from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from typing import Dict

app = FastAPI()

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Fake database
fake_db: Dict[str, str] = {}

class UserCreate(BaseModel):
    email: EmailStr
    password: str

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

@app.post("/register", status_code=201)
def register_user(user: UserCreate):
    if user.email in fake_db:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    hashed_password = hash_password(user.password)
    fake_db[user.email] = hashed_password
    return {"message": "User registered successfully"}

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Starter!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

