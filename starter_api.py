from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Literal  # Restrict role values
from auth_utils import get_current_user, create_access_token, verify_password, hash_password
from database import SessionLocal, User  # Import User model and database session
import register  # Import register API from register.py

# Authentication changes:
# - Implemented authentication with JWT tokens.
# - Users must log in to get a token and use protected routes.
# - Passwords are securely hashed before storing.
# - Users are restricted to valid roles ("student" or "tutor").
# - JWT now stores user_id instead of email.

app = FastAPI()

# Include register routes from register.py
app.include_router(register.router)

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
    role: Literal["student", "tutor"]  # ✅ Restricts roles to valid values

@app.post("/login")
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)):
    """Logs in a user and returns an access token"""

    # Find user by email
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(
            form_data.password,
            user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generate access token using user_id instead of email
    access_token = create_access_token(
        data={"sub": user.user_id, "role": user.role})

    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/protected-endpoint")
def protected_route(current_user: dict = Depends(get_current_user)):
    """Protected route that requires authentication"""
    return {
        "message": "You have accessed a protected route!",
        "user": current_user}


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Starter with Authentication!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
