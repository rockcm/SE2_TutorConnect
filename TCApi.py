from fastapi import FastAPI, HTTPException, Form, Request
import sqlite3
from fastapi.responses import HTMLResponse, JSONResponse
from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import traceback
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api")

app = FastAPI()

# Add middleware to log all requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    try:
        response = await call_next(request)
        logger.info(f"Response status: {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        logger.error(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"detail": str(e), "traceback": traceback.format_exc()},
        )

# Allow cross-origin requests (update settings in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up static files (CSS, JS, images)
db_path = "TutorConnect.db"  # Path to the SQLite database

@app.post("/users/create", response_class=HTMLResponse)
async def create_user(
    request: Request,
    name: str = Form(...),       # User's name
    email: str = Form(...),      # User's email
    password: str = Form(...),   # User's password
    role: str = Form("user")     # User's role (with a default value)
):
    """
    API endpoint to create a new user via form data (for HTMX).
    Now accepts a password as well.
    """
    logger.info(f"Creating user: {name}, {email}, role={role}")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # Insert a new user into the database, including the role field
        cursor.execute(
            "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
            (name, email, password, role)
        )
        conn.commit()
        # Retrieve the ID of the newly created user
        user_id = cursor.lastrowid
        conn.close()
        logger.info(f"User created successfully with ID: {user_id}")
    except sqlite3.Error as e:
        logger.error(f"Database error creating user: {str(e)}")
        return f"<p>Error creating user: {str(e)}</p>"
    
    # Return an HTML table displaying the new user's ID, name, and email.
    # Note: Password is kept hidden for security reasons.
    return f"""
    <table border="1">
        <thead>
            <tr><th>ID</th><th>Name</th><th>Email</th><th>Role</th></tr>
        </thead>
        <tbody>
            <tr><td>{user_id}</td><td>{name}</td><td>{email}</td><td>{role}</td></tr>
        </tbody>
    </table>
    """

@app.get("/users", response_class=HTMLResponse)
async def get_users(request: Request):
    """API endpoint to get all users as an HTML table for HTMX frontend."""
    logger.info("Getting all users")
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Access rows as dictionaries
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        conn.close()
        logger.info(f"Found {len(users)} users")
    except Exception as e:
        logger.error(f"Error getting users: {str(e)}")
        return f"<p>Error getting users: {str(e)}</p>"
    
    if not users:
        return "<p>No users found</p>"
    
    # Build HTML table rows for each user record (excluding the password field)
    table_rows = "".join(
        f"<tr><td>{user['user_id']}</td><td>{user['name']}</td><td>{user['email']}</td><td>{user['role']}</td></tr>" 
        for user in users
    )
    html_content = f"""
    <table border="1">
        <thead>
            <tr><th>ID</th><th>Name</th><th>Email</th><th>Role</th></tr>
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
async def update_user(
    user_id: int = Form(...),  # The ID of the user to update
    name: str = Form(...),     # New name for the user
    email: str = Form(...),    # New email for the user
    role: str = Form(None)     # New role for the user (optional)
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
        
        # First, check if the user exists
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        current_user = cursor.fetchone()
        
        if not current_user:
            conn.close()
            return "<p>User not found</p>"
            
        # Build update query based on provided parameters
        update_values = [name, email]
        update_query = "UPDATE users SET name = ?, email = ?"
        
        # Add role if provided and not None
        if role is not None:
            update_query += ", role = ?"
            update_values.append(role)
        
        # Add WHERE clause and user_id parameter
        update_query += " WHERE user_id = ?"
        update_values.append(user_id)
        
        # Execute the update query
        cursor.execute(update_query, update_values)
        conn.commit()
        
        # Retrieve the updated user record to display in the HTML response
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return "<p>Error: Updated user not found</p>"
        
        # Return an HTML table containing the updated user information
        html_content = f"""
        <table border="1">
            <thead>
                <tr><th>ID</th><th>Name</th><th>Email</th><th>Role</th></tr>
            </thead>
            <tbody>
                <tr>
                    <td>{user['user_id']}</td>
                    <td>{user['name']}</td>
                    <td>{user['email']}</td>
                    <td>{user['role']}</td>
                </tr>
            </tbody>
        </table>
        """
        return HTMLResponse(content=html_content)
        
    except Exception as e:
        logger.error(f"Error updating user: {str(e)}")
        logger.error(traceback.format_exc())
        return HTMLResponse(content=f"<p>Error updating user: {str(e)}</p>", status_code=500)

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
        f"<tr><td>{user['user_id']}</td><td>{user['name']}</td><td>{user['email']}</td><td>{user['role']}</td></tr>" 
        for user in users
    )
    
    html_content = f"""
    <table border="1">
        <thead>
            <tr><th>ID</th><th>Name</th><th>Email</th><th>Role</th></tr>
        </thead>
        <tbody>
            {table_rows}
        </tbody>
    </table>
    """
    return HTMLResponse(content=html_content)

@app.get("/users/search", response_class=HTMLResponse)
async def search_users(request: Request, search_term: str = ""):
    """
    API endpoint to search for users based on a search term.
    The search matches against both name and email fields.
    Returns an HTML table of matching users for HTMX frontend.
    """
    logger.info(f"Searching users with term: '{search_term}'")
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
        logger.info(f"Found {len(users)} users matching '{search_term}'")
    except Exception as e:
        logger.error(f"Error searching users: {str(e)}")
        return f"<p>Error searching users: {str(e)}</p>"
    
    if not users:
        return "<p>No matching users found</p>"
    
    # Build HTML table rows for each matching user
    table_rows = "".join(
        f"<tr><td>{user['user_id']}</td><td>{user['name']}</td><td>{user['email']}</td><td>{user['role']}</td></tr>" 
        for user in users
    )
    
    html_content = f"""
    <table border="1">
        <thead>
            <tr><th>ID</th><th>Name</th><th>Email</th><th>Role</th></tr>
        </thead>
        <tbody>
            {table_rows}
        </tbody>
    </table>
    """
    return HTMLResponse(content=html_content)

@app.get("/users/search/json")
async def search_users_json(request: Request, search_term: str = ""):
    """
    API endpoint to search for users based on a search term, returning JSON.
    The search matches against both name and email fields.
    """
    logger.info(f"Searching users (JSON) with term: '{search_term}'")
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
        logger.info(f"Found {len(users)} users matching '{search_term}' (JSON)")
    except Exception as e:
        logger.error(f"Error searching users (JSON): {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
    return users

@app.post("/users/login", response_class=HTMLResponse)
async def login_user(
    request: Request,
    email: str = Form(...),     # User's email
    password: str = Form(...)   # User's password
):
    """
    API endpoint to authenticate a user via form data (for HTMX).
    Checks email and password against the database.
    """
    logger.info(f"Login attempt for email: {email}")
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Check if user exists with the provided email and password
        cursor.execute(
            "SELECT * FROM users WHERE email = ? AND password = ?",
            (email, password)
        )
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            logger.warning(f"Login failed for email: {email}")
            return "<p class='error'>Invalid email or password</p>"
        
        logger.info(f"Login successful for user: {user['name']} (ID: {user['user_id']})")
        
        # Return success message with user details (excluding password)
        return f"""
        <div class="login-success">
            <h3>Login Successful!</h3>
            <p>Welcome back, {user['name']}!</p>
            <table border="1">
                <tr><th>ID</th><td>{user['user_id']}</td></tr>
                <tr><th>Name</th><td>{user['name']}</td></tr>
                <tr><th>Email</th><td>{user['email']}</td></tr>
                <tr><th>Role</th><td>{user['role']}</td></tr>
            </table>
            <script>
                // Store user information in localStorage
                localStorage.setItem('user_id', '{user['user_id']}');
                localStorage.setItem('user_name', '{user['name']}');
                localStorage.setItem('user_email', '{user['email']}');
                localStorage.setItem('user_role', '{user['role']}');
                localStorage.setItem('is_logged_in', 'true');
                
                // Redirect to dashboard or home page after a short delay
                setTimeout(() => {{
                    window.location.href = 'index.html';
                }}, 1500);
            </script>
        </div>
        """
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        return f"<p class='error'>Login error: {str(e)}</p>"


