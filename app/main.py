from fastapi import FastAPI
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User

app = FastAPI(
    title="FastAPI + MySQL Production App",
    version="1.0"
)

@app.get("/")
def root():
    return {"message": "FastAPI + MySQL is running inside Docker!"}

@app.get("/users")
def get_users():
    db: Session = SessionLocal()
    users = db.query(User).all()
    return users
