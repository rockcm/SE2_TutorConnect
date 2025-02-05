from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, User, Tutor, Subject, find_matches

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/match/{user_id}")
def get_matches(user_id: int, db: Session = Depends(get_db)):
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