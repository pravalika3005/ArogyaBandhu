from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# =========================================================
# DATABASE CONFIGURATION
# =========================================================

DATABASE_URL = "sqlite:///./arogyabandhu.db"


# =========================================================
# DATABASE ENGINE
# =========================================================

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)


# =========================================================
# DATABASE SESSION
# =========================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# =========================================================
# BASE CLASS
# =========================================================

Base = declarative_base()


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()