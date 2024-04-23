from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from constants import (
    DB_HOST,
    DB_PASSWORD,
    DB_PORT,
    DB_USER,
    DB_NAME,
)


def DATABASE_URL_asyncpg():
    # postgresql+asyncpg://postgres:postgres@localhost:5432/sa
    return f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(
    url=DATABASE_URL_asyncpg()
)

db_session = async_sessionmaker(engine)

   
