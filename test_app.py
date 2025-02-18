import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from main import app, get_db, UserCreate, User
from database import Base  # Import Base from your database module

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables in the test database
Base.metadata.create_all(bind=engine)

# Dependency override for testing
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Override the get_db dependency in the app
app.dependency_overrides[get_db] = override_get_db

# Test client
client = TestClient(app)

# Fixture to clean up the database after each test
@pytest.fixture(scope="function")
def clean_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Test cases
def test_register_user(clean_db):
    """Test user registration"""
    user_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "securepassword",
        "role": "student",
    }

    response = client.post("/register", json=user_data)
    assert response.status_code == 201
    assert response.json()["message"] == "User registered successfully"
    assert "user_id" in response.json()

def test_register_existing_user(clean_db):
    """Test registration with an existing email"""
    user_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "securepassword",
        "role": "student",
    }

    # Register the user for the first time
    client.post("/register", json=user_data)

    # Try to register the same user again
    response = client.post("/register", json=user_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already exists"

def test_login_success(clean_db):
    """Test successful login"""
    user_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "securepassword",
        "role": "student",
    }

    # Register the user
    client.post("/register", json=user_data)

    # Login with correct credentials
    login_data = {
        "username": "john.doe@example.com",
        "password": "securepassword",
    }
    response = client.post("/login", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_invalid_credentials(clean_db):
    """Test login with invalid credentials"""
    user_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "securepassword",
        "role": "student",
    }

    # Register the user
    client.post("/register", json=user_data)

    # Login with incorrect password
    login_data = {
        "username": "john.doe@example.com",
        "password": "wrongpassword",
    }
    response = client.post("/login", data=login_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

def test_protected_endpoint(clean_db):
    """Test access to a protected endpoint"""
    user_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "securepassword",
        "role": "student",
    }

    # Register the user
    client.post("/register", json=user_data)

    # Login to get the access token
    login_data = {
        "username": "john.doe@example.com",
        "password": "securepassword",
    }
    login_response = client.post("/login", data=login_data)
    access_token = login_response.json()["access_token"]

    # Access the protected endpoint with the token
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/protected-endpoint", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "You have accessed a protected route!"
    assert response.json()["user"]["email"] == "john.doe@example.com"

def test_protected_endpoint_unauthorized(clean_db):
    """Test access to a protected endpoint without a token"""
    response = client.get("/protected-endpoint")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to FastAPI Starter with Authentication!"
