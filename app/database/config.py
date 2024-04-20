from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from constants import (
    DB_HOST,
    DB_PASSWORD,
    DB_PORT,
    DB_USER,
)


def DATABASE_URL_asyncpg(self):
    # postgresql+asyncpg://postgres:postgres@localhost:5432/sa
    return (f"postgresql+asyncpg://{DB_USER}:"
            f"{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres")

engine = create_async_engine(
    url="sqlite+aiosqlite:///test.db",
    echo=True
)

db_session = async_sessionmaker(engine)

   
