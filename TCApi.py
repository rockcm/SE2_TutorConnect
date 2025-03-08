from fastapi import FastAPI, HTTPException, Form
import sqlite3
from fastapi.responses import HTMLResponse
from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow cross-origin requests (update settings in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_path = "TutorConnect.db"  # Path to the SQLite database

@app.post("/users/create", response_class=HTMLResponse)
def create_user(name: str = Form(...), email: str = Form(...)):
    """API endpoint to create a new user via form data (for HTMX)."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # Insert a new user into the database
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        # Retrieve the ID of the newly created user
        user_id = cursor.lastrowid
        conn.close()
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    # Return an HTML table displaying the new user
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
        # Set row_factory so that rows can be accessed as dictionaries
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    if not users:
        return "<p>No users found</p>"
    
    # Build HTML table rows for each user record
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
    
    # If the user is not found, return a simple message
    if not user:
        return "<p>User not found</p>"
    
    # Return an HTML table containing the updated user information
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
        # Connect to the SQLite database
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
