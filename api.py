from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

# CORS Middleware (Allows frontend to communicate with the API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for request validation
class Item(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

# Root endpoint
@app.get("/")
def home():
    return {"message": "Welcome to FastAPI!"}
