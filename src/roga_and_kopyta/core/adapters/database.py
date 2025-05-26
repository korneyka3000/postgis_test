import uuid

from orjson import dumps, loads
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from roga_and_kopyta.config import settings


__all__ = (
    "async_database_engine",
    "async_session_maker",
)

async_database_engine = create_async_engine(
    url=settings.DB_URL.unicode_string(),
    plugins=["geoalchemy2"],
    json_deserializer=loads,
    json_serializer=lambda obj: dumps(obj).decode(),
    pool_use_lifo=True,
    max_overflow=100,
    pool_size=500,
    pool_pre_ping=True,
    echo=settings.DEBUG,
    connect_args={
        "prepared_statement_name_func": lambda: f"__asyncpg_{uuid.uuid4()}__",
        "statement_cache_size": 0,
        "prepared_statement_cache_size": 0,
    },
)
async_session_maker = async_sessionmaker(
    bind=async_database_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)
