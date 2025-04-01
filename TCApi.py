from fastapi import FastAPI, HTTPException, Form
import sqlite3
from fastapi.responses import HTMLResponse
from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request

app = FastAPI()

# Allow cross-origin requests (update settings in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Route for the home page
@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Route for another page (e.g., about.html)
@app.get("/about")
def about_page(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

db_path = "TutorConnect.db"  # Path to the SQLite database

@app.post("/users/create", response_class=HTMLResponse)
def create_user(
    name: str = Form(...),       # User's name
    email: str = Form(...),      # User's email
    password: str = Form(...)    # User's password (new parameter)
):
    """
    API endpoint to create a new user via form data (for HTMX).
    Now accepts a password as well.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # Insert a new user into the database, including the password field.
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, password)
        )
        conn.commit()
        # Retrieve the ID of the newly created user
        user_id = cursor.lastrowid
        conn.close()
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    # Return an HTML table displaying the new user's ID, name, and email.
    # Note: Password is kept hidden for security reasons.
    return f"""
    <table border="1">
        <thead>
            <tr><th>ID</th><th>Name</th><th>Email</th></tr>
        </thead>
        <tbody>
            <tr><td>{user_id}</td><td>{name}</td><td>{email}</td></tr>
        </tbody>
    </table>
    """

@app.get("/users", response_class=HTMLResponse)
def get_users():
    """API endpoint to get all users as an HTML table for HTMX frontend."""
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Access rows as dictionaries
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    if not users:
        return "<p>No users found</p>"
    
    # Build HTML table rows for each user record (excluding the password field)
    table_rows = "".join(
        f"<tr><td>{user['user_id']}</td><td>{user['name']}</td><td>{user['email']}</td></tr>" 
        for user in users
    )
    html_content = f"""
    <table border="1">
        <thead>
            <tr><th>ID</th><th>Name</th><th>Email</th></tr>
        </thead>
        <tbody>
            {table_rows}
        </tbody>
    </table>
    """
    return HTMLResponse(content=html_content)

@app.get("/users/json", response_model=List[Dict])
def get_users_json():
    """API endpoint to get all users as JSON."""
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = [dict(row) for row in cursor.fetchall()]
        conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    
    return users

@app.post("/users/update", response_class=HTMLResponse)
def update_user(
    user_id: int = Form(...),  # The ID of the user to update
    name: str = Form(...),     # New name for the user
    email: str = Form(...)     # New email for the user
):
    """
    API endpoint to update an existing user's details.
    Accepts form data and returns an HTML table with the updated user.
    This endpoint is intended for use with an HTMX frontend.
    """
    try:
        # Connect to the SQLite database and set row_factory for dictionary access
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Execute the update query for the specified user
        cursor.execute(
            "UPDATE users SET name = ?, email = ? WHERE user_id = ?",
            (name, email, user_id)
        )
        conn.commit()
        
        # If no rows were updated, the user was not found
        if cursor.rowcount == 0:
            conn.close()
            raise HTTPException(status_code=404, detail="User not found")
        
        # Retrieve the updated user record to display in the HTML response
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    if not user:
        return "<p>User not found</p>"
    
    # Return an HTML table containing the updated user information (excluding the password)
    html_content = f"""
    <table border="1">
        <thead>
            <tr><th>ID</th><th>Name</th><th>Email</th></tr>
        </thead>
        <tbody>
            <tr>
                <td>{user['user_id']}</td>
                <td>{user['name']}</td>
                <td>{user['email']}</td>
            </tr>
        </tbody>
    </table>
    """
    return HTMLResponse(content=html_content)

@app.post("/users/delete", response_class=HTMLResponse)
def delete_user(user_id: int = Form(...)):
    """
    API endpoint to delete a user based on their ID.
    Accepts form data and returns an HTML snippet confirming deletion.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # Execute the delete query
        cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()
        # Check if a user was actually deleted
        if cursor.rowcount == 0:
            conn.close()
            return "<p>User not found.</p>"
        conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # Return a confirmation message as HTML
    return f"<p>User with ID {user_id} has been deleted successfully.</p>"

@app.get("/users/search", response_class=HTMLResponse)
def search_users(search_term: str = ""):
    """
    API endpoint to search for users based on a search term.
    The search matches against both name and email fields.
    Returns an HTML table of matching users for HTMX frontend.
    """
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Use LIKE with wildcards to search for partial matches in name or email
        search_pattern = f"%{search_term}%"
        cursor.execute(
            "SELECT * FROM users WHERE name LIKE ? OR email LIKE ? ORDER BY name",
            (search_pattern, search_pattern)
        )
        users = cursor.fetchall()
        conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    if not users:
        return "<p>No matching users found</p>"
    
    # Build HTML table rows for each matching user
    table_rows = "".join(
        f"<tr><td>{user['user_id']}</td><td>{user['name']}</td><td>{user['email']}</td></tr>" 
        for user in users
    )
    
    html_content = f"""
    <table border="1">
        <thead>
            <tr><th>ID</th><th>Name</th><th>Email</th></tr>
        </thead>
        <tbody>
            {table_rows}
        </tbody>
    </table>
    """
    return HTMLResponse(content=html_content)

@app.get("/users/search/json")
def search_users_json(search_term: str = ""):
    """
    API endpoint to search for users based on a search term, returning JSON.
    The search matches against both name and email fields.
    """
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Use LIKE with wildcards to search for partial matches in name or email
        search_pattern = f"%{search_term}%"
        cursor.execute(
            "SELECT * FROM users WHERE name LIKE ? OR email LIKE ? ORDER BY name",
            (search_pattern, search_pattern)
        )
        users = [dict(row) for row in cursor.fetchall()]
        conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return users
