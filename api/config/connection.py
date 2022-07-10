from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


SQLALCHEMY_DATABASE_URL = (
    "postgresql+asyncpg://postgres:c011f0ae@localhost:5433/postgres"
)

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

session = sessionmaker(engine, expire_on_commit=True, future=True, class_=AsyncSession)
