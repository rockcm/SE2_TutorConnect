# tests/test_tcapi.py

from fastapi.testclient import TestClient
from TCApi import app  # Make sure this matches your filename exactly
import pytest
import sqlite3

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from Dockerized FastAPI!"}

@pytest.fixture(scope="module")
def test_db():
    # Connect to test database
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    
    # Clean up from previous tests
    cursor.execute("DELETE FROM users")
    conn.commit()
    
    # Make sure password column exists in schema
    try:
        cursor.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'password' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN password TEXT")
            conn.commit()
    except Exception as e:
        print(f"Error checking/creating password column: {e}")
    
    # Insert test data
    cursor.execute(
        "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
        ("Test User", "test@example.com", "password123", "student")
    )
    conn.commit()
    
    # Get the ID of the inserted user
    cursor.execute("SELECT last_insert_rowid()")
    user_id = cursor.fetchone()[0]
    
    # Insert a user that will match the "Updated" search term
    cursor.execute(
        "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
        ("Updated Search", "updated_search@example.com", "searchpass", "student")
    )
    conn.commit()
    
    conn.close()
    
    return {"user_id": user_id}

def test_create_user():
    response = client.post(
        "/users/create",
        data={
            "name": "New User",
            "email": "new@example.com",
            "password": "newpass123",
            "role": "student"
        }
    )
    assert response.status_code == 200
    assert "New User" in response.text
    assert "new@example.com" in response.text

def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert "Test User" in response.text or "New User" in response.text

def test_get_user_by_id(test_db):
    user_id = test_db["user_id"]
    response = client.get(f"/users/json?user_id={user_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test User"
    assert response.json()["email"] == "test@example.com"
    assert "password" in response.json()  # Ensure password field exists in response

def test_update_user(test_db):
    user_id = test_db["user_id"]
    response = client.post(
        "/users/update",
        data={
            "user_id": user_id,
            "name": "Updated User",
            "email": "updated@example.com",
            "role": "tutor"
        }
    )
    assert response.status_code == 200
    assert "Updated User" in response.text
    assert "updated@example.com" in response.text

def test_delete_user():
    # Create a user to delete
    create_response = client.post(
        "/users/create",
        data={
            "name": "Delete Me",
            "email": "delete@example.com",
            "password": "deletepass",
            "role": "student"
        }
    )
    
    # Extract user_id from response
    user_id = None
    for line in create_response.text.split("\n"):
        if "<td>" in line and "</td>" in line and not user_id:
            user_id = line.split("<td>")[1].split("</td>")[0]
            break
    
    # Delete the user
    delete_response = client.post(
        "/users/delete",
        data={"user_id": user_id}
    )
    assert delete_response.status_code == 200
    # Match the exact message in the response
    assert f"User with ID {user_id} has been deleted successfully." in delete_response.text

def test_search_users():
    # Search for "Updated" which should match the user we created in the fixture
    response = client.get("/users/search?search_term=Updated")
    assert response.status_code == 200
    assert "Updated" in response.text

def test_login():
    # First create a user with known credentials
    client.post(
        "/users/create",
        data={
            "name": "Login User",
            "email": "login@example.com",
            "password": "loginpass123",
            "role": "student"
        }
    )
    
    # Try to login with the created user
    response = client.post(
        "/users/login",
        data={
            "email": "login@example.com",
            "password": "loginpass123"
        }
    )
    assert response.status_code == 200
    assert "Login Successful!" in response.text  # Case-sensitive match

    