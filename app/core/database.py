from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings


#  Get DB URL from settings
DATABASE_URL = settings.DATABASE_URL

#  Fix for Render (postgres → postgresql)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")

#  Create engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True  # helps avoid connection issues
)

#  Session
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)




#  Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()