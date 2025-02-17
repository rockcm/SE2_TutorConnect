from dateime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

# Authentication changes:
# This file is needed for user authentication in our FastAPI app because it manages JWT token validation and access control.
# The get_current_user function extracts information from the token.
# - This ensures that only authenticated users can access the routes. 
# Without this file, there would be no way to verify who is logged in or allowed to perform actions.

# Secret key for signing JWT tokens (change this in production)
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120  # Token expiration time

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dependency to retrieve the token from requests
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def hash_password(password: str) -> str:
    """Hashes a plain text password before storing it in the database."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies if a given plaintext password matches the stored hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Generates a JWT access token for authentication."""
    to_encode = data.copy()

    
    if "sub" in to_encode:
        to_encode["sub"] = str(to_encode["sub"])  

    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)):
    """Decodes JWT token and retrieves the current user."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")  # Extract user ID from token
        role: str = payload.get("role")    # Extract user role

        if user_id is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return {"sub": user_id, "role": role}  # Return user info as a dictionary

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

t
