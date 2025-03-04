from fastapi import FastAPI, HTTPException
import sqlite3
from typing import List, Dict
from fastapi.responses import HTMLResponse

app = FastAPI()

db_path = "TutorConnect.db"  # Path to your SQLite database

def get_users_from_db() -> List[Dict]:
    """Fetch all users from the database."""
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # To return rows as dictionaries
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users", response_model=List[Dict])
def get_users():
    """API endpoint to get all users."""
    users = get_users_from_db()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users

@app.get("/users2", response_class=HTMLResponse)
def get_users():
    """API endpoint to get all users as an HTML table for HTMX frontend."""
    users = get_users_from_db()
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