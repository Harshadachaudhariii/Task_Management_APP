from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# ---- Component 2: The Engine (the bridge to MySQL) ----
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False
                       )

# ---- Component 3: SessionLocal (the desk factory) ----
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

# ---- Component 4: Base (the master blueprint for tables) ----
Base = declarative_base()


# ---- The Office Manager: FastAPI dependency ----
def get_db():
    """
    This function is a FastAPI dependency that provides a database session.
    It ensures that the session is properly closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()