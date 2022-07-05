from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:c011f0ae@localhost:5433/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={}, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

Base = declarative_base()


def get_db():
    """Get database session"""

    database = SessionLocal()

    try:
        yield database
    finally:
        database.close()
