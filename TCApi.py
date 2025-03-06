from fastapi import FastAPI, HTTPException, Form
import sqlite3
from fastapi.responses import HTMLResponse
from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change this in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

db_path = "TutorConnect.db"  # Path to the SQLite database

@app.post("/users/create", response_class=HTMLResponse)
def create_user(name: str = Form(...), email: str = Form(...), password: str = Form(...)):
    """API endpoint to create a new user via form data (for HTMX)."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
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
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    if not users:
        return "<p>No users found</p>"
    
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
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = [dict(row) for row in cursor.fetchall()]
        conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    
    return users
