from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
from database import SessionLocal, User, Tutor, Subject
from auth_utils import get_current_user  

# Authentication changes: 
# Mostly focused on securing the /match/{user_id} endpoint. 
# The current_user: dict = Depends{get_current_user} line ensures that only authenticated users with a valid 
# - JWT token can get to the endpoint. 
# Also added user validation so that users can't retrieve matches for other accounts by checking user_ids. 
# Added role-based access control, so that only students can request tutors. 

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/match/{user_id}")
def get_matches(
    user_id: int, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)  #  Require authentication
):
    # Ensure the user is only requesting their own matches
    if current_user["sub"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    # Ensure only students can request tutor matches
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user or user.role != "student":
        raise HTTPException(status_code=403, detail="Only students can request matches")

    tutors = find_matches(db, user_id)
    return {"matches": [tutor.name for tutor in tutors]}

def find_matches(db: Session, user_id: int):
    user = db.query(User).filter(User.user_id == user_id).first()
    
    if not user:
        return None
    
    # Find tutors that match subjects & availability
    tutors = db.query(Tutor).filter(
        Tutor.expertise.overlap(user.preferred_subjects),
        Tutor.availability.overlap(user.preferred_availability)
    ).order_by(Tutor.rating.desc(), Tutor.experience_years.desc()).all()
    
    return tutors
