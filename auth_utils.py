from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

#Authentication changes:
# This file is needed for user auth in our FastAPI app because it manages JWT Token validation and access ccontrol.
# The get_current_user functions exctracts information from token
# - this ensures that only authenticated users can access the routes. 
# Without this file, there'd be mo way verify who is logged in or allowed to do stuff. 



#  Secret key for signing JWT tokens (change this in production)
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"

#Dependency to retrieve the token from requests
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    """ Decodes JWT token and retrieves the current user """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")  # Extract user ID from token
        role: str = payload.get("role")    # Extract user role

        if user_id is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return {"sub": user_id, "role": role}  #  Return user info as a dictionary

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
