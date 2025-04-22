# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build/Run Commands
- Run Flask server: `python server.py`
- Run FastAPI server: `uvicorn starter_api:app --reload`
- Database migration: `python database.py` (creates tables)
- Test database connection: `sqlite3 TutorConnect.db .tables`

## Code Style Guidelines
- Python: Follow PEP 8 conventions with descriptive variable names
- Import order: standard library -> third-party -> local modules
- Always use type annotations in Python function signatures
- JavaScript: Use ES6+ features, name functions with camelCase
- Error handling: Use try/except with specific exception types
- API endpoints: Follow RESTful conventions with proper status codes

## Project Structure
- Backend: Flask/FastAPI (Python) with SQLAlchemy ORM
- Authentication: JWT tokens with bcrypt password hashing
- Database: SQLite for development (PostgreSQL schema compatible)
- Frontend: Plain JavaScript with some templates using HTML/CSS

## Testing
- No formal testing framework currently implemented
- Recommended: Install pytest for future test development
- API testing with Postman or curl recommended