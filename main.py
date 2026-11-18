from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.utils.db import get_db

app = FastAPI(title="Task Management API")

@app.get("/")
def home():
    return {"message": "Task Management API is running"}

@app.get("/test-db")
def test_db(db:Session=Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "Database connected successfully!"}
