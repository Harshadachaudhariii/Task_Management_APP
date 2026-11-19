from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from src.utils.settings import settings

# ---- Component 2: The Engine (the bridge to MySQL) ----
engine = create_engine(
    url = settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=False
                       )

# ---- Component 3: Base (the master blueprint for tables) ----
Base = declarative_base()

# ---- Component 4: SessionLocal (the desk factory) ----
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

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