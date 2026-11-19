from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session
from src.utils.db import get_db, engine, Base, SessionLocal

# 1. Define the Lifespan Context Manager
@asynccontextmanager
async def lifespan(app: FastAPI):

    print("APPLICATION STARTING...")

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        print("DATABASE CONNECTED SUCCESSFULLY!")

        Base.metadata.create_all(bind=engine)

    except Exception as e:
        print("DATABASE CONNECTION FAILED!")
        print(type(e).__name__)
        print(str(e))
        raise

    yield

    print("SERVER SHUTTING DOWN...")

app = FastAPI(
    title="Task Management API",
    lifespan=lifespan
)

@app.get("/")
def home():
    return {"message": "Task Management API is running"}

@app.get("/test-db")
def test_db(db:Session=Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "Database connected successfully!"}
