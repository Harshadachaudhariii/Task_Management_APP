from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session
from src.utils.db import get_db, engine, Base
from src.tasks.router import task_routes
from src.user.router import user_routes

@asynccontextmanager
async def lifespan(app: FastAPI):

    # Startup
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    Base.metadata.create_all(bind=engine)

    print("Database tables created/verified successfully!")

    yield

    # Shutdown
    print("Server shutting down...")


app = FastAPI(
    title="Task Management API",
    lifespan=lifespan
)
app.include_router(task_routes)
app.include_router(user_routes)


@app.get("/")
def home():
    return {"message": "Task Management API is running"}


@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "Database connected successfully!"}
